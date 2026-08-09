# Nextflow

!!! overview "On this Page"
    - Loading Nextflow and configuring it for Aoraki
    - Where the work directory and container images should live
    - Keeping the head process alive for the length of a run
    - Controlling how many jobs a pipeline puts in the queue
    - Requesting GPUs, batching short tasks, and resuming a failed run

[Nextflow](https://nextflow.io/) describes a pipeline as a set of processes connected by
channels. You write what each step does; Nextflow works out the order, submits each task to
Slurm as a separate job, and stitches the results together.

Because it talks to Slurm directly, a Nextflow pipeline behaves like hundreds of small jobs
rather than one big one. Most of this page is about making that behave well on a shared cluster.

## Loading Nextflow

!!! terminal

    ```bash
    module load nextflow
    nextflow -version
    ```

Several versions are installed. `module load nextflow` gives you the newest; use
`module avail nextflow` to see the rest, and `module load nextflow/24.04.3-qlizevk` (for example)
to pin one. Nextflow needs Java, and the module loads `openjdk/17` for you — you do not need to
load it yourself.

The first time you run it, Nextflow downloads its own dependencies into `$HOME/.nextflow`. That
is normal and only happens once per version.

## Configure It for Aoraki

Out of the box Nextflow runs every task as a local process on whatever machine you launched it
from — which on the login node means it will run your whole pipeline there. It has to be told to
use the scheduler.

Create `$HOME/.nextflow/config` with the following. Nextflow reads this file for every pipeline
you run, so this is a one-off:

```groovy
process {
    executor = 'slurm'
    queue    = 'aoraki'

    withLabel: 'gpu' {
        queue          = 'aoraki_gpu'
        clusterOptions = '--gres=gpu:1'
        maxForks       = 2
    }
}

executor {
    queueSize       = 50
    submitRateLimit = '10/1min'
}
```

What each part does:

- `executor = 'slurm'` is the setting that matters. Without it, nothing reaches the scheduler.
- `queue` is the Slurm partition. `aoraki` is the general-purpose one; see the
  [Cluster Overview](../../../getting_started/overview.md) for the others.
- The `gpu` label block is covered under [GPU Processes](#gpu-processes) below.
- `queueSize` and `submitRateLimit` are covered under
  [How Many Jobs at Once](#how-many-jobs-at-once).

!!! note "A pipeline's own settings win"
    This file is merged with the `nextflow.config` that ships with whatever pipeline you run, and
    the pipeline's file is applied last. Well-written pipelines set their own `cpus`, `memory` and
    `time` per process, and those will override anything you put here. Treat your global config as
    "how to reach the scheduler", not "how big every task should be".

To see what a pipeline will actually use once everything is merged, run this from the pipeline's
directory:

!!! terminal

    ```bash
    nextflow config -profile singularity
    ```

## Where the Work Directory Goes

Nextflow gives every task its own directory under `work/`, containing its inputs, its outputs and
its logs. Nothing is cleaned up automatically — that is what makes `-resume` possible. It also
means a single run can leave hundreds of gigabytes behind.

By default `work/` is created wherever you launched the pipeline from. **If that is your home
directory, you will hit the {{ home_quota }} hard quota and the run will fail partway through**,
usually with an error that looks like a problem with the pipeline rather than a problem with
disk space.

Put it on `/projects` instead:

!!! terminal

    ```bash
    nextflow run <pipeline> -work-dir /projects/<division>/<department>/<group>/nextflow_work
    ```

Or set it once in `$HOME/.nextflow/config`:

```groovy
workDir = '/projects/<division>/<department>/<group>/nextflow_work'
```

When a run has finished and you have copied out the results you want, delete the work directory.
See [Storage Options](../../../storage/storage_options.md) for what each storage area is for.

## Container Images

Most published pipelines ship their software as containers. Docker is not available on the
cluster — it requires root — so you need the Singularity or Apptainer profile instead:

!!! terminal

    ```bash
    nextflow run <pipeline> -profile singularity
    ```

Some pipelines call this profile `apptainer` rather than `singularity`. Either works here:
Apptainer is installed at `/usr/bin/apptainer` with a `singularity` compatibility symlink, and
no module is needed to use it.

Set a shared cache directory so images are pulled once rather than re-downloaded into every
run's work directory:

!!! terminal

    ```bash
    export NXF_APPTAINER_CACHEDIR=/projects/<division>/<department>/<group>/apptainer_cache
    ```

!!! warning "Do not leave the image cache in your home directory"
    Without `NXF_APPTAINER_CACHEDIR`, images are cached under `$HOME/.apptainer/cache`. Pipeline
    images are routinely several gigabytes each and a pipeline may use a dozen of them, so the
    {{ home_quota }} home quota disappears quickly — and it will take the rest of your work with
    it when you can no longer write to your home directory.

    Put the line in your `~/.bashrc` so you cannot forget it.

For more on containers generally, see [Apptainer](../../software/software_environments/apptainer.md).

## Keeping the Head Process Alive

Nextflow itself does not run your analysis. It sits there submitting jobs, waiting for them and
submitting the next ones — for the entire length of the pipeline, which may be days. If that
process dies, the pipeline stops.

The [login node](../../../general/guidelines/login_node_usage.md) is not the place for it. The
better pattern is to submit the head process as a small, long-running batch job. It needs almost
no resources itself, and `sbatch` works from compute nodes, so it can submit the pipeline's tasks
from there quite happily.

!!! terminal "run_pipeline.sh"

    ```bash
    #!/bin/bash -e
    #SBATCH --job-name=nextflow_head
    #SBATCH --partition=aoraki_long
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=4G
    #SBATCH --time=3-00:00:00
    #SBATCH --output=nextflow_head_%j.out

    module load nextflow

    export NXF_APPTAINER_CACHEDIR=/projects/<division>/<department>/<group>/apptainer_cache

    nextflow run <pipeline> \
        -profile singularity \
        -work-dir /projects/<division>/<department>/<group>/nextflow_work \
        -resume
    ```

Submit it with `sbatch run_pipeline.sh`. Give `--time` more than you think the pipeline needs:
if the head job hits its wall time, every task it was managing is orphaned.

For a short pipeline you are watching interactively, `tmux` on the login node is a reasonable
alternative — it keeps the process alive when your SSH connection drops. See
[Interactive Sessions](../interactive/interactive_shell.md) for how to use it.

## How Many Jobs at Once

By default Nextflow keeps **100** tasks submitted at a time and submits them as fast as it can.
On a shared cluster that is more aggressive than it sounds, because Slurm caps how many jobs one
user may have running in each partition.

Table: Running jobs allowed per user, by partition

| Partition | Jobs running at once |
| :-- | --: |
| `aoraki_short` | 250 |
| `aoraki` | 100 |
| `aoraki_small` | 30 |
| `aoraki_long` | 25 |
| `aoraki_bigmem` | 10 |
| Any GPU partition | 2 |

So the default of 100 uses your entire allowance on `aoraki` — one pipeline and you have no
room left for anything else you want to run. Dropping `queueSize` to 50 costs you very little
in wall time and leaves you space to work.

`submitRateLimit` spreads the submissions out. Without it, Nextflow will fire 100 `sbatch` calls
at the scheduler in a burst every time a stage completes.

## GPU Processes

Nextflow's Slurm executor only understands five process directives: `clusterOptions`, `cpus`,
`memory`, `queue` and `time`. In particular it does **not** support the `accelerator` directive,
which is what most Nextflow documentation tells you to use for GPUs — on Slurm it is silently
ignored.

This matters more than it sounds. Sending a task to `queue = 'aoraki_gpu'` puts it on a machine
that has GPUs, but Slurm hands out GPUs individually: without an explicit request the task gets
none, and the pipeline either falls back to CPU or fails with a CUDA error. The GPU has to come
through `clusterOptions`:

```groovy
process {
    withLabel: 'gpu' {
        queue          = 'aoraki_gpu'
        clusterOptions = '--gres=gpu:1'
        maxForks       = 2
    }
}
```

`maxForks = 2` matches the two-running-jobs cap on the GPU partitions. Without it, Nextflow
happily submits fifty GPU tasks that then sit pending while two run — which does not make the
pipeline faster, but does fill the queue.

Check which label a pipeline uses for its GPU steps before relying on this; `gpu` is a common
convention but not a universal one. For GPU jobs generally, see
[GPU Jobs](../batch/slurm_examples/gpu-slurm.md).

## Batching Short Tasks

If a pipeline has thousands of tasks that each take a minute or two, submitting one Slurm job
per task wastes more time on scheduling overhead than the tasks take to run. The `array`
directive groups them into Slurm job arrays instead:

```groovy
process {
    array = 100
}
```

This requires a recent Nextflow — use `nextflow/24.04.3-qlizevk` or newer. It is the single most
effective change you can make to a pipeline made of many short steps, and it is much kinder to
the scheduler than the equivalent flood of individual jobs.

## Resuming a Failed Run

Add `-resume` and Nextflow re-uses the results of every task that already completed successfully,
picking up from the first one that failed:

!!! terminal

    ```bash
    nextflow run <pipeline> -profile singularity -resume
    ```

This only works while the work directory still exists — it is where the cached results live. If
you have deleted `work/`, `-resume` has nothing to resume from and the pipeline starts over.

## nf-core

[nf-core](https://nf-co.re/) is a curated collection of over 100 community-built Nextflow
pipelines for bioinformatics, all following the same conventions. They come with `singularity`
profiles and sensible per-process resource requests, so in practice they need little from you
beyond the executor configuration above.

## EPI2ME

[EPI2ME Desktop](https://labs.epi2me.io/) is Oxford Nanopore's graphical front end for running
their Nextflow pipelines, and it can import generic Nextflow workflows too. It is available
through OnDemand — see
[Available Apps](../../software/OnDemand/available_apps.md#epi2me-desktop).

It was not designed for cluster use, and running pipelines from the command line as described
above gives you far more control over how they reach the scheduler.

!!! related-pages "What's next?"
    - For whether you need a pipeline at all, see [Workflows](index.md)
    - For the simpler alternative, see [Array Jobs](../batch/slurm_examples/array-slurm.md)
    - For where the work directory should live, see [Storage Options](../../../storage/storage_options.md)
    - For containers on the cluster, see [Apptainer](../../software/software_environments/apptainer.md)
    - Stuck? Email the eResearch Support team at **{{ support_email }}**
