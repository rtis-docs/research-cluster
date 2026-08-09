# Interactive Sessions from the Command Line

!!! overview "On this Page"
    - Getting a shell on a compute node with `srun --pty`
    - Holding an allocation across several commands with `salloc`
    - Which of the two to use
    - Running graphical software, and asking for a GPU
    - Keeping a session alive when your connection drops

When you connect to the cluster over [SSH](../../access/login_ssh.md) or through the [OnDemand shell](../../software/OnDemand/ood_shell.md) you land on the **login node**. That node is shared by everyone and is meant for editing files, moving data and submitting work — not for running your analysis.

To do actual work in a terminal you need a shell on a **compute node**, and you get one by asking Slurm for it. There are two commands for this: `srun --pty` and `salloc`.

## `srun --pty`: A Shell on a Compute Node

`srun --pty` submits a job whose only job step is an interactive shell, and connects your terminal to it.

!!! terminal

    ```bash
    srun --partition=aoraki --cpus-per-task=4 --mem=16G --time=02:00:00 --pty bash
    ```

Your request queues like any other job. Once it starts, the prompt changes to show you are on a compute node:

!!! terminal

    ```output
    srun: job 669120 queued and waiting for resources
    srun: job 669120 has been allocated resources
    [user@aoraki13 ~]$
    ```

From here you are on `aoraki13`, with the 4 cores and 16 GB you asked for. Load modules, run your software, and type `exit` when you are finished — that ends the job and releases the resources.

If you leave out `--partition`, `--time` or `--mem` you get the [defaults](../running_jobs_overview.md#what-you-get-by-default): the `aoraki` partition, an 8-hour limit and 2 GB per core. The defaults are fine for a quick look; set them deliberately for anything else.

!!! tip "Ask for a short wall time"
    Slurm backfills short jobs into gaps in the schedule, so `--time=01:00:00` will usually start noticeably sooner than `--time=08:00:00`. You can always start another session.

## `salloc`: Holding an Allocation

`salloc` reserves resources and hands them to you, rather than wrapping a single command.

!!! terminal

    ```bash
    salloc --partition=aoraki --cpus-per-task=8 --mem=32G --time=02:00:00
    ```

On Aoraki, `salloc` puts you straight onto the first allocated node with a shell, so the immediate experience is much like `srun --pty`:

!!! terminal

    ```output
    salloc: Granted job allocation 669135
    salloc: Nodes aoraki07 are ready for job
    [user@aoraki07 ~]$
    ```

The difference is what the shell *is*. With `srun --pty` your shell is the job step, so the allocation is already in use. With `salloc` the allocation is held open, and every `srun` you run inside it launches a new step across the full allocation:

!!! terminal

    ```bash
    # inside the salloc session
    srun --ntasks=4 ./my_mpi_program
    srun hostname
    ```

Type `exit` to release the allocation. Until you do, it is yours — and it is charged to you — even if you are doing nothing.

### Which One Should You Use?

Table: Choosing between the two commands

| | `srun --pty` | `salloc` |
| :-- | :-- | :-- |
| Best for | one interactive shell, one thing to do | a sequence of steps, or launching parallel tasks by hand |
| Multi-node or MPI work | awkward | the right tool |
| Ends when | you exit the shell | you exit the allocation |

For everyday use — compiling something, testing a command, running a short interactive tool — `srun --pty` is simpler and is what most people want. Reach for `salloc` when you want to run several `srun` steps against one reservation, or when you are testing an MPI program before putting it in a batch script.

## Common Options

Everything you can put in a batch script works here too, as a command-line flag. See [Job Script Options](../batch/sbatch_options.md) for the full set.

| Option | Effect |
| :-- | :-- |
| `--partition=` | Which group of nodes to run on. Defaults to `aoraki`. |
| `--time=hh:mm:ss` | Wall time. Your session ends when this runs out. |
| `--cpus-per-task=` | Cores. Defaults to 1. |
| `--mem=` / `--mem-per-cpu=` | Memory. Defaults to 2 GB per core. |
| `--x11` | Forward graphical windows back to your machine. |
| `--gpus-per-node=` | Request GPUs, alongside a GPU partition. |
| `--job-name=` | A name you will recognise in `squeue`. |

### Graphical Software

X11 forwarding is enabled on the cluster, so a graphical application can display on your own machine. Connect with `ssh -X` (or `ssh -Y`) and add `--x11` to the session:

!!! terminal

    ```bash
    ssh -X aoraki-login.otago.ac.nz
    srun --partition=aoraki --cpus-per-task=4 --mem=16G --time=01:00:00 --x11 --pty bash
    ```

It works, but it is sensitive to network latency and awkward over a home connection. For anything more than a quick plot window, the [HPC Desktop](../../software/OnDemand/hpc_desktop.md) in OnDemand is a much better experience.

### GPU Sessions

To get a GPU you need a GPU partition *and* a request for the GPU itself:

!!! terminal

    ```bash
    srun --partition=aoraki_gpu_A100_40GB \
         --gpus-per-node=1 \
         --cpus-per-task=8 \
         --mem=32G \
         --time=01:00:00 \
         --pty bash
    ```

Check the GPU is visible before you start work:

!!! terminal

    ```bash
    nvidia-smi
    ```

Which partition to pick, and how to request a particular GPU model, is covered in [GPU Jobs](../batch/slurm_examples/gpu-slurm.md). Note that GPU jobs are limited to a single node, and you can have at most **2 running GPU jobs per GPU partition** — an idle interactive GPU session uses one of those two slots, so end it when you stop working.

## Limits Worth Knowing

- **Your session ends when the wall time runs out**, with no warning and no chance to save. Ask for enough, and save your work as you go.
- **A session dies if your SSH connection drops.** See below.
- **Per-job caps apply.** Most GPU partitions cap a single job at 16 cores, 2 GPUs and 150 GB; `aoraki_small` at 8 cores and 32 GB; `aoraki_short` at 32 cores and 256 GB. Asking for more than the cap means the job is rejected or never starts. The full set is in the [Cluster Overview](../../overview.md).

### Surviving a Dropped Connection

An interactive session is attached to your terminal, so closing your laptop or losing your network kills it. Two ways around that:

**Use `tmux` on the login node**, then start your session inside it. `tmux` keeps the terminal alive on the login node when you disconnect, and you can reattach later.

!!! terminal

    ```bash
    tmux new -s work                        # on the login node
    srun --partition=aoraki --time=04:00:00 --pty bash
    # detach with Ctrl-b then d; reconnect later and run:
    tmux attach -t work
    ```

**Or use OnDemand.** Sessions launched from the portal are not tied to your browser at all — close the tab, come back tomorrow, and reconnect from **My Interactive Sessions**.

If the work does not actually need you present, the real answer is a [batch job](../batch/slurm_quickstart.md), which cannot be interrupted this way at all.

!!! related-pages "What's next?"
    - For an overview of all the interactive options, see [Interactive Jobs](interactive.md)
    - For the browser equivalents, see [OnDemand Shell](../../software/OnDemand/ood_shell.md) and the [HPC Desktop](../../software/OnDemand/hpc_desktop.md)
    - For the full list of options and their defaults, see [Job Script Options](../batch/sbatch_options.md)
    - To run the same work unattended, see the [Slurm Quickstart](../batch/slurm_quickstart.md)
    - To check what your session used, see [Job Efficiency](../efficiency.md)
