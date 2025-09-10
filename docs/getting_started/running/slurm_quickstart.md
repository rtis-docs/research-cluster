# Slurm Quickstart Outline

<!-- TODO fix/edit this page -->
## Quickstart Steps

This guide will help you quickly get started with Slurm by showing how to write and submit a simple job script for a single task.

- Write a Slurm job script for one task.
- Submit the job using `sbatch`.
- Monitor and manage your job with Slurm commands.


## 1. What is Slurm?
Slurm is an open-source workload manager designed for high-performance computing (HPC) clusters. It handles job scheduling, resource allocation, and job execution, allowing users to efficiently run and manage batch jobs on shared compute resources. Slurm helps maximize cluster utilization by queuing jobs, assigning resources, and tracking job progress.

## 2. Writing a Slurm Job Script
- Create a new file (e.g., `myjob.slurm`)
- Basic script structure:
    - Shebang (`#!/bin/bash`)
    - Slurm directives (e.g., `#SBATCH --job-name=example`)
    - Resource requests (CPUs, memory, time)
    - Output options (`#SBATCH --output=output.txt`)
    - Module loading or environment setup
    - Commands to run your application
    ### Requesting Resources

    When writing a Slurm job script, you can specify the resources your job needs using `#SBATCH` directives:

    - **CPUs per task:**  
        `#SBATCH --cpus-per-task=4`  
        Requests 4 CPU cores for each task.

    - **Total number of tasks:**  
        `#SBATCH --ntasks=2`  
        Runs 2 tasks in parallel.

    - **Memory:**  
        `#SBATCH --mem=8G`  
        Requests 8 GB of memory for the job.

    - **Time limit:**  
        `#SBATCH --time=01:00:00`  
        Sets a maximum runtime of 1 hour.

    Adjust these values based on your application's requirements to optimize resource usage and scheduling.
## 3. Example Slurm Job Script
Here is an example Slurm job script for a single task:

```bash
#!/bin/bash
#SBATCH --job-name=example_job
#SBATCH --output=example_output.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00

# Load necessary modules or set up your environment here
# module load python/3.9

echo "Running on $SLURM_CPUS_ON_NODE CPUs for a single task"
python3 my_script.py
```
```bash
#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=output.txt
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --mem=1G

echo "Hello from Slurm!"
```

## 4. Submitting the Job
- Use the `sbatch` command:
    ```bash
    sbatch myjob.slurm
    ```

## 5. Monitoring Job Status
- Check job queue:
    ```bash
    squeue -u $USER
    ```
- View job output:
    ```bash
    cat output.txt
    ```

## 6. Cancelling a Job
- Find job ID and cancel:
    ```bash
    scancel <job_id>
    ```

## 7. Additional Resources
- Link to Slurm documentation: [https://slurm.schedmd.com/documentation.html](https://slurm.schedmd.com/documentation.html)
