# Deploying the queue and availability data

This is the runbook for phases 1 and 2 — getting the exporter running and the dashboard
imported. Once both are done the six `aoraki_*` panels have data, and the documentation page
(phase 3) can be published.

Nothing here touches the documentation site. The site is unaffected until the page is merged.

## What you are deploying, and where

| Stage | What | Host | Reversible? |
| :-- | :-- | :-- | :-- |
| 1 | `slurm_wait_exporter.py` + systemd unit | `rtis-xdmod-p01.uod.otago.ac.nz` | Yes — stop and remove two files |
| 2 | One scrape job in `prometheus.yml` | wherever Prometheus runs (`research-monitoring`) | Yes — delete four lines, reload |
| 3 | Dashboard `aoraki-queue-availability.json` | Grafana | Yes — delete the dashboard |

The two hosts differ, so stages 1 and 2 are separate SSH sessions. Between them there is a
firewall check, which is the step most likely to need someone else.

Total hands-on time is about twenty minutes. There is no maintenance window and no restart of
anything that users depend on: Prometheus takes a `SIGHUP`, and Grafana is untouched apart
from an import.

---

## Stage 1 — the exporter

### 1.1 Dry-run it first, on the target host

Do this before installing anything. It runs the exporter's whole collection path against live
Slurm and prints what it would serve, without writing a state file or leaving a process behind.

```bash
scp monitoring/slurm-wait-exporter/slurm_wait_exporter.py rtis-xdmod-p01.uod.otago.ac.nz:/tmp/
ssh rtis-xdmod-p01.uod.otago.ac.nz \
  "python3 /tmp/slurm_wait_exporter.py --oneshot --dry-run --state '' --backfill 604800"
```

This is the slowest thing the exporter ever does — the 7-day backfill, roughly 4.5 seconds
and 260 MB of peak RSS. If it completes here it will complete under systemd.

**What you are checking:**

* It exits 0 and prints a few hundred lines of Prometheus text format.
* The log line reads `recorded N newly started jobs` with N in the low thousands — about
  11,700 for a 7-day backfill. Zero means `sacct` returned nothing, which usually means no
  slurmdbd access. N in the tens of thousands means the array collapse below is not working:
  `sacct` returns roughly 56,000 rows for the same week, and the exporter counts each array
  once rather than once per task.
* `aoraki_gres_gpu_total` sums to **57**, matching what Slurm manages. Not 67 — that is the
  DCGM figure and includes cards outside the cluster partitions.
* There is **no** `gpu_type="unknown"` series.
* **No partition's `le="+Inf"` bucket is far above its `le="604800"` one.** A large gap means
  jobs are being recorded with multi-year waits, which is what happens if a job cancelled
  while pending slips through — `sacct` renders its `Start` as `2106-02-07`, the `UINT32_MAX`
  sentinel, rather than as `Unknown`. The exporter drops any start in the future for exactly
  this reason. It is worth confirming, because on a bad week that is 60% of the rows on
  `aoraki_fastcore` and 20% on `aoraki_gpu_A100_80GB`.
* **`aoraki_gpu`'s median is seconds, not tens of minutes.** It is the partition holding
  almost every GPU on the cluster, and it is rarely contended. A median in the tens of
  minutes there means array tasks are being counted individually: each task of an array
  inherits the array's `Eligible` time, so the hundredth task is charged for the ninety-nine
  ahead of it — which its submitter's `QOSMaxJobsPerUserLimit` caused, not the cluster. Cross-
  check against `squeue -p aoraki_gpu -t PD -O JobID,Reason`; if the live queue is empty or
  everything in it says `QOSMaxJobsPerUserLimit`, a long median is the exporter, not Aoraki.

A quick check of the last two:

```bash
ssh rtis-xdmod-p01.uod.otago.ac.nz \
  "python3 /tmp/slurm_wait_exporter.py --oneshot --dry-run --state '' --backfill 0" \
  | grep '^aoraki_gres_gpu_total' \
  | awk '{s+=$2} END {print "configured GPUs:", s}'
```

If Python is older than 3.6 on that host, stop — the script uses f-strings. Everything else it
needs is in the standard library, so there is nothing to `pip install`.

If `sacct` is missing or unauthorised, fall back to `rtis-login-r01` for the whole of stage 1
and change the scrape target in step 2.1 accordingly. Everything else is identical.

