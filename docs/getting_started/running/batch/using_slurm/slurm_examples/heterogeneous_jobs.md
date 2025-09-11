# Heterogeneous Jobs

Heterogeneous jobs in Slurm allow you to submit a single job that requests different resources for different job components (job steps). This is useful when your workflow requires, for example, both CPU-only and GPU resources, or different memory or core counts for different tasks, all within the same job allocation.

## How Heterogeneous Jobs Work

A heterogeneous job is composed of two or more job components, each with its own resource requirements. Slurm schedules all components together, and each component runs as a separate job step.

## Example: CPU and GPU Components

Suppose you have a workflow where the first part runs on CPUs and the second part requires a GPU. You can submit a heterogeneous job by specifying the resources for each component directly in your script using `#SBATCH` lines and separating components with `#SBATCH hetjob`.

Below is an example heterogeneous job script for a cluster where GPU jobs must use a separate partition (e.g., `aoraki_gpu`):

!!! terminal

    ```bash
    #!/bin/bash

    #SBATCH --job-name=hetero_example

    # Component 1: CPU-only
    #SBATCH --partition=aoraki
    #SBATCH --ntasks=2
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=8G

    #SBATCH hetjob

    # Component 2: GPU
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gres=gpu:1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=2
    #SBATCH --mem=16G

    echo "This is component $SLURM_HET_GROUP_ID of the heterogeneous job"

    if [ "$SLURM_HET_GROUP_ID" -eq 0 ]; then
        echo "Running CPU-only component"
        # Place CPU-only commands here
    else
        echo "Running GPU component"
        # Place GPU commands here
    fi
    ```

To submit this job, simply run:

!!! terminal

    ```bash
    sbatch hetero_script.sh
    ```

Each component will execute the script, and you can branch logic based on `SLURM_HET_GROUP_ID`.

!!! note

    If your cluster uses a separate partition for GPU jobs (e.g., `aoraki_gpu`), you must specify the partition for each component using `#SBATCH --partition=...` in the relevant section. For example:

    ```bash
    #SBATCH --partition=aoraki           # For CPU component
    #SBATCH hetjob
    #SBATCH --partition=aoraki_gpu       # For GPU component
    ```

    Each component can have its own partition and resource requirements. Make sure to match the partition to the resources (CPU or GPU) needed for each component.

For more details, see the [Slurm documentation on heterogeneous jobs](https://slurm.schedmd.com/heterogeneous_jobs.html).

<!-- TODO improve wording for using different partitions -->