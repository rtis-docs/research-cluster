# Job Efficiency

Efficient use of cluster resources helps you get results faster and reduces wait times for everyone. Here are the steps you can follow to determine how efficient your SLURM job was:

To determine the efficiency of your SLURM job, you can follow these steps:

## 1. Submit Your Job

Submit your job to the SLURM scheduler using the `sbatch` command. Jobs run through OnDemand are done for you and the job number can be found on the job card under the "My Interactive Sessions" page.

!!! terminal
    ```bash
    sbatch my_job_script.sh
    ```
*What to look for*: The command will return a job ID. Make a note of this ID, as you will use it to check your job's status and efficiency.


## 2. Monitor Job Progress 

Check the status of your job while it is running.

!!! terminal
    ```bash
    squeue -u your_username
    ```

## 3. Check Job Completion

After your job finishes, view its details using the `sacct` command.

!!! terminal
    ```bash
    sacct -j job_id --format=JobID,JobName,Partition,Account,AllocCPUS,State,ExitCode
    ```

*What to look for*: Confirm that the job state is COMPLETED. If the state is FAILED, OUT_OF_MEMORY, or CANCELLED, investigate the reason (e.g., insufficient resources, errors in your script).

## 4. Analyze Job Efficiency 

Use the `seff` command to see how well your job used the allocated resources.

!!! terminal
    ```bash
    seff job_id
    ```

The output includes:
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

*What to look for*: Focus on CPU Efficiency and Memory Efficiency. These show how much of your allocated resources were actually used.

## 5. Interpret Efficiency Metrics

- **CPU Efficiency**: Shows how much of the allocated CPU time was actually used. Low values may mean your job was waiting or underutilized CPUs.
- **Memory Efficiency**: Shows how much of the allocated memory was used. Low values may mean you requested more memory than needed.

*What to look for*: High percentages (close to 100%) mean you used resources efficiently. Low percentages suggest you may be over-requesting resources.

## 6. Improve Efficiency

- If CPU or memory efficiency is low, consider reducing your resource requests in future jobs.
- If your job was killed for exceeding memory or time, request more resources next time.
- Use efficiency data to balance resource requests and job reliability.
*What to look for*: Adjust your job scripts based on the efficiency metrics to optimize future runs.

By following these steps and checking the suggested outputs, you can assess and improve the efficiency of your SLURM jobs.