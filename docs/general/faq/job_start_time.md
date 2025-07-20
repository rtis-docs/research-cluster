# How long do I have to wait for my job to start?


There is no guaranteed way to know the exact wait time for a SLURM job, but you can get a good estimate using SLURM commands and by checking cluster utilisation.

## Check your job in the queue:

  Use the following command to see your jobs and their status:

!!! terminal
    
    ```bash
    squeue -u $USER
    ```

  Look for the ``ST`` (state) and ``START_TIME`` columns. ``PD`` means "pending," and ``R`` means "running."

## Estimated start time:

  After submitting a job, you can check its estimated start time (if available):

!!! terminal

    ```bash
     scontrol show job <jobid> | grep StartTime
    ```

  This shows SLURM's estimated start time, but be aware that this can change as other jobs are submitted or finish.


## Tip:

  If you need your jobs to start quickly, consider requesting fewer resources (such as fewer CPUs, less memory, or a shorter time limit) or being flexible with which partition you use.

- This command can be useful to list configured and allocated resources for all nodes:

!!! terminal
    
    ```bash
    for i in {01..09} {11..12} {14..43}; do echo aoraki$i; scontrol show node aoraki$i | grep TRES; done
    ```