### 1.2 Install

```bash
scp monitoring/slurm-wait-exporter/slurm_wait_exporter.py \
    monitoring/slurm-wait-exporter/slurm-wait-exporter.service \
    rtis-xdmod-p01.uod.otago.ac.nz:/tmp/

ssh rtis-xdmod-p01.uod.otago.ac.nz
sudo install -m 0755 /tmp/slurm_wait_exporter.py /usr/local/bin/slurm_wait_exporter.py
sudo install -m 0644 /tmp/slurm-wait-exporter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now slurm-wait-exporter
```

`StateDirectory=aoraki-wait-exporter` in the unit creates `/var/lib/aoraki-wait-exporter`
automatically with the right ownership. Do not create it by hand — under `DynamicUser=yes` the
UID is allocated at start, so a directory you made yourself will have the wrong owner.

**Replacing the script later is `install` plus `systemctl restart`, with one caveat.** The
state file carries a `version`, and a release that changes how a wait is counted bumps it.
The exporter then discards the old state and backfills 7 days afresh, which is correct — the
alternative is a histogram half-built under each rule. Prometheus sees the counters drop, and
treats it as a counter reset, so `rate()` recovers on its own. Anything on the dashboard
looking back past the restart will read low until the window clears it, which for panels 100
and 101 is 6 hours.

### 1.3 Confirm it started

```bash
systemctl status slurm-wait-exporter --no-pager
curl -s localhost:9341/metrics | head -30
```

The first start blocks on the 7-day backfill before it opens the port, so allow a few seconds
before the first `curl`. After that, requests are served from cached state and return
immediately — the collection runs on a background thread every 60 seconds.

Then confirm the state file was written, which is what makes the histogram survive a restart:

```bash
sudo ls -l /var/lib/aoraki-wait-exporter/state.json
```

**If it failed to start**, `journalctl -u slurm-wait-exporter -n 50 --no-pager`. The one
failure mode worth anticipating is munge:

> The unit runs under `DynamicUser=yes`, which relies on the munge socket being
> world-accessible. That is the default (`/var/run/munge/munge.socket.2`, mode 0777) but is
> sometimes tightened. If the log shows munge authentication failures, replace
> `DynamicUser=yes` with a static `User=` belonging to the munge group, then
> `daemon-reload` and restart. You will then need to create `/var/lib/aoraki-wait-exporter`
> owned by that user.

### 1.4 Sanity-check the numbers against Slurm

The exporter's GPU counts come from parsing `sinfo -N`, which lists a node once *per
partition*. Confirm the dedupe held, by comparing against Slurm at the same moment:

```bash
curl -s localhost:9341/metrics | grep '^aoraki_gres_gpu_alloc' | awk '{s+=$2} END {print "exporter alloc:", s}'
sinfo -h -N -O "NodeList:30,GresUsed:60" | sort -u -k1,1 \
  | grep -o 'gpu:[A-Za-z0-9_.-]*:[0-9]*' | awk -F: '{s+=$3} END {print "sinfo alloc:  ", s}'
```

These should agree. If the exporter's figure is two to three times larger, the dedupe is not
working and the parse needs looking at before the dashboard means anything.

### 1.5 Open the port

Prometheus must reach `rtis-xdmod-p01:9341`. Port `8080` on the same host is already scraped
(the existing `SLURM` job), but that is open to the whole network in the `public` zone, so it
proves nothing about `9341`.

From the **Prometheus host**:

```bash
curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://rtis-xdmod-p01.uod.otago.ac.nz:9341/metrics
```

`200` and you are done. A timeout means a firewall rule is needed. `rtis-xdmod-p01` runs
firewalld with a dedicated **`prometheus` zone** that already holds `9100/tcp` for
node_exporter, and that is where this belongs — not a loose rich rule in `public`:

```bash
sudo firewall-cmd --permanent --zone=prometheus --add-port=9341/tcp
sudo firewall-cmd --permanent --zone=prometheus --add-source=10.66.32.94/32   # only if absent
sudo firewall-cmd --reload
```

Check the source list first with `sudo firewall-cmd --zone=prometheus --list-all`. Two traps
here, both of which cost time on the first deployment:

