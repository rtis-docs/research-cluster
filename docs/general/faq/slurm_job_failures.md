# Jobs Failing

## Why did my job fail?


Check the job's output and error logs (e.g., `slurm-<jobid>.out`) for error messages.

You can also view a summary of job exit codes and status with:

!!! terminal

    ```bash
    sacct -j <jobid> --format=JobID,State,ExitCode
    ```


## How do I change or cancel a job after it starts running?


- To **cancel** a job, use:

!!! terminal
    
    ```bash
    scancel <jobid>
    ```

- To **change resources**, you must cancel the job and resubmit it with new resource requests.
