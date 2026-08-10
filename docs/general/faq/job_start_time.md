# Why Is My Job Not Starting?

!!! overview "On this Page"
    - Finding your job in the queue and reading its state
    - What each pending reason means, and what to do about it
    - Getting an estimated start time
    - Making your next job start sooner

A job that is not running is not necessarily stuck. Slurm holds it until a node with the
resources you asked for is free, and until it is your job's turn. The queue tells you which
of those two is happening.

## Where Is My Job?

!!! terminal

    ```bash
    squeue --me
    ```

    ```output
    JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
    669120    aoraki  analysis  abcde01  R    1:12:33      1 aoraki07
    669121 aoraki_gpu    train  abcde01 PD       0:00      1 (Priority)
    ```

Two columns matter:

- **`ST`** — the state. `R` is running, `PD` is pending, `CG` is completing.
- **`NODELIST(REASON)`** — for a running job, the node it is on. For a pending job, the
  reason it is not running yet, in brackets.

## What Does the Reason in Brackets Mean?

Table: Pending reasons you are likely to see on Aoraki

| Reason | What it means | What to do |
| :-- | :-- | :-- |
| `(Priority)` | Other jobs are ahead of yours | Wait, or ask for less so backfill can slot you in |
| `(Resources)` | Your job is next, but no node has enough free right now | Wait — it will start as jobs ahead of it finish |
| `(QOSMaxJobsPerUserLimit)` | You are already running the maximum number of jobs allowed in that partition. On GPU partitions that is **2** | Wait for one to finish, or cancel an idle session |
| `(QOSMaxGRESPerUser)` | You already hold the maximum GPUs allowed | As above |
| `(AssocMaxJobsLimit)` | An account-wide job limit is in force | Wait, or email {{ support_email }} |
| `(Dependency)` | The job it depends on has not finished yet | Nothing — unless the other job failed, in which case cancel this one |
| `(DependencyNeverSatisfied)` | The job it depended on failed or was cancelled, so this one will never run | `scancel` it and resubmit |
| `(ReqNodeNotAvail)` | A node you asked for is down, draining or reserved — often ahead of scheduled maintenance | Drop the explicit node request, or wait for the maintenance window to pass |
| `(PartitionTimeLimit)` | Your `--time` is longer than the partition allows | Reduce `--time`, or use `aoraki_long` |
| `(PartitionConfig)` | Your request cannot be satisfied by any node in that partition — usually too many cores or too much memory | Reduce the request, or choose a partition that has nodes that size |
| `(JobHeldUser)` / `(JobHeldAdmin)` | The job is held. You can release your own with `scontrol release <jobid>` | Release it, or contact {{ support_email }} for an admin hold |
| `(BeginTime)` | You asked for it to start later with `--begin` | Nothing |

The current partition limits are in the [Cluster Overview](../../getting_started/overview.md#partition-limits).

## When Will My Job Start?

!!! terminal

    ```bash
    squeue --me --start
    ```

This adds a `START_TIME` column with Slurm's estimate. `scontrol` shows the same thing for
one job, along with everything else Slurm knows about it:

!!! terminal

    ```bash
    scontrol show job <jobid>
    ```

!!! warning "The estimate moves"
    It is a projection based on the jobs currently queued, and it assumes every one of them
    runs for its full requested wall time. Most finish early, so jobs usually start sooner
    than the estimate. New submissions and higher-priority work can push it the other way.
    Treat it as a rough guide, not a booking.

## How Do I Make My Job Start Sooner?

In order of how much difference it makes:

1. **Ask for less time.** Slurm backfills short jobs into gaps in the schedule, so a job
   asking for 2 hours has far more places to fit than the same job asking for 3 days. This
   is the single most effective change — see
   [Why Asking for Less Starts Sooner](../../getting_started/running/running_jobs_overview.md#why-asking-for-less-starts-sooner).
2. **Ask for less memory and fewer cores.** Both make the gap your job needs smaller. Use
   [`seff`](../../getting_started/running/efficiency.md) on a previous run to find out what
   it really needed.
3. **Use a different partition.** If your work does not need the general-purpose nodes,
   `aoraki_short` and `aoraki_small` use cores that would otherwise sit idle on the GPU
   nodes, and are often much quicker to start.
4. **Do not name a specific node** with `--nodelist` unless you genuinely need it. You are
   then waiting for one machine instead of dozens.

## How Busy Is the Cluster?

!!! terminal

    ```bash
    sinfo -o "%20P %5D %14F %10m %11l"
    ```

    ```output
    PARTITION            NODES NODES(A/I/O/T) MEMORY     TIMELIMIT
    aoraki*              27    23/4/0/27      1030000+   7-00:00:00
    aoraki_bigcpu        10    8/2/0/10       1500000    14-00:00:00
    aoraki_gpu           10    10/0/0/10      770000+    7-00:00:00
    ```

The `NODES(A/I/O/T)` column is **A**llocated / **I**dle / **O**ther / **T**otal. A partition
showing `10/0/0/10` has nothing free.

To see which GPUs each node has, and how many are already taken:

!!! terminal

    ```bash
    sinfo -p aoraki_gpu -o "%20P %10N %20G %30C"
    ```

[Current Utilisation](../../getting_started/current_utilisation.md) shows the same picture
as graphs over the last week, which is a better guide to when the cluster is usually quiet.

## Why Did a Job I Submitted Later Start First?

Two mechanisms, both working as intended:

- **Backfill.** While Slurm holds nodes free for a large job at the front of the queue, it
  looks down the queue for smaller jobs that can start *and finish* before the large job is
  due to begin. A short job jumps ahead because it fits in the gap.
- **Fairshare.** Priority takes account of how much of the cluster you and your group have
  used recently. Heavy recent use lowers your priority relative to someone who has been idle.

## Can I Ask for More Than a Partition Allows?

No. Aoraki enforces partition limits at submission, so a request over the limit is either
rejected immediately by `sbatch` or sits pending with `(PartitionConfig)` or
`(PartitionTimeLimit)` and never runs.

Check your request against the [partition limits](../../getting_started/overview.md#partition-limits) before
submitting. If your work genuinely needs more than a partition allows, email
{{ support_email }} — limits can be raised for a specific piece of work.

!!! related-pages "What's next?"
    - For how the scheduler decides, see [Running Jobs](../../getting_started/running/running_jobs_overview.md)
    - To adjust what you request, see [Job Script Options](../../getting_started/running/batch/sbatch_options.md)
    - To find out what your last job actually needed, see [Job Efficiency](../../getting_started/running/efficiency.md)
    - If the job started and then failed, see [Why Did My Job Fail?](slurm_job_failures.md)
    - For GPU-specific queuing, see [GPU Questions](gpu_jobs.md)