* **Use the Prometheus host's own address, not the site name.** `research-monitoring.otago.ac.nz`
  resolves to `10.69.242.37`, which is a front-end VIP. The host is `rtis-monitor-p01` and it
  sends from **`10.66.32.94`**. A rule written against the VIP silently never matches. Confirm
  with `ip route get 10.66.31.89` on the Prometheus host and read the `src` field.
* **Adding that source also grants it `9100/tcp`**, since it is a zone not a per-port rule.
  That is almost certainly correct — it is the Prometheus host — but it is a wider change than
  opening one port, so make it deliberately.

Do not move on until this returns 200. Adding the scrape job before the port is reachable just
produces a target that is permanently down.

---

## Stage 2 — Prometheus and Grafana

### 2.1 Add the scrape job

Prometheus is version **2.37.0**, configured from **`/etc/prometheus/prometheus.yml`**, on the
same host as Grafana (its datasource points at `http://localhost:9090`).

Append to the `scrape_configs:` list, alongside the existing `prometheus`, `node`, `GPU`,
`SLURM`, `ondemand` and two `weka-*` jobs:

```yaml
  - job_name: slurm-wait
    scrape_interval: 60s
    static_configs:
      - targets: ['rtis-xdmod-p01.uod.otago.ac.nz:9341']
```

The global `scrape_interval` is 15s; 60s is deliberate here because the exporter only refreshes
its data once a minute, so anything faster returns the same numbers repeatedly. The global
`scrape_timeout` of 10s is left alone and is ample — responses are served from cache.

Back up first, since this file feeds every dashboard you have:

`scrape_configs:` is the last top-level key in the file, so appending at the end lands inside
it:

```bash
sudo cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.bak
sudo vi /etc/prometheus/prometheus.yml
sudo /usr/local/bin/promtool check config /etc/prometheus/prometheus.yml
```

**`promtool` needs its absolute path under `sudo`.** It lives in `/usr/local/bin`, which is not
in this host's `secure_path` (`/sbin:/bin:/usr/sbin:/usr/bin`), so plain
`sudo promtool` fails with `command not found` even though `which promtool` finds it. It is
already installed; there is nothing to `dnf install`.

Do not skip the check. A YAML error here takes Prometheus down on reload, and that stops every
existing dashboard, not just this one.

### 2.2 Reload Prometheus

**`--web.enable-lifecycle` is `false` on this instance**, so `curl -X POST /-/reload` will be
refused. Use a `SIGHUP` via systemd:

```bash
sudo systemctl reload prometheus
sudo systemctl status prometheus --no-pager
```

A reload does not drop the TSDB or interrupt other scrapes. If your unit has no `ExecReload`,
`sudo kill -HUP $(pidof prometheus)` does the same thing. Restarting is not necessary.

### 2.3 Confirm the target is up

Prometheus UI → **Status → Targets** → look for `slurm-wait`. State should be **UP** with a
recent "Last Scrape" and no error.

Or from Grafana's **Explore** tab, against the Prometheus datasource:

```promql
up{job="slurm-wait"}
```

Expect `1`. Then confirm real data is arriving, not just an empty 200:

```promql
aoraki_gres_gpu_total
sum(aoraki_job_wait_seconds_count)
time() - aoraki_wait_exporter_last_scrape_timestamp_seconds
```

The last one should stay under about 120 seconds. If it climbs steadily, the HTTP server is
alive but the background refresh thread has died — check `journalctl` for `refresh failed`.

### 2.4 Import the dashboard

In Grafana: **Dashboards → New → Import → Upload dashboard JSON file**, and select
`monitoring/grafana/aoraki-queue-availability.json`.

It should import without prompting for a datasource, because the datasource uid `UeV7jcYVk` is
written into every panel. If Grafana *does* prompt, the datasource uid has changed since this
was built and the JSON needs updating rather than mapping — mapping at import time will not
persist into the `d-solo` embeds the documentation uses.

Two things in that file are load-bearing:

* **The uid is `aoraki-queue`.** Every iframe on the documentation page is
  `/d-solo/aoraki-queue/...`. Let Grafana assign a different uid on import and all eleven
  panels go blank on the site.
* **Panel IDs are fixed** — 100–102, 110–111, 120–124, 130–131. The page embeds them by ID.
  Rearranging panels in the UI is safe; deleting and recreating one is not, because it comes
  back with a new ID.

### 2.5 Confirm the panels render, and that they render *embedded*

