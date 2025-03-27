# Job Efficiency


To determine the efficiency of your SLURM job, you can follow these steps:

1. **Submit Your Job**: First, submit your job to the SLURM scheduler using the `sbatch` command.

    ```bash
    sbatch my_job_script.sh
    ```

2. **Monitor Job Progress**: Use the `squeue` command to monitor the progress of your job.

    ```bash
    squeue -u your_username
    ```

3. **Check Job Completion**: Once your job is completed, you can check the job details using the `sacct` command.

    ```bash
    sacct -j job_id --format=JobID,JobName,Partition,Account,AllocCPUS,State,ExitCode
    ```

4. **Analyze Job Efficiency**: To analyze the efficiency of your job, you can use the `seff` command, which provides a summary of the job's resource usage.

    ```bash
    seff job_id
    ```

    The `seff` command will output information such as:

    - Job ID
    - Job Name
    - Partition
    - User
    - State
    - Nodes
    - Cores per node
    - CPU Utilized
    - CPU Efficiency
    - Memory Utilized
    - Memory Efficiency

    Example output:

    ```output
    Job ID: 123456
    Job Name: my_job
    Partition: compute
    User: your_username
    State: COMPLETED
    Nodes: 1
    Cores per node: 4
    CPU Utilized: 01:30:00
    CPU Efficiency: 75.00% of 02:00:00 core-walltime
    Memory Utilized: 2.00 GB
    Memory Efficiency: 50.00% of 4.00 GB
    ```

5. **Interpret Efficiency Metrics**: The key metrics to look at are CPU Efficiency and Memory Efficiency. These metrics indicate how well your job utilized the allocated resources. Higher percentages indicate better efficiency.

By following these steps, you can determine the efficiency of your SLURM job and make any necessary adjustments to improve resource utilization in future runs.