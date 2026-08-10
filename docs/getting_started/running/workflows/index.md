# Workflows

!!! overview "On this Page"
    - What a workflow manager does, and when you need one
    - Whether your problem is an array job or a pipeline
    - Which workflow tools are available on Aoraki
    - The two settings to get right before your first run

A workflow manager runs a chain of tools for you. You describe the steps and how they connect,
and it works out what can run in parallel, submits each task to Slurm as its own job, waits for
the results, and feeds them into the next step. If something fails halfway through, it can pick
up where it stopped instead of starting again.

## Do You Actually Need One?

Workflow managers earn their complexity on pipelines with several stages. For a single program
run over many inputs, an [array job](../batch/slurm_examples/array-slurm.md) is simpler,
faster to write, and easier to debug.

Table: Choosing between an array job and a workflow manager

| Your problem | Use this |
| :-- | :-- |
| One program, many input files, no dependencies between them | An [array job](../batch/slurm_examples/array-slurm.md) |
| A handful of steps you run by hand every few months | A shell script that calls `sbatch` |
| Several tools chained together, where one step's output is the next step's input | A workflow manager |
| A published pipeline someone else wrote — nf-core, an ONT workflow | A workflow manager, because the pipeline already is one |
| The same analysis re-run as data arrives, and you need to know exactly what produced each result | A workflow manager |

The honest summary: if you can describe your work as "run this one thing 500 times", reach for
an array job. If you can only describe it as a diagram, reach for a workflow manager.

## What Is Available

Table: Workflow tools on the Research Cluster

| Tool | Availability | Notes |
| :-- | :-- | :-- |
| [Nextflow](nextflow.md) | `module load nextflow` | The supported option. Five versions installed, and it submits directly to Slurm |
| Snakemake | Not installed as a module | Install it into a [conda environment](../../software/software_environments/conda.md) yourself |
| [EPI2ME Desktop](../../software/OnDemand/available_apps.md#epi2me-desktop) | Through OnDemand | A graphical front end to Oxford Nanopore's Nextflow pipelines |

### Snakemake

There is no Snakemake module on Aoraki. If you want to use it, create a
[conda environment](../../software/software_environments/conda.md) and install Snakemake together
with its Slurm executor plugin, then run it with `--executor slurm`. We have not set this path
up as a supported configuration, so if you hit trouble getting it talking to the scheduler,
email the eResearch Support team at **{{ support_email }}** — we would rather help than have you
give up on it.

## Before Your First Run

Two settings catch almost everyone, whichever tool you pick. Both come down to the same thing:
workflow managers write a great deal of data, and by default they write it to your home
directory, which has a hard quota of **{{ home_quota }}**.

**Put the working directory on `/projects`.** Every intermediate file from every task lands
there. A single run of a genomics pipeline can produce hundreds of gigabytes of intermediates
you will never look at, and they stay on disk until you delete them. `/projects` is sized for
this; your home directory is not.

**Move the container image cache off your home directory.** Pipelines pull container images —
often several gigabytes each — and cache them. Point that cache at a projects path and the
images are downloaded once and shared between runs instead of being re-pulled every time.

The [Nextflow page](nextflow.md) shows exactly how to set both. For where the storage areas are
and what they are for, see [Storage Options](../../../storage/storage_options.md).

!!! warning "The head process runs for as long as the pipeline does"
    A workflow manager is not fire-and-forget. One long-lived process sits there orchestrating,
    submitting jobs and waiting for them, for the entire duration of the run — which may be days.
    If it dies, the pipeline stops.

    That process must live somewhere that survives your SSH session closing. See
    [Keeping the Head Process Alive](nextflow.md#keeping-the-head-process-alive).

!!! related-pages "What's next?"
    - To get started, see [Nextflow](nextflow.md)
    - For the simpler alternative, see [Array Jobs](../batch/slurm_examples/array-slurm.md)
    - For where your data should live, see [Storage Options](../../../storage/storage_options.md)
    - For how jobs are scheduled at all, see [Running Jobs](../running_jobs_overview.md)
