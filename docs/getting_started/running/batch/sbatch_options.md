# Job Script Options

!!! overview "On this Page"
    - How `#SBATCH` lines work, and how command-line options interact with them
    - The options you are most likely to need, with their Aoraki defaults
    - Requesting memory correctly
    - Requesting cores, tasks and nodes for parallel work
    - Output files, email notification and job dependencies

This page is the reference for what you can put in a job script. If you have not submitted a job before, start with the [Slurm Quickstart](slurm_quickstart.md).

## How `#SBATCH` Lines Work

A job script is an ordinary bash script. The lines beginning `#SBATCH` are comments as far as bash is concerned, but Slurm reads them as your resource request:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=analysis
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=32G
    #SBATCH --time=04:00:00

    module load R
    Rscript analysis.R
    ```

Two rules:

- **They must appear before the first command.** Slurm stops reading `#SBATCH` lines as soon as it hits a real line of script, so anything below your first `module load` or `echo` is silently ignored.
- **The command line overrides the script.** `sbatch --time=08:00:00 my_job.sh` runs with an 8-hour limit whatever the script says. This is useful for re-running something with a different size without editing the file.

The same options work as flags to [`srun` and `salloc`](../interactive/interactive_shell.md) for interactive sessions.

## The Options You Will Actually Use

Table: Common `sbatch` options and what they default to on Aoraki

| Option | Short | Default on Aoraki | What it does |
| :-- | :-- | :-- | :-- |
| `--job-name=` | `-J` | the script's filename | A name you will recognise in `squeue` |
| `--partition=` | `-p` | `aoraki` | Which group of nodes to run on |
| `--time=` | `-t` | 8 hours (1 h on `aoraki_short`, 24 h on `aoraki_long`) | Wall time limit. The job is killed when it runs out |
| `--cpus-per-task=` | `-c` | 1 | Cores for each task |
| `--mem=` | | 2 GB per allocated core | Memory for the job on each node |
| `--mem-per-cpu=` | | | Memory per core instead of a total |
| `--ntasks=` | `-n` | 1 | Number of tasks (processes) |
| `--nodes=` | `-N` | 1 | Number of nodes |
| `--output=` | `-o` | `slurm-%j.out` | Where standard output goes |
| `--error=` | `-e` | merged into `--output` | Where errors go |
| `--chdir=` | `-D` | where you ran `sbatch` | Directory to start in |
| `--array=` | `-a` | | Run the script over a range of indices |
| `--dependency=` | `-d` | | Wait for another job first |
| `--mail-type=` | | | When to email you |
| `--mail-user=` | | | Where to email you |
| `--gpus-per-node=` | | | GPUs per node, alongside a GPU partition |

