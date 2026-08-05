# Job Efficiency

!!! overview "On this Page"
    - Why the size of your request matters to you and to everyone else
    - Checking what a finished job actually used, with `seff`
    - How to read the CPU and memory efficiency numbers
    - What is different about interactive and OnDemand sessions
    - Using the result to size your next job

Every job reserves the cores and memory it asked for, for as long as it asked for them — whether or not it uses them. A job that requests 64 GB and uses 4 GB has taken 60 GB out of the cluster for nothing, and because Slurm allocates memory as well as cores, it may have left cores on that node idle because no other job could fit alongside it.

This works against you as well. A large request has to wait for a large gap in the schedule, so an over-sized job starts later than a right-sized one doing exactly the same work. Slurm [backfills](running_jobs_overview.md#why-asking-for-less-starts-sooner) short, small jobs into gaps, and your job can only benefit from that if it is honest about what it needs.

The fix is a short loop: run something, look at what it used, size the next one from that.

## 1. Run the Job

Submit as usual with [`sbatch`](batch/slurm_quickstart.md), and note the job ID it returns:

!!! terminal

    ```bash
    sbatch my_job_script.sh
    ```

For a session launched from OnDemand, the job ID is on the session card under **My Interactive Sessions**.

If you are sizing an unfamiliar workload, start with a deliberately small test — a fraction of the input, a short wall time — rather than guessing at the full run.

## 2. Watch It While It Runs

!!! terminal

    ```bash
    squeue --me
    ```

The `ST` column shows `R` for running and `PD` for pending; for a pending job, the last column says why. See [Job Queuing](../../general/faq/job_start_time.md) if it is not starting.

## 3. Check How It Finished

Once the job has ended, `sacct` tells you the outcome:

!!! terminal

    ```bash
    sacct -j <jobid> --format=JobID,JobName,Partition,AllocCPUS,State,Elapsed,ExitCode
    ```

Table: The job states you are most likely to see

| State | What happened |
| :-- | :-- |
| `COMPLETED` | Finished normally |
| `FAILED` | Your script exited with an error |
| `OUT_OF_MEMORY` | Used more memory than requested — ask for more |
| `TIMEOUT` | Hit the wall time — ask for more time, or make it faster |
| `CANCELLED` | Stopped by you or by an administrator |

[Slurm Job Management and Troubleshooting](../../general/faq/slurm_job_failures.md) covers each of these in more detail.

## 4. See What It Actually Used

`seff` compares what you asked for against what the job used:

!!! terminal

    ```bash
    seff <jobid>
    ```

    ```output
    Job ID: 123456
    Job Name: my_job
    Partition: aoraki
    User: your_username
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 4
    CPU Utilized: 01:30:00
    CPU Efficiency: 75.00% of 02:00:00 core-walltime
    Memory Utilized: 2.00 GB
    Memory Efficiency: 50.00% of 4.00 GB
    ```

Two numbers matter.

**CPU Efficiency** is the CPU time your job used as a fraction of the core-time it reserved (cores × wall time). The job above held 4 cores for 30 minutes — 2 hours of core-time — and used 1.5 hours of it, so 75%.

**Memory Efficiency** is the peak memory the job reached as a fraction of what it requested. The job above asked for 4 GB and peaked at 2 GB, so 50%.

!!! note "`seff` needs a finished job"
    Run it after the job has ended. For a job that is still running, `sstat -j <jobid>` gives a live view instead.

## 5. Read the Numbers

Table: What each combination is telling you

| CPU efficiency | Memory efficiency | What it means | What to do |
| :-- | :-- | :-- | :-- |
| High (>75%) | High (>50%) | Well sized | Nothing |
| Low | High | You asked for cores the software did not use | Reduce `--cpus-per-task` |
| High | Low | Right on cores, over-provisioned on memory | Reduce `--mem` |
| Low | Low | Over-provisioned on both | Reduce both, and check the job did what you expected |
| — | Close to 100% | The job may have been killed for exceeding memory | Increase `--mem` |

Wall time is worth checking separately: compare `Elapsed` from `sacct` against the `--time` you asked for. Requesting three days for a job that takes forty minutes is the most common reason a job sits in the queue longer than it needs to.

!!! warning "Low CPU efficiency is not always over-requesting"
    A job that spends most of its time reading and writing files can show low CPU efficiency while using exactly the right number of cores. So can a multi-threaded program whose parallel section is short. Work out what the job spends its time doing before you cut cores.

## 6. Size the Next One

- **Memory** — take the peak from `seff` and add roughly 20% headroom. Do not round up to the size of the node.
- **Cores** — if efficiency was low, halve the request and compare. Most software stops scaling well before the core counts people ask for.
- **Wall time** — take the elapsed time and add a margin for a slower node or a larger input. Generous, not extravagant.
- **Re-check** after changing the input, the software or the partition — the right size moves.

[Current Utilisation](../current_utilisation.md) shows what the cluster looks like right now, which is useful context for why a particular request waited.

## Interactive and OnDemand Sessions

Efficiency applies to interactive work too, and interactive sessions are usually where the most capacity goes to waste — they hold their allocation while you read, think, or go to lunch.

What changes is which numbers are meaningful:

- **Ignore CPU efficiency.** It will always be low, because the session spends most of its time waiting for you to type. That is expected, and not something to fix.
- **Watch peak memory.** This is the number to size from. If you used less than about 75% of the memory you requested, ask for less next time.
- **Watch wall time hardest.** A session's real cost is the hours it sat idle. Ask for the length of a working session rather than a whole day, and click **Delete** under **My Interactive Sessions** when you finish rather than leaving it to expire.

`seff <jobid>` works the same way for OnDemand sessions — take the job ID from the session card.

!!! related-pages "What's next?"
    - For how jobs and the scheduler work, see [Running Jobs](running_jobs_overview.md)
    - To adjust your request, see [Job Script Options](batch/sbatch_options.md)
    - For sizing an interactive session, see [Interactive Jobs](interactive/interactive.md)
    - If a job failed, see [Slurm Troubleshooting](../../general/faq/slurm_job_failures.md)
    - For what a fair share of the cluster looks like, see [Reasonable Usage](../../general/guidelines/reasonable_usage.md)