Five panels use metrics that already existed and should have a week of history immediately:
110, 111, 121, 124, 130, 131. The six `aoraki_*` panels — 100, 101, 102, 120, 122, 123 — start
from the moment of first scrape.

Panel **100** (median wait) is the exception and will look empty at first. It is a
`rate()` over a 6-hour window on a counter, so it needs two scrapes to draw anything and
several hours before the line is meaningful. Panel **120** (GPUs free by type) is the one to
watch instead for an immediate signal — it is a plain gauge and should populate within a
minute.

Finally, check one panel through the embed route the site actually uses, in a private browser
window so you are testing the anonymous view rather than your logged-in session:

```
https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&panelId=120&theme=light
```

A graph means the site will work. A "Dashboard not found" means the uid changed at import.

> Note that `d-solo` returns HTTP 200 for a dashboard that does not exist — it is a
> single-page app shell. You have to look at the rendered page; a status code proves nothing.

---

## After a day, and after a week

**The 7-day backfill does not make panels 100 and 101 meaningful straight away**, which is
counter-intuitive enough to be worth stating plainly. The backfill sets the counter's starting
*level*, but those panels are `rate()` over a 6-hour window, and a rate measures the *increase*
since the first scrape. For the first few hours they therefore describe only the handful of
jobs that started since deployment — expect to see medians of a few seconds on every partition,
including ones the reference figures below put in the hours. That is the window filling, not a
broken parse. Give it a full 6 hours before judging the numbers.

The backfill still earns its place: it makes `sum(aoraki_job_wait_seconds_count)` a real figure
from the first scrape, and it means a restart does not reset the counters and corrupt every
`rate()` spanning it. Worth revisiting once:

* **After a few hours** — panel 100 should show plausible medians. As a reference, the figures
  from 11,702 submissions (56,355 tasks) over the week to 11 August 2026 were 13h median on
  `aoraki_gpu_A100_80GB`, 30m on `aoraki_bigcpu`, 27s on `aoraki_gpu_H200`, and 2s on both
  `aoraki_gpu_L4_24GB` and `aoraki_gpu`. If the dashboard disagrees with that shape by an
  order of magnitude, something is wrong with the parse rather than with the cluster.
* **After a restart** — confirm panel 100 has no downward step in it. A drop to zero means the
  state file is not persisting and the counters reset, which corrupts every `rate()` over that
  window.
* **Panel 123 (GPUs offline)** is expected to be non-zero: `aoraki44` is drained with
  `GPU0 Error : Not responding`, which is why all eight H200s currently read as unavailable
  rather than busy. That panel exists so a hardware fault does not masquerade as demand.

## Rolling it back

Stage 2, dashboard only — delete the dashboard in Grafana. Nothing else is affected.

Stage 2, scrape job:

```bash
sudo cp /etc/prometheus/prometheus.yml.bak /etc/prometheus/prometheus.yml
sudo promtool check config /etc/prometheus/prometheus.yml
sudo systemctl reload prometheus
```

Stage 1, the exporter:

```bash
sudo systemctl disable --now slurm-wait-exporter
sudo rm /etc/systemd/system/slurm-wait-exporter.service /usr/local/bin/slurm_wait_exporter.py
sudo systemctl daemon-reload
sudo rm -rf /var/lib/aoraki-wait-exporter        # only if you do not intend to reinstall
```

Keep the state directory if there is any chance of reinstalling. Deleting it throws away the
accumulated histogram, and the backfill can only rebuild the last seven days of it.

The already-collected `aoraki_*` samples stay in the Prometheus TSDB either way. Retention is
unlimited on this instance (`storage.tsdb.retention.time` is `0s`), so nothing expires them.

## Ongoing cost

Measured against the live cluster:

| Query | Frequency | Wall | CPU |
| :-- | :-- | --: | --: |
| `sacct`, 2-hour window | every 60s | 0.06s | ~0.00s |
| `squeue` | every 60s | 0.01s | ~0.00s |
| `sinfo` | every 60s | 0.01s | ~0.00s |
| `sacct`, 7-day backfill | once, at first start | 3.67s | 1.92s |

Steady state is 0.08 seconds of wall time per 60-second cycle — a 0.13% duty cycle. The load
falls on slurmdbd and slurmctld, not on the host running the exporter. Prometheus gains one
target producing roughly 150 series.
