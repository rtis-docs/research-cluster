# Software and Environments

!!! overview "On this Page"
    - Finding out whether something is installed
    - Why a command works in your shell but not in your job script
    - Installing software yourself, and where to put it
    - Containers, and asking us to install something

## Is a Particular Piece of Software Installed?

Most centrally installed software is provided as a **module**:

!!! terminal

    ```bash
    module avail              # everything available
    module spider samtools    # search for something by name
    module load samtools      # load the latest version
    module list               # what you have loaded now
    ```

`module load <name>` without a version gives you the highest version number available. Name
the version explicitly — `module load r/4.4.3` — when you need results to be reproducible.

Not everything comes from a module. Some software has its own page under
[Applications](../../getting_started/software/applications/index.md), some is available as
an [OnDemand app](../../getting_started/software/OnDemand/available_apps.md), and
domain-specific collections are provided through
[SBGrid](../../getting_started/software/software_environments/sbgrid.md).

## Why Does My Batch Job Say "command not found" When It Works When I Type It?

Because a batch job starts in a fresh environment. It does not inherit the modules you
loaded, the Conda environment you activated, or anything you set up in the shell you
submitted from.

Everything the job needs has to be in the job script:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=analysis
    #SBATCH --time=02:00:00
    #SBATCH --mem=16G

    module load samtools          # load it here, not before sbatch
    samtools view input.bam
    ```

For Conda, activate inside the script as well. `conda activate` needs Conda's shell function
to be set up first, which is why activating in a job script often needs an extra line — see
[Using Conda with Slurm](../../getting_started/software/software_environments/conda.md#using-conda-with-slurm).

Two related traps:

- **`~/.bashrc` is not always read.** A non-interactive job shell may skip parts of your
  startup files, so anything you rely on being in `~/.bashrc` may not be there. See
  [Shells](../../getting_started/software/software_environments/shells.md).
- **It worked yesterday.** If you have since loaded a different module version by default,
  pin the version in the script.

## Can I Install Software Myself?

Yes. You do not have root, so anything needing a system package manager is out, but
everything below works in your own space:

| Approach | Good for | See |
| :-- | :-- | :-- |
| Conda / Mamba | Bioinformatics, data science, anything on conda-forge or Bioconda | [Conda](../../getting_started/software/software_environments/conda.md) |
| Python virtual environments | Pure-Python projects, alongside a Python module | [venv](../../getting_started/software/software_environments/venv.md) |
| `renv` | Reproducible R project libraries | [renv](../../getting_started/software/software_environments/renv.md) |
| Spack | Compiled scientific software and its dependencies | [Spack](../../getting_started/software/software_environments/spack.md) |
| Apptainer | Anything that ships as a container | [Apptainer](../../getting_started/software/software_environments/apptainer.md) |

Whichever you use, **install it somewhere other than your home directory** if it is going to
be large. See below.

## Why Is Conda Filling Up My Home Directory?

Conda puts environments in `~/.conda/envs` and caches every package it downloads in
`~/.conda/pkgs` by default. A handful of bioinformatics environments will use most of a
{{ home_quota }} quota on their own.

Three things help:

- **Create environments in `/projects` instead**, with `conda create -p /projects/.../envs/myenv`.
  They are then shareable with your group as well.
- **Move the package cache** off your home directory — see
  [Cache location](../../getting_started/software/software_environments/conda.md#cache-location).
- **Clean up.** `conda clean --all` removes cached downloads, and `conda env remove -n <name>`
  removes environments you no longer use.

[Storage and Quotas](disk_usage.md) covers the other things that commonly fill a home
directory.

## Can I Run Docker Containers?

Not directly — Docker requires root, which is not available on a shared cluster. Use
**Apptainer** instead, which is designed for HPC and runs as your own user.

Apptainer can run most Docker images without modification:

!!! terminal

    ```bash
    module load apptainer
    apptainer pull mytool.sif docker://biocontainers/samtools:latest
    apptainer exec mytool.sif samtools --version
    ```

See [Apptainer](../../getting_started/software/software_environments/apptainer.md). Build
images on your own machine or pull them ready-made; the cluster is not the place to iterate
on a container definition.

## Which Versions of Python and R Are Available?

!!! terminal

    ```bash
    module avail python
    module avail r
    ```

The system Python is there for the operating system, not for your work — do not install
packages into it. Load a Python module and create a virtual environment, or use Conda.

For R, [R and RStudio](../../getting_started/software/applications/r_rstudio.md) covers
running it on the cluster, and RStudio is available as an
[OnDemand app](../../getting_started/software/OnDemand/available_apps.md).

## How Do I Ask for Software to Be Installed?

Email {{ support_email }}. Include:

- The **name and version**, and a link to its home page or repository
- **How you install it** if you already know — a Conda package, a container, a source tarball
- Whether anyone else in your group needs it, which affects where we put it
- Any licence you hold, for commercial software

Where the software is straightforward to install into your own space, we will usually point
you at the quickest route rather than making you wait for a central install. See
[Support](../support.md) for the other ways to reach us and what makes a request easy to act on.

!!! related-pages "What's next?"
    - For modules, see [Using Modules](../../getting_started/software/software_environments/modules.md)
    - For the full set of options, see [Software Environments](../../getting_started/software/software_environments/index.md)
    - For per-application notes, see [Applications](../../getting_started/software/applications/index.md)
    - If a job is failing rather than a command missing, see [Why Did My Job Fail?](slurm_job_failures.md)
