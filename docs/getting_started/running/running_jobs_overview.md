# Running Jobs Overview

!!! overview "On this Page"
    - Interactive Jobs (Open OnDemand)
    - Batch Jobs (Slurm)
    - How to Choose

When deciding how to run your job on the cluster, you have two main options: interactive jobs (often launched through Open OnDemand) and batch jobs (submitted directly to Slurm).

## How Jobs Are Managed on a Cluster

All jobs on a cluster are managed by a scheduler, such as Slurm. The scheduler keeps track of available resources (like CPUs, memory, and GPUs) and coordinates when and where jobs run. When you submit a job, it enters a queue and waits until the requested resources are free. The scheduler ensures fair access for all users, prioritizes jobs based on policies, and monitors job progress. This system allows many users to share the cluster efficiently and helps prevent resource conflicts.


## Interactive Jobs (Open OnDemand)

- **Best for:** Exploratory work, debugging, visualization, or when you need a graphical interface (e.g., Jupyter, RStudio, desktop apps).
- **How it works:** You launch an interactive session from the Open OnDemand portal. The portal submits a Slurm job for you and provides access to a running environment in your browser.
- **Advantages:** Immediate feedback, easy access to files and applications, no need to write a job script.
- **Limitations:** Not ideal for long-running or large-scale jobs. Resources may be limited compared to batch jobs.

## Batch Jobs (Slurm)

- **Best for:** Large-scale computations, production runs, jobs that can run unattended, or when you need to process many files or parameters.
- **How it works:** You write a job script specifying resources and commands, then submit it to Slurm using `sbatch`. The scheduler runs your job when resources are available.
- **Advantages:** Suitable for automation, reproducibility, and running many jobs at once. Can request more resources and run for longer periods.
- **Limitations:** Requires writing a job script and waiting for resources to become available.

## How to Choose

- Use **interactive jobs** for short, hands-on tasks, testing, or when you need a graphical interface.
- Use **batch jobs** for longer, automated, or resource-intensive work.

If you’re unsure, start with an interactive session to explore your workflow, then move to batch jobs for larger or repeated tasks.



!!! related-pages "What's next?"
    - [Open OnDemand Guide](../software/onDemand/ondemand.md)
    - [Writing Slurm Job Scripts](slurm_quickstart.md)
    - [Job Efficiency](efficiency.md)