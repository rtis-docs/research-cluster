# Interactive Jobs

!!! overview "On this Page"
    - What an interactive job is, and how it differs from a batch job
    - The three ways to start one, and how to choose between them
    - How to size a session so it starts quickly and does not waste resources
    - When to stop working interactively and write a batch script

An **interactive job** gives you a compute node you can work on directly — a notebook, a desktop, or a shell prompt — instead of submitting a script and waiting for the output.

It is still an ordinary Slurm job. That has two consequences people are often surprised by:

- **It queues.** Pressing **Launch** or running `srun` does not start anything immediately. Your session waits until the resources you asked for are free, exactly like a batch job.
- **It holds its allocation for the whole wall time**, whether or not you are typing. A three-day session where you spend two of them thinking has reserved a node for three.

Because of the second point, interactive work is the easiest way to waste cluster capacity — and the easiest to fix. Ask for a realistic wall time, and end the session when you are done.

## Three Ways to Start One

Table: The three routes into an interactive session

| Route | What you get | Use this when |
| :-- | :-- | :-- |
| **An [OnDemand app](../../software/OnDemand/available_apps.md)** | JupyterLab, RStudio, MATLAB, a full Linux desktop and more, in your browser | Almost always — it is the easiest route, needs no Slurm syntax, and survives a closed laptop |
| **[`srun --pty`](interactive_shell.md)** | A single shell prompt on a compute node | You are already in a terminal and want a quick prompt on a node |
| **[`salloc`](interactive_shell.md#salloc-holding-an-allocation)** | An allocation you keep, and run several commands against | You want one reservation for a sequence of steps, or need to launch parallel tasks by hand |

### OnDemand apps

[Open OnDemand](../../software/OnDemand/ondemand.md) is the web portal for the cluster. You fill in a short form — cores, memory, wall time, GPU or not — and it writes and submits the Slurm job for you.

Two things make it the default recommendation. It handles graphical software, which a plain SSH session cannot do comfortably. And the session is not tied to your connection: close the browser tab, go home, and reconnect to the same session from **My Interactive Sessions**.

[Available Apps :material-arrow-right:](../../software/OnDemand/available_apps.md){ .md-button }

If the software you need has no app of its own, the [HPC Desktop](../../software/OnDemand/hpc_desktop.md) gives you a full Linux desktop on a compute node.

### A shell on a compute node

If you are already working in a terminal and just want a prompt on a compute node — to compile something, to test a command before putting it in a script, or to run a short interactive tool — use `srun --pty` or `salloc`.

[Interactive Sessions from the Command Line :material-arrow-right:](interactive_shell.md){ .md-button }

!!! note "Not the same as OnDemand's shell"
    **Clusters > Aoraki Shell Access** in OnDemand gives you a terminal on the **login node**, not a compute node — it is a browser equivalent of SSH. See [OnDemand Shell](../../software/OnDemand/ood_shell.md). To get onto a compute node from there, you still run `srun --pty` or `salloc`.

## Sizing Your Session

What you request is what you get, and nothing more. If the application inside your session needs more memory than you asked for it is killed; it cannot borrow the rest of the node.

- **Wall time is the lever that matters most.** Slurm backfills short jobs into gaps in the schedule, so a two-hour session usually starts sooner than an eight-hour one. Ask for what your working session actually needs, not for the whole day.
- **Memory is reserved even when unused**, so a habit of asking for 200 GB "to be safe" keeps a node's cores idle for everyone else.
- **Cores only help if the software uses them.** Most interactive exploration is single-threaded.
<<<<<<< HEAD
- The same per-job limits apply as to any other job — see the [Cluster Overview](../../../getting_started/overview.md). GPU partitions cap a single job at 2 GPUs, and you may have at most 2 running GPU jobs per partition and 10 running OnDemand sessions.
=======
- The same per-job limits apply as to any other job — see the [Cluster Overview](../../overview.md). GPU partitions cap a single job at 2 GPUs, and you may have at most 2 running GPU jobs per partition and 10 running OnDemand sessions.
>>>>>>> bee4f213358f539a530dcc7d94b8a392cfc04f9a

Once a session ends, `seff <jobid>` tells you what you actually used. For an interactive session the number to look at is peak memory — see [Job Efficiency](../efficiency.md).

!!! tip "End the session when you finish"
    For OnDemand, click **Delete** under **My Interactive Sessions** — closing the tab does not end the job. For `srun --pty` or `salloc`, type `exit`.

## When to Use a Batch Job Instead

Move to [batch](../batch/slurm_quickstart.md) as soon as any of these is true:

- The work runs for hours without you doing anything.
- You want to run it more than once, or over many inputs.
- You want it to survive closing your laptop or losing your connection.
- You want a record of exactly what was run.

The usual progression is to work out the shape of an analysis interactively on a small subset of the data, then turn it into a script and submit it over everything.

!!! related-pages "What's next?"
    - For a shell on a compute node, see [Interactive Sessions from the Command Line](interactive_shell.md)
    - For the browser portal, see [Open OnDemand](../../software/OnDemand/ondemand.md) and [Available Apps](../../software/OnDemand/available_apps.md)
    - For graphical software with no app of its own, see the [HPC Desktop](../../software/OnDemand/hpc_desktop.md)
    - To check what your session actually used, see [Job Efficiency](../efficiency.md)
    - To move on to unattended work, see the [Slurm Quickstart](../batch/slurm_quickstart.md)
    - To see how busy the cluster is, see [Current Utilisation](../../current_utilisation.md)
