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

This is the slowest thing the exporter ever does — the 7-day backfill, roughly 2.5 seconds
and 260 MB of peak RSS. If it completes here it will complete under systemd.

**What you are checking:**

* It exits 0 and prints a few hundred lines of Prometheus text format.
* `aoraki_job_wait_seconds_count{partition="aoraki_gpu_A100_80GB"}` is a large number, not
  zero. Zero means `sacct` returned nothing, which usually means no slurmdbd access.
* `aoraki_gres_gpu_total` sums to **57**, matching what Slurm manages. Not 67 — that is the
  DCGM figure and includes cards outside the cluster partitions.
* There is **no** `gpu_type="unknown"` series.

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
(the existing `SLURM` job), so the path exists — but `9341` is a new port and may need adding.

From the **Prometheus host**:

```bash
curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://rtis-xdmod-p01.uod.otago.ac.nz:9341/metrics
```

`200` and you are done. A timeout means a firewall rule is needed; on a firewalld host that is:

```bash
sudo firewall-cmd --permanent --add-port=9341/tcp && sudo firewall-cmd --reload
```

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

```bash
sudo cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.bak
sudo vi /etc/prometheus/prometheus.yml
sudo promtool check config /etc/prometheus/prometheus.yml
```

Do not skip `promtool check config`. A YAML error here takes Prometheus down on reload, and
that stops every existing dashboard, not just this one.

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
* **Panel IDs are fixed** — 100–102, 110–111, 120–123, 130–131. The page embeds them by ID.
  Rearranging panels in the UI is safe; deleting and recreating one is not, because it comes
  back with a new ID.

### 2.5 Confirm the panels render, and that they render *embedded*

Five panels use metrics that already existed and should have a week of history immediately:
110, 111, 121, 130, 131. The six `aoraki_*` panels — 100, 101, 102, 120, 122, 123 — start
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

The histogram is cumulative and seeded with a 7-day backfill, so panels 100 and 101 are usable
almost immediately. Worth revisiting once:

* **After a few hours** — panel 100 should show plausible medians. As a reference, the figures
  measured by hand from 72,199 jobs over the week to 5 August 2026 were 18h 14m median on
  `aoraki_gpu_A100_80GB`, 44m on `aoraki_bigmem`, 23s on `aoraki_gpu_H200`, and effectively
  zero on `aoraki_gpu_L4_24GB`. If the dashboard disagrees with that shape by an order of
  magnitude, something is wrong with the parse rather than with the cluster.
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
| `sacct`, 7-day backfill | once, at first start | 2.34s | 0.31s |

Steady state is 0.08 seconds of wall time per 60-second cycle — a 0.13% duty cycle. The load
falls on slurmdbd and slurmctld, not on the host running the exporter. Prometheus gains one
target producing roughly 150 series.
