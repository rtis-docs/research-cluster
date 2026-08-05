# Why Did My Job Fail?

!!! overview "On this Page"
    - Finding your job's output and working out how it ended
    - The four failures that account for most of them: memory, time, environment, paths
    - Stopping a job, and what you can and cannot change after submitting
    - What to send when you ask for help

When a job does not do what you expected, work through it in this order: **where the output
went**, **how Slurm says the job ended**, and then **what the output actually says**.

## Where Did the Output Go?

Unless you said otherwise, Slurm writes everything your job printed — both standard output
and standard error — to `slurm-<jobid>.out` in the directory you ran `sbatch` from.

!!! terminal

    ```bash
    cat slurm-669120.out
    ```

Nine times out of ten the real error message is in there. To send output somewhere else, or
to split errors into their own file, see
[Output and Errors](../../getting_started/running/batch/sbatch_options.md#output-and-errors).

## How Did My Job End?

`sacct` reports Slurm's view of the job, which tells you whether the job failed or was
*killed*, and those need different fixes.

!!! terminal

    ```bash
    sacct -j <jobid> --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS
    ```

Table: The job states you are most likely to see

| State | What happened | Where to go |
| :-- | :-- | :-- |
| `COMPLETED` | The script exited cleanly with status 0 | If the results are wrong, the problem is in your code, not in Slurm |
| `FAILED` | The script exited with a non-zero status | Read `slurm-<jobid>.out` |
| `OUT_OF_MEMORY` | The job used more memory than it requested | [Below](#my-job-says-out_of_memory) |
| `TIMEOUT` | The job hit its wall time | [Below](#my-job-says-timeout-can-i-extend-it) |
| `CANCELLED` | Stopped by you, an administrator, or the scheduler | [Below](#my-job-says-cancelled-and-i-did-not-cancel-it) |
| `NODE_FAIL` | The node the job was on failed | Resubmit. If it keeps happening, tell us the node name |

!!! note "`COMPLETED` does not mean correct"
    Slurm only knows the exit status of your script. A pipeline whose last command succeeds
    reports `COMPLETED` even if a step in the middle failed. Adding `set -euo pipefail` near
    the top of a bash job script makes the job fail when any command in it does.

## My Job Says `OUT_OF_MEMORY`

Your job asked for a certain amount of memory and tried to use more, so Slurm killed it.
The output file often ends abruptly, or with a message about a killed process.

If you did not set `--mem` or `--mem-per-cpu`, your job got **2 GB per allocated core** —
so a single-core job had 2 GB, and a four-core job had 8 GB. That default is the usual cause.

To find out how much it really needed, look at a run that *did* finish:

!!! terminal

    ```bash
    seff <jobid>
    ```

Take the peak memory, add about 20% headroom, and set `--mem` to that. If nothing has ever
finished, double the request and try again. See
[Job Efficiency](../../getting_started/running/efficiency.md) for reading the numbers, and
[Memory](../../getting_started/running/batch/sbatch_options.md#memory) for the difference
between `--mem` and `--mem-per-cpu`.

## My Job Says `TIMEOUT`. Can I Extend It?

Not yourself. When a job reaches the wall time you requested, Slurm sends it `SIGTERM` and
then `SIGKILL`, and anything not already written to disk is lost.

What to do instead:

- **Checkpoint.** Write partial results or state to disk as you go, so a job that is cut
  short can be resumed rather than restarted. Most long-running scientific software has an
  option for this.
- **Resubmit with more time**, up to the [partition's limit](../overview.md#partition-limits).
  `aoraki_long` allows 30 days.
- **Ask early, not late.** An administrator can sometimes extend a job that is *still
  running*, if the resources are available and it does not disrupt other work. Email
  {{ support_email }} **before** the job hits its limit — once it has been killed, nothing
  can be recovered.

## Why Does My Job Say "command not found"?

A batch job does not inherit the modules and environments you loaded in your shell. Any
`module load`, `conda activate` or `source` you rely on has to be in the job script itself.
See [Software and Environments](software.md#why-does-my-batch-job-say-command-not-found-when-it-works-when-i-type-it).

## My Job Ran but I Cannot Find Its Output Files

A job starts in the directory you submitted it from, not in your home directory. If your
script writes to a relative path, the files are relative to *that* directory.

Two things make this easier to reason about:

- Use absolute paths for input and output, or
- Start the script with `cd $SLURM_SUBMIT_DIR` so it is explicit.

Note that anything your job wrote to `/tmp` is **gone** — each job gets its own temporary
directory and it is deleted when the job ends. See
[Where do temporary files go during a job?](disk_usage.md#where-do-temporary-files-go-during-a-job).

## My Job Says `CANCELLED` and I Did Not Cancel It

`sacct` shows who did it — give the `State` column enough width or the name is truncated:

!!! terminal

    ```bash
    sacct -j <jobid> --format=JobID,State%30,ExitCode,Elapsed
    ```

A state of `CANCELLED by <uid>` names the user or administrator responsible. Common causes
are a job cancelled during a maintenance window, a job cancelled by an administrator because
it was affecting a node, or your own `scancel` from another terminal. Check the
**Announcements** section for planned maintenance, and email {{ support_email }} if none of
those fits.

## How Do I Stop a Job?

!!! terminal

    ```bash
    scancel <jobid>              # one job
    scancel -u $USER             # everything you have queued or running
    scancel -t PENDING -u $USER  # only the ones that have not started
    scancel --name=my_job        # everything with a given --job-name
    ```

Job IDs come from `squeue --me`. Cancelling an array job by its base ID cancels every task
in it; add `_3` to cancel just one task.

## Can I Change a Job After I Have Submitted It?

**While it is pending**, some things can be adjusted:

!!! terminal

    ```bash
    scontrol update jobid=<jobid> TimeLimit=04:00:00
    scontrol update jobid=<jobid> Partition=aoraki_short
    ```

You can only *reduce* a time limit, and any change still has to fit the partition's limits.

**Once it is running**, you cannot change what it was allocated. Cancel it and resubmit.

## What Should I Send When I Ask for Help?

Email {{ support_email }} with:

- The **job ID** — that alone lets us see the accounting record, the node, and how it ended
- The **job script**, and the command you used to submit it
- The **error output**, copied as text rather than a screenshot
- What you expected to happen

The [Support](../support.md) page has the full list, including how to put together a small
test case for problems that are harder to pin down.

!!! related-pages "What's next?"
    - If the job never started at all, see [Why Is My Job Not Starting?](job_start_time.md)
    - To right-size your next request, see [Job Efficiency](../../getting_started/running/efficiency.md)
    - For the options themselves, see [Job Script Options](../../getting_started/running/batch/sbatch_options.md)
    - For module and environment problems, see [Software and Environments](software.md)
    - For GPU-specific problems, see [GPU Questions](gpu_jobs.md)
