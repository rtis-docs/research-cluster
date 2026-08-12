# Aoraki Slurm wait time and GRES exporter

A small Prometheus exporter that fills three gaps left by
[prometheus-slurm-exporter](https://github.com/vpenso/prometheus-slurm-exporter), which is what
currently feeds `research-monitoring.otago.ac.nz`.

That exporter publishes 56 `slurm_*` metrics. All of them are *counts* of jobs and nodes, or
*capacity* in CPU cores. None of them records:

* **how long jobs waited before starting** — that lives in slurmdbd and nothing scrapes it;
* **GPUs allocated versus configured** — there are no `slurm_gpus_*` metrics on this build at
  all, so nothing distinguishes a GPU that is *held by a job* from one that is merely *busy*;
* **why a job is pending** — a dependency hold and a full cluster look identical in
  `slurm_queue_pending`.

This exporter adds those three, and nothing else.

## What it does not do

It never submits a job. It runs `sacct`, `squeue` and `sinfo` — the same read-only client
commands you would type by hand — and serves the results over HTTP. Nothing is scheduled and
no compute node is touched.

## Cost

Measured on `rtis-login-r01` against the live cluster:

| Query | Frequency | Wall | CPU | Rows |
| :-- | :-- | --: | --: | --: |
| `sacct`, 2-hour window | every 60s | 0.06s | ~0.00s | ~450 |
| `squeue` | every 60s | 0.01s | ~0.00s | ~370 |
| `sinfo` | every 60s | 0.01s | ~0.00s | ~96 |
| `sacct`, 7-day backfill | **once, at first start** | 2.34s | 0.31s | ~73,000 |

Steady state is 0.08s of wall time per 60-second cycle — a **0.13% duty cycle**, and
effectively no CPU. The load falls on slurmdbd and slurmctld.

The backfill is the only heavy query and it runs exactly once, to seed the histogram so the
dashboard is useful immediately rather than after a week of accumulation. `--backfill 0` skips
it and starts from empty.

## Install

Recommended host is **`rtis-xdmod-p01`**: it already runs prometheus-slurm-exporter on `:8080`
and already has slurmdbd access, so this adds one unit and one scrape target and needs no new
firewall rule. Any host with `sacct`, `squeue` and `sinfo` will do — the login node is the
fallback.

```bash
install -m 0755 slurm_wait_exporter.py /usr/local/bin/slurm_wait_exporter.py
install -m 0644 slurm-wait-exporter.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now slurm-wait-exporter
curl -s localhost:9341/metrics | head
```

> The unit runs under `DynamicUser=yes`. This relies on the munge socket being world-accessible,
> which is the default (`/var/run/munge/munge.socket.2`, mode 0777) but is sometimes tightened.
> If the logs show munge authentication failures, replace `DynamicUser=yes` with a static
> `User=` that is in the munge group.

Then add one scrape job to Prometheus:

```yaml
  - job_name: slurm-wait
    scrape_interval: 60s
    static_configs:
      - targets: ['rtis-xdmod-p01.uod.otago.ac.nz:9341']
```

Finally import `../grafana/aoraki-queue-availability.json` into Grafana.

Two things about that file are load-bearing and should not be changed casually:

* **Panel IDs are fixed** (100-102, 110-111, 120-123, 130-131). The documentation site embeds
  them by ID through `d-solo`, so renumbering a panel silently blanks a graph on the site.
* **The datasource is hardcoded** to uid `UeV7jcYVk`, the existing Prometheus datasource on
  `research-monitoring.otago.ac.nz`, so the import needs no datasource mapping. Point it
  elsewhere and the queries will need remapping.

Five of the eleven panels use metrics that already exist and will render immediately. The other
six need this exporter running before they show anything.

## Metrics

### `aoraki_job_wait_seconds` — histogram, by `partition`

Seconds between a job becoming **eligible** and starting.

The wait is measured from `Eligible`, not `Submit`. This matters: job `3981468` was submitted
at 2026-03-26T12:32, became eligible at 2026-03-27T12:23, and started at exactly its eligible
time. Measuring from `Submit` would have recorded a 24-hour wait that was entirely a `--begin`
or dependency hold of the submitter's own making. `Eligible` measures only the part the cluster
is responsible for.

Buckets are `5, 15, 30, 60, 300, 900, 1800, 3600, 7200, 21600, 43200, 86400, 259200, 604800`
seconds. They are sized from the measured distribution — 35% of jobs start within a minute,
but the tail reaches 15 days, so both ends need resolution. Waits under 5 seconds cannot be
resolved further and read as "under 5 seconds".

Counters are cumulative and persist across restarts in
`/var/lib/aoraki-wait-exporter/state.json`. Each refresh re-queries with a 2-hour overlap and
dedupes on `JobIDRaw`, so a missed or slow run cannot drop jobs or count them twice.

### `aoraki_pending_job_seconds_{max,median}` — gauge, by `partition`

How long the jobs queued *right now* have been waiting. Jobs held by a dependency, an
administrative hold or `--begin` are excluded — they are not waiting on the cluster.

### `aoraki_pending_jobs` — gauge, by `partition` and `blocked`

Queued job counts. `blocked="true"` covers `Dependency`, `DependencyNeverSatisfied`,
`JobHeldUser`, `JobHeldAdmin` and `BeginTime`. Keeping these separate matters: a large share of
Aoraki's pending queue at any moment is dependency holds, and counting them as contention
badly overstates how loaded the cluster is.

### `aoraki_gres_{gpu,shard}_{total,alloc,unavailable}` — gauge, by `gpu_type`

GPUs configured, currently allocated to jobs, and sitting on nodes that are down, drained or
reserved. `unavailable` is deliberately separate from `alloc`: at the time of writing all eight
H200s are unavailable rather than busy, because `aoraki44` is drained with
`GPU0 Error : Not responding`. A dashboard that only showed "not free" would make a hardware
fault look like demand.

Parsed from `sinfo -N`, **deduped by node first**. `sinfo -N` emits one row per node *per
partition* — `aoraki11` appears three times, under `aoraki_short`, `aoraki_gpu` and
`aoraki_gpu_A100_80GB` — so summing the raw rows triple-counts every GPU node.

Note these will not tally with the DCGM panels. DCGM sees 67 GPUs; Slurm manages 57. The extra
ten are on `rtis-gpu-01..04` and include a TITAN V and some L40S that are not in any cluster
partition.

## Checking it

`--oneshot` prints one scrape and exits; `--dry-run` additionally leaves the state file alone.
Together they let you test against real data without installing anything or writing to disk:

```bash
ssh aoraki "python3 - --oneshot --dry-run --state '' --backfill 604800" < slurm_wait_exporter.py
```

The histogram this produces should reproduce the wait times you get by computing
`Start - Eligible` from `sacct` directly. Verified against 72,199 jobs over 7 days:

| Partition | Histogram p50 | Exact p50 |
| :-- | --: | --: |
| `aoraki_gpu_A100_80GB` | 18h 37m | 18h 14m |
| `aoraki_bigmem` | 44m | 44m |
| `aoraki_bigcpu` | 23m | 24m |
| `aoraki_gpu` | 30m | 30m |
| `aoraki_gpu_H200` | 23s | 23s |

GPU counts should match `sinfo` exactly (57 configured, 32 allocated at the time of that run).
