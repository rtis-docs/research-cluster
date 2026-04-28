# Dependent Jobs

Slurm allows you to specify dependencies between jobs, so that a job will only start after another job (or jobs) have finished, failed, or met other conditions. This is useful for workflows where later steps depend on the output of earlier steps.

## How Dependencies Work

You can use the `--dependency` option with `sbatch` to set dependencies. The most common type is `afterok`, which means the dependent job will start only if the specified job(s) complete successfully.

Example syntax:

!!! terminal

    ```bash
    sbatch --dependency=afterok:<jobid> second_job.sh
    ```

## Example: Simple Dependency

Submit a first job and capture its job ID:

!!! terminal

    ```bash
    jobid=$(sbatch first_job.sh | awk '{print $4}')
    ```

Then submit a second job that depends on the first:

!!! terminal

    ```bash
    sbatch --dependency=afterok:$jobid second_job.sh
    ```

## Example: Linking Array Jobs by Task ID

<!-- TODO this needs better formatting -->

Suppose you have two array jobs (see [array examples](array-slurm.md) for more about array jobs) and you want each task in the second array to depend on the corresponding task in the first array.

**first_array.sh**
!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --array=1-5
    echo "First array job, task $SLURM_ARRAY_TASK_ID"
    ```
**second_array.sh**

!!! terminal 

    ```bash 
    #!/bin/bash
    #SBATCH --array=1-5
    echo "Second array job, task $SLURM_ARRAY_TASK_ID"
    ```

Submit the first array job and capture its job ID:

!!! terminal

    ```bash
    first_jobid=$(sbatch --array=1-5 first_array.sh | awk '{print $4}')
    ```

Then submit the second array job, linking each task by its array index:

!!! terminal

    ```bash
    sbatch --array=1-5 --dependency=afterok:${first_jobid}_%a second_array.sh
    ```

Here, `%a` is replaced by the array index, so task 1 in `second_array.sh` depends on task 1 in `first_array.sh`, and so on.


This setup ensures that each corresponding task in the second array only starts after its counterpart in the first array completes successfully