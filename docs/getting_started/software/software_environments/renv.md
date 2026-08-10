# renv (R Package Environments)

!!! overview "On this Page"
      - What `renv` does, and when it is worth the effort on a shared cluster
      - Setting up a project, and getting package installs to take minutes instead of hours
      - Moving the package cache off your home directory before it fills up
      - Using an `renv` project from a Slurm job and from RStudio on OnDemand
      - Sharing a project so someone else gets the same package versions

[`renv`](https://rstudio.github.io/renv/) gives each project its own R package library, and records the exact version of every package in a lockfile. Reinstalling from that lockfile — on the cluster, on a laptop, or a year later — gets you the same versions you started with.

On a shared system this solves a specific problem. Without it, every project you run shares one library in your home directory. Upgrading a package for one analysis silently changes every other analysis that used it, and there is no record of what the versions were when your results were produced.

!!! note "renv or the other options?"
    `renv` manages **R packages within a project**. It does not manage R itself, and it does not install system libraries.

    - For a different **version of R**, use the [module system](modules.md).
    - For a full environment including non-R dependencies, see [Conda/Mamba](conda.md), which can also manage R.
    - For setting a single library path for all your work rather than per project, see [Managing Package Libraries](../applications/r_rstudio.md#managing-package-libraries-with-r-and-rstudio).

## Before You Start

`renv` is not installed system-wide, so you install it once yourself. First load an R module — the system R in `/usr/bin/R` is older and is not the one to build work against.

To see the available versions:

!!! terminal

    ```bash
    module spider r
    ```

Then load one and install `renv`:

!!! terminal

    ```bash
    module load r/4.4.3
    Rscript -e 'install.packages("renv", repos = "https://cloud.r-project.org")'
    ```

!!! warning "Package libraries are tied to an R version"
    A library built under `r/4.4.3` will not work under `r/4.5.1`. R keeps them apart automatically — the default library path is `~/R/x86_64-pc-linux-gnu-library/4.4`, with the version on the end — and `renv` does the same inside each project.

    This means **pin the R module version in your job scripts** rather than using `module load r`. If you move a project to a newer R, expect to run `renv::restore()` again to rebuild the library for it.

Package installation compiles C, C++ and Fortran code and can be heavy. The [login node](../../../general/guidelines/login_node_usage.md) allows 8 CPUs and 60 GB of memory, and asks that tasks stay under 30 minutes — a small project fits comfortably, but for a large restore use an [interactive allocation](../../running/interactive/interactive_shell.md) instead.

## Setting Up a Project

Work in a directory on [`/projects` or `/weka`](../../../storage/storage_options.md) rather than your home directory. Package libraries get large, and your home directory has a {{ home_quota }} quota.

!!! terminal

    ```bash
    cd /projects/<division>/<school>/<department>/<group>/my_analysis
    module load r/4.4.3
    R
    ```

Then, in R:

!!! r-code

    ```r
    renv::init()
    ```

This creates three things in the project directory:

Table: What `renv::init()` adds to your project

| Path | What it is | Commit to git? |
| :-- | :-- | :-- |
| `renv.lock` | The lockfile — every package and its exact version | **Yes**. This is the reproducible record |
| `renv/activate.R` | Startup script that points R at the project library | **Yes** |
| `.Rprofile` | One line, sourcing `renv/activate.R` | **Yes** |
| `renv/library/` | The installed packages themselves | No — `renv` adds this to `.gitignore` for you |

From now on, starting R **from that directory** activates the project automatically. You should see a startup message naming the project. If you do not, you are in the wrong directory, or R was started in a way that skips `.Rprofile` — see [Common Problems](#common-problems).

## Making Installs Fast

This is the single change worth making on this cluster. By default R downloads package *source* from CRAN and compiles it, which for a large project can take hours.

The cluster runs Rocky Linux 9, and [Posit Package Manager](https://packagemanager.posit.co/) publishes prebuilt binaries for it. Pointing R at those turns most of that compiling into a download.

Add this to your `~/.Rprofile` so it applies to everything you do:

!!! r-code "File: `~/.Rprofile`"

    ```r
    options(
      repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/rhel9/latest"),
      HTTPUserAgent = sprintf(
        "R/%s R (%s)",
        getRversion(),
        paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])
      ),
      Ncpus = 8
    )
    ```

The `HTTPUserAgent` line is what tells Package Manager to serve binaries rather than source. `Ncpus` lets R compile several packages at once for the ones that still need building — set it no higher than the cores you have available.

!!! tip "Check it is working"
    Install something and watch the output. A binary install reports downloading a `.tar.gz` and unpacking it in seconds. A source install prints pages of compiler commands. If you are still seeing compiler output for common packages, the `HTTPUserAgent` option has not been picked up.

!!! note "A project `.Rprofile` replaces your personal one"
    R sources **only one** `.Rprofile` — the one in the project directory if it exists, otherwise the one in your home directory. Because `renv` creates a project `.Rprofile`, your `~/.Rprofile` is **not** read inside a project.

    To keep the repository settings inside a project, either add the `options()` block to the project's `.Rprofile` above the `renv` line, or put the equivalent in `~/.Renviron`, which is always read. See [.Renviron vs .Rprofile](../applications/r_rstudio.md#renviron-vs-rprofile).

## Moving the Cache off Your Home Directory

`renv` keeps one shared cache of installed packages and links each project's library to it, so ten projects using the same version of a package store it once. That cache lives under `~/.cache/R/renv` by default, and on a {{ home_quota }} home directory quota it will eventually become a problem.

Move it somewhere with room, by adding a line to `~/.Renviron`:

!!! terminal

    ```bash
    nano ~/.Renviron
    ```

!!! r-code "File: `~/.Renviron`"

    ```r
    RENV_PATHS_CACHE=/projects/<division>/<school>/<department>/<group>/renv-cache
    ```

`.Renviron` is read before R starts, so this applies to `R`, `Rscript`, batch jobs and RStudio alike. Restart R for it to take effect.

!!! tip "A research group can share one cache"
    Point everyone in the group at the same `RENV_PATHS_CACHE` directory and packages are downloaded and built once for the whole group. The directory needs to be group-writable — see [File Permissions](../../../storage/file_permissions.md).

## Everyday Use

Table: The commands you will use most

| Command | What it does |
| :-- | :-- |
| `renv::install("dplyr")` | Install a package into the project library |
| `renv::snapshot()` | Record what is currently installed into `renv.lock` |
| `renv::status()` | Compare the lockfile against what is installed |
| `renv::restore()` | Install what the lockfile says, discarding differences |
| `renv::update()` | Update packages to their latest available versions |

The cycle is: install what you need, then `renv::snapshot()` to record it.

!!! r-code

    ```r
    renv::install("dplyr")
    renv::install("ggplot2")

    # Bioconductor and GitHub packages work too
    renv::install("bioc::DESeq2")
    renv::install("tidyverse/glue")

    renv::snapshot()
    ```

`renv::snapshot()` only records packages your code actually loads, by scanning for `library()` and `::` calls. If you install something and it does not appear in the lockfile, check that it is referenced somewhere in the project.

## Using renv in a Slurm Job

The important part is that the job must **start R with the project directory as its working directory**, so that the project `.Rprofile` is read and the project library is used.

!!! terminal "Script: `run_analysis.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=r_analysis
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00

    # Pin the same R version the project library was built for
    module load r/4.4.3

    # Start in the project directory so renv activates
    cd /projects/<division>/<school>/<department>/<group>/my_analysis

    Rscript analysis.R
    ```

Submit it as usual:

!!! terminal

    ```bash
    sbatch run_analysis.sh
    ```

To confirm the job used the project library rather than your personal one, print the paths at the top of the R script:

!!! r-code "Script: `analysis.R`"

    ```r
    cat("Library paths in use:\n")
    print(.libPaths())
    ```

The first path should be inside your project's `renv/library/`.

!!! warning "Run `renv::restore()` before you submit, not inside the job"
    Restoring downloads and compiles packages. Doing that inside a batch job means every job repeats the work, jobs sit in the queue holding an allocation while they compile, and an array job will have many tasks writing to the cache at once.

    Restore once, interactively, then submit. Jobs should find everything already built.

!!! warning "Do not use `--vanilla`"
    `Rscript --vanilla` and `R --no-init-file` skip `.Rprofile`, which is exactly the file that activates `renv`. The job will run against your default library and either fail with missing packages or, worse, quietly use different versions.

## Using renv with RStudio on OnDemand

RStudio is available through [OnDemand](../OnDemand/available_apps.md) as versioned Apptainer images. `renv` works there, with one thing to watch.

Each RStudio image bundles its own R, which is **not** the same installation as the `r/…` modules. A project library built under `module load r/4.4.3` on the command line is only reusable in RStudio if that image has a matching R version. If the versions differ, R will tell you the library is for a different version, and you need `renv::restore()` to rebuild it for that R.

The simplest approach is to pick one R version for a project and stay with it — either an RStudio image, or a module — rather than moving between them.

Opening the project in RStudio through **File → Open Project**, or starting RStudio in the project directory, activates `renv` the same way as on the command line.

## Sharing and Reproducing a Project

The lockfile is the deliverable. Commit `renv.lock`, `.Rprofile` and `renv/activate.R` to version control, and leave `renv/library/` out of it.

Someone else — or you, on another system — then runs:

!!! r-code

    ```r
    renv::restore()
    ```

which installs the recorded versions into a fresh project library.

!!! note "Lockfiles record the repository as well as the packages"
    If you followed [Making Installs Fast](#making-installs-fast), the lockfile will name the Rocky Linux binary repository. That URL serves binaries for this cluster and source everywhere else, so it still works for a collaborator on macOS or Windows — but they will get no speed benefit and may prefer to set their own `repos`.

For a result you may need to reproduce years later, record the R version alongside the lockfile — the module name, such as `r/4.4.3`, is enough. `renv` restores packages, not R itself.

## Common Problems

**Starting R does not activate the project.** R only reads `.Rprofile` from its working directory. Check with `getwd()` that you are in the project, and that `.Rprofile` exists there. In a Slurm job this is almost always a missing `cd`.

**Packages are missing in a job that worked interactively.** Your shell startup files are not read by a Slurm job in the same way, so anything you loaded by hand is absent. Make sure the job script has its own `module load r/…` and `cd` into the project.

**A package fails to compile with a missing header or library.** The package needs a system library that is not loaded. Search the modules for it:

!!! terminal

    ```bash
    module spider <name>
    ```

Load it before installing. If there is no module for what the package needs, email the eResearch Support team at **{{ support_email }}** with the package name and the error, and it can be added.

**"Package was installed by a different version of R".** The library was built for another R. Load the R version the project was created with, or run `renv::restore()` to rebuild it for the version you are now using.

**Your home directory filled up.** Move the cache, as in [Moving the Cache off Your Home Directory](#moving-the-cache-off-your-home-directory). Existing projects pick up the new location on their next install; the old `~/.cache/R/renv` can then be deleted.

**Everything is compiling from source and taking hours.** The repository options are not being applied. Inside a project, `~/.Rprofile` is ignored — see the note in [Making Installs Fast](#making-installs-fast). Check with `getOption("repos")`, which should show the `packagemanager.posit.co` URL.

!!! related-pages "What's next?"
      - For R versions, RStudio, and library paths outside `renv`, see [R and Rstudio](../applications/r_rstudio.md)
      - For worked examples of running R under the scheduler, see [Using R with Slurm](../../running/batch/slurm_examples/r-slurm.md)
      - For loading R and other software, see [Using Modules (LMOD)](modules.md)
      - For managing non-R dependencies alongside R, see [Conda/Mamba](conda.md)
      - For where to keep project data and libraries, see [Storage Options](../../../storage/storage_options.md)
