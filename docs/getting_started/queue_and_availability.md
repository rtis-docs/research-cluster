# Queue and Availability

!!! overview "On this Page"
    - How full each partition is, and how much of the cluster's memory is committed
    - How long jobs have recently waited before starting, partition by partition
    - Which GPUs are free, which are allocated or offline, and how hard they are working
    - How to read these graphs without drawing the wrong conclusion

The cheapest moment to change your mind about a job is before you submit it. If the GPU you
asked for is heavily oversubscribed and a similar one is sitting idle, moving your job across
can be the difference between starting in a minute and starting tomorrow.

!!! note

    This data is only visible if you are on the University of Otago network or connected via VPN.

## CPU and Memory Availability

Most work on Aoraki asks for cores and memory rather than for a GPU, so start here: how many
cores are free in each partition, and how full each partition is as a share of its total.

<iframe class="grafana-panel" loading="lazy" title="Free CPU cores by partition" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=110&hideLogo=true"></iframe>

<iframe class="grafana-panel grafana-panel--tall" loading="lazy" title="How full each partition is" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-6h&to=now&refresh=1m&theme=light&panelId=111&hideLogo=true"></iframe>

Cores are not usually what a job waits on, though. Memory often is:

<iframe class="grafana-panel" loading="lazy" title="Cluster memory allocated" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=131&hideLogo=true"></iframe>

If this sits near the top while cores are still free, the cluster is memory-bound, and asking
for less memory per job is the fastest route to starting sooner. [Job Efficiency](running/efficiency.md)
covers how to find out what your jobs actually used.

## How Long Jobs Are Waiting

Free capacity tells you what the cluster looks like at this instant; how long jobs have
actually taken to start tells you what to expect. This is the number worth checking before you
submit, and the GPU partitions are where it varies most.

<iframe class="grafana-panel grafana-panel--tall" loading="lazy" title="Typical wait on each GPU partition over the last 24 hours" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-24h&to=now&refresh=1m&theme=light&panelId=102&hideLogo=true"></iframe>

!!! example "Why this is worth a look"

    In the week to 11 August 2026, the median job on `aoraki_gpu_A100_80GB` waited **13 hours**
    before it started. Over the same week the median job on `aoraki_gpu_L4_24GB`,
    `aoraki_gpu_H200` and `aoraki_gpu_RTX6000` started in **under half a minute**.

    Those numbers move around, which is exactly why the graph is here rather than a table. But
    the pattern is persistent: the A100 partitions are the most heavily contended on Aoraki,
    and a job that does not specifically need an A100 will usually start far sooner somewhere
    else.

The same measure over the last week, across every partition rather than only the GPU ones, as a
median and as the slow end of the distribution:

<div class="grafana-pair" markdown>
<iframe class="grafana-panel" loading="lazy" title="Median wait before starting, by partition" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=100&hideLogo=true"></iframe>
<iframe class="grafana-panel" loading="lazy" title="Ninetieth percentile wait before starting, by partition" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=101&hideLogo=true"></iframe>
</div>

Read them together. The median is the typical experience; the p90 is what one job in ten runs
into. A partition where the two are close is predictable. A partition with a low median and a
high p90 is usually quick but occasionally very slow, which matters if you have a deadline.

How many jobs are queued is a different signal again — a partition can have a short wait and a
long queue if it is turning work over quickly:

<iframe class="grafana-panel" loading="lazy" title="Jobs waiting by partition" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=130&hideLogo=true"></iframe>

If your own job is already queued and you want to know why it specifically has not started,
that is a different question — see
[Why Is My Job Not Starting?](../general/faq/job_start_time.md).

## GPU Availability and Utilisation

<iframe class="grafana-panel" loading="lazy" title="GPUs free now, by type" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-6h&to=now&refresh=1m&theme=light&panelId=120&hideLogo=true"></iframe>

A GPU is counted as free only if it is neither allocated to a job nor sitting on a node that is
down, drained or reserved. Those last ones are broken out separately, because a hardware fault
that takes a node out of service is not the same thing as demand:

<div class="grafana-pair" markdown>
<iframe class="grafana-panel" loading="lazy" title="GPUs in use over time, by type" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=122&hideLogo=true"></iframe>
<iframe class="grafana-panel" loading="lazy" title="GPUs offline over time, by type" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=123&hideLogo=true"></iframe>
</div>

Whether a GPU is *allocated* and whether it is *working* are different questions. The panels
above answer the first. These answer the second — how hard each model has actually been
computing, averaged over the last day and across every GPU of that model:

<iframe class="grafana-panel" loading="lazy" title="GPU utilisation by model, 24 hour average" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=121&hideLogo=true"></iframe>

A model sitting low here is not necessarily one you can have — it may be fully allocated to
jobs that are between GPU-heavy steps. Read it alongside *GPUs free now*, above.

<iframe class="grafana-panel" loading="lazy" title="GPU utilisation trend, by model" src="https://research-monitoring.otago.ac.nz/d-solo/aoraki-queue/aoraki-queue-and-availability?orgId=1&from=now-7d&to=now&refresh=1m&theme=light&panelId=124&hideLogo=true"></iframe>

The trend is a one hour moving average. Raw GPU utilisation is sampled every five seconds and
swings between 0 and 100%, so the unsmoothed version of this graph is unreadable with eleven
models on it — and its "last value" is a coin toss rather than a summary.

Models with only a handful of GPUs move a long way on a single job: the cluster has sixteen
RTX PRO 6000s but only four H100 NVLs, and both get one line here.

For per-node detail rather than an average per model, see
[Current Utilisation](current_utilisation.md).

## How to Read These Graphs

**Allocated is not the same as busy.** A GPU held by a job that is loading data, waiting on the
filesystem or sitting at an idle interactive prompt shows near-zero utilisation while remaining
completely unavailable to everyone else. If you are asking *can I get a GPU*, look at what is
free. If you are asking *am I using mine well*, look at utilisation — and at
[Job Efficiency](running/efficiency.md).

**Waiting time is measured from when your job became eligible, not when you submitted it.** A
job held back by `--begin` or by a dependency on another job has not been waiting on the
cluster, and counting that time here would make Aoraki look slower than it is.

**Do not add partitions together.** A node belongs to several partitions at once — `aoraki11`
is in `aoraki_short`, `aoraki_gpu` and `aoraki_gpu_A100_80GB` simultaneously — so summing the
per-partition figures counts the same hardware more than once. Compare partitions side by side
instead.

**An array counts once, not once per task.** Most of the work on the CPU partitions arrives as
array submissions of several thousand tasks, and every task in an array shares the array's
eligible time — so task 900 looks like it waited for however long tasks 1 to 899 took to work
through, even though what held it back was the submitter's own limit on concurrent jobs. These
graphs therefore record each array once, as the wait of its first task to start. That is the
figure that answers *if I submit now, when do I start*; it is not how long the last task of a
large array will take to come round.

**The GPU counts here and on Current Utilisation do not match, on purpose.** Slurm manages 57
GPUs across the cluster partitions. The monitoring agents report 67, because several hosts
outside those partitions also run GPUs — the utilisation graphs above exclude the standalone
workstations and cover the 62 GPUs on the cluster's compute nodes. This page counts what
Slurm can allocate to you.

## If Something Looks Wrong

If a partition shows no data at all, or a node has been drained for longer than you would
expect, email the eResearch Support team at **{{ support_email }}** — a persistent gap here
usually means a node or an exporter needs attention rather than that the cluster is quiet.

!!! related-pages "What's next?"
    - [Why Is My Job Not Starting?](../general/faq/job_start_time.md) for a job that is already queued
    - [Current Utilisation](current_utilisation.md) for per-node GPU detail
    - [Cluster Overview](overview.md#partition-limits) for the partitions and their limits
    - [GPU Jobs](../general/faq/gpu_jobs.md) for asking for a GPU correctly
    - [Job Efficiency](running/efficiency.md) for whether you are using what you asked for