The complete list is in the [Slurm `sbatch` documentation](https://slurm.schedmd.com/sbatch.html).

!!! note "`--account` is not needed"
    Every Aoraki user has a default account, and every partition accepts it. If a script you copied from another cluster's documentation has `#SBATCH --account=...`, delete the line.

### Time Formats

`--time` accepts several forms. The two worth remembering are `hh:mm:ss` and `days-hh:mm:ss`:

| You write | You get |
| :-- | :-- |
| `--time=30` | 30 minutes |
| `--time=04:00:00` | 4 hours |
| `--time=2-00:00:00` | 2 days |
| `--time=1-12:30:00` | 1 day, 12 hours, 30 minutes |

You cannot ask for more than the partition's maximum — the job is rejected at submission. Maximum wall times per partition are in the [Cluster Overview](../../overview.md).

## Memory

Memory is allocated to your job the same way cores are, and it is a hard limit: a job that tries to use more than it asked for is killed with `OUT_OF_MEMORY`.

**If you do not ask, you get 2 GB per allocated core.** So `--cpus-per-task=8` with no memory option gives your job 16 GB. That is often enough; when it is not, ask explicitly.

There are two ways to ask, and you should use one or the other, not both:

| Option | Meaning | Use when |
| :-- | :-- | :-- |
| `--mem=64G` | 64 GB total, per node | Almost always — it is the easiest to reason about |
| `--mem-per-cpu=4G` | 4 GB for each core, so 8 cores gives 32 GB | The memory your job needs scales with the number of cores |

Specify units — `G` for GB, `M` for MB. `--mem=4` means 4 **megabytes**, which is a common and confusing mistake.

!!! warning "Over-requesting memory is not free"
    Nodes are shared, and Slurm treats memory as a consumable resource. If you reserve 500 GB and use 10 GB, the other 490 GB cannot be given to anyone else, and cores on that node sit idle because no job can fit alongside yours. Use [`seff`](../efficiency.md) after a job to find the right number.

!!! note "Options that do not exist"
    `--mem-per-task` and `--mem-per-node` are not Slurm options, though they appear in some documentation. The real ones are `--mem`, `--mem-per-cpu` and `--mem-per-gpu`.

## Cores, Tasks and Nodes

Slurm distinguishes between **tasks** (separate processes) and **cores** (CPUs given to each of those processes). Which one you want depends entirely on how your software parallelises.

| Option | Meaning |
| :-- | :-- |
| `--nodes` / `-N` | How many nodes to spread across |
| `--ntasks-per-node` | How many processes to start on each node |
| `--ntasks` / `-n` | Total processes, letting Slurm choose the layout |
| `--cpus-per-task` / `-c` | Cores available to each process |

The rule of thumb:

- **Threaded software on one machine** — OpenMP, R's `parallel`, Python's `multiprocessing`, most bioinformatics tools with a `--threads` option. Use `--nodes=1 --ntasks=1 --cpus-per-task=N`. This is the common case.
- **MPI software** — use `--ntasks=N` (optionally with `--nodes`), and leave `--cpus-per-task=1` unless each rank is itself threaded.
- **Many independent runs** — do not use tasks at all. Use an [array job](slurm_examples/array-slurm.md).

An example of the threaded case, requesting 16 cores on one node:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=threaded
    #SBATCH --partition=aoraki
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=16
    #SBATCH --mem=32G
    #SBATCH --time=02:00:00

    # Tell the software how many cores it has
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    ./my_program --threads $SLURM_CPUS_PER_TASK
    ```

!!! tip "Tell your software what it was given"
    Slurm allocates the cores but does not make your program use them. Read `$SLURM_CPUS_PER_TASK` and pass it on, as above — that way changing the `#SBATCH` line is enough, and the two can never disagree.

!!! warning "More cores is not always faster"
    Very few programs scale linearly. A job asking for 64 cores and using 4 waits longer to start *and* finishes no sooner. Test at a couple of sizes and compare, then request what actually helps.

<<<<<<< HEAD
Note that GPU jobs and OnDemand sessions are limited to a **single node**, and each partition caps the cores a single job may request — see the [Cluster Overview](../../../getting_started/overview.md).
=======
Note that GPU jobs and OnDemand sessions are limited to a **single node**, and each partition caps the cores a single job may request — see the [Cluster Overview](../../overview.md).
>>>>>>> bee4f213358f539a530dcc7d94b8a392cfc04f9a

## Output and Errors

By default everything your script prints, both normal output and errors, is combined into `slurm-<jobid>.out` in the directory you submitted from.

To change that, use `--output` and `--error` with these placeholders:

| Placeholder | Becomes |
| :-- | :-- |
| `%j` | The job ID |
| `%x` | The job name |
| `%A` | The array job's ID |
| `%a` | The array task index |

!!! terminal

    ```bash
    #SBATCH --output=logs/%x-%j.out
    #SBATCH --error=logs/%x-%j.err
    ```

!!! warning "The directory must already exist"
    Slurm will not create `logs/` for you. If the directory is missing the job fails immediately with no output to tell you why.

## Email Notification

!!! terminal

    ```bash
    #SBATCH --mail-user=your.name@otago.ac.nz
    #SBATCH --mail-type=END,FAIL
    ```

`--mail-type` accepts `BEGIN`, `END`, `FAIL`, `TIME_LIMIT`, `ALL`, and `ARRAY_TASKS`. `END,FAIL` is the useful combination for most work.

!!! warning "Not with array jobs"
    Adding `ARRAY_TASKS` to a 500-task array sends you 500 emails. Leave it off unless you have a specific reason.

## Job Dependencies

`--dependency` holds a job in the queue until another one reaches a particular state:

!!! terminal

    ```bash
    sbatch --dependency=afterok:12345 second_stage.sh
    ```

| Condition | Starts when the first job |
| :-- | :-- |
| `afterok:<jobid>` | finished successfully |
| `afterany:<jobid>` | finished, successfully or not |
| `afternotok:<jobid>` | failed |
| `singleton` | any earlier job of yours with the same name has finished |

See [Dependent Jobs](slurm_examples/dependent_jobs.md) for chaining several stages together.

## Array Jobs

`--array` runs the same script many times with a different index each time, which is the right way to process many inputs:

!!! terminal

    ```bash
    #SBATCH --array=1-100%10
    ```

That submits 100 tasks and lets at most 10 run at once. Each task sees its own index in `$SLURM_ARRAY_TASK_ID`. Arrays may have up to 100,000 tasks.

!!! tip "Always throttle with `%N`"
    Without the `%10`, all 100 tasks compete for resources at once. Throttling keeps the queue usable for everyone and rarely makes your work finish later. See [Reasonable Usage](../../../general/guidelines/reasonable_usage.md).

Worked examples are on the [Array Jobs](slurm_examples/array-slurm.md) page.

## GPUs

A GPU job needs both a GPU partition and a request for the GPU itself:

!!! terminal

    ```bash
    #SBATCH --partition=aoraki_gpu_A100_40GB
    #SBATCH --gpus-per-node=1
    #SBATCH --cpus-per-task=8
    ```

The partition determines which GPU model you can get. Which one to choose, how to request a specific model, and how many cores to pair with a GPU are covered on the [GPU Jobs](slurm_examples/gpu-slurm.md) page.

## Useful Environment Variables

Inside a running job, Slurm sets variables describing what you were actually given. Read these rather than hard-coding numbers:

| Variable | Contains |
| :-- | :-- |
| `SLURM_JOB_ID` | This job's ID |
| `SLURM_JOB_NAME` | The job name |
| `SLURM_CPUS_PER_TASK` | Cores allocated to each task |
| `SLURM_NTASKS` | Number of tasks |
| `SLURM_ARRAY_TASK_ID` | This task's index, in an array job |
| `SLURM_SUBMIT_DIR` | The directory you ran `sbatch` from |

!!! note "Temporary files"
    Each job gets its own private `/tmp`, `/var/tmp` and `/dev/shm`, isolated from every other job on the node and deleted when the job ends. Write scratch files there freely, but copy anything you want to keep back to `/projects` or `/weka` before the job finishes.

!!! related-pages "What's next?"
    - To submit your first job, see the [Slurm Quickstart](slurm_quickstart.md)
    - To check whether your request matched what the job used, see [Job Efficiency](../efficiency.md)
    - For worked scripts, see [Array Jobs](slurm_examples/array-slurm.md), [GPU Jobs](slurm_examples/gpu-slurm.md), [R Jobs](slurm_examples/r-slurm.md) and [Dependent Jobs](slurm_examples/dependent_jobs.md)
<<<<<<< HEAD
    - For partitions, hardware and per-job limits, see the [Cluster Overview](../../../getting_started/overview.md)
=======
    - For partitions, hardware and per-job limits, see the [Cluster Overview](../../overview.md)
>>>>>>> bee4f213358f539a530dcc7d94b8a392cfc04f9a
    - The complete option reference is at [slurm.schedmd.com/sbatch.html](https://slurm.schedmd.com/sbatch.html)
