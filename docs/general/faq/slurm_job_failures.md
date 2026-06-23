# SLURM Job Management and Troubleshooting

## How do I check the status of my job(s)?

You can use the `squeue` command to check the status of all your jobs:

!!! terminal

    ```bash
    squeue -u $USER
    ```

This will display your jobs, including job ID, partition, name, and status. The `ST` column shows the state: `PD` = Pending, `R` = Running, `CG` = Completing, etc.

## How do I see why my job is pending?

Use:

!!! terminal

    ```bash
    scontrol show job <jobid>
    ```

Look for the `Reason=` field in the output. It will tell you why the job isn't running (e.g., resources unavailable, priority, dependency).

## How do I cancel a running or pending job?

To cancel a job, use:

!!! terminal

    ```bash
    scancel <jobid>
    ```

You can find your job ID using `squeue -u $USER`.

## How do I get notified when my job finishes or fails?

Add these lines to your SLURM script:

!!! terminal

    ```bash
    #SBATCH --mail-type=END,FAIL
    #SBATCH --mail-user=your.email@domain.com
    ```

This will send an email to you when your job ends or fails.

## Where do I find the output and error logs for my job?

By default, SLURM writes standard output and error to a file named `slurm-<jobid>.out` in the directory where you submitted the job.

You can customize the output and error file names with:

!!! terminal

    ```bash
    #SBATCH --output=myjob.out
    #SBATCH --error=myjob.err
    ```

## How do I set job dependencies (e.g., run a job after another finishes)?

Use the `--dependency` option when submitting your job:

!!! terminal

    ```bash
    sbatch --dependency=afterok:<jobid> myscript.sh
    ```

This will start your job only after the specified job completes successfully.

## Why did my job fail?

Check the job's output and error logs (e.g., `slurm-<jobid>.out`) for error messages.

You can also view a summary of job exit codes and status with:

!!! terminal

    ```bash
    sacct -j <jobid> --format=JobID,State,ExitCode
    ```

## Can I extend the time limit of a running job?

SLURM jobs **cannot** be extended past their requested wall time. If your job exceeds the time limit, SLURM will **terminate** it.

### Important notes

- You cannot extend the session.
- If your code does not save progress regularly, you may lose data.
- SLURM will send a termination signal (SIGTERM, then SIGKILL) when the time limit is reached.

### Best practices

- Always write output or checkpoints regularly (for example, save to a file every few minutes or after each iteration).
- Use software that supports checkpointing or periodic saves.
- If you need more time, you can cancel and resubmit your job with a longer time limit *before* it reaches the time limit.

### Admin extensions

Only an administrator can extend the time limit of a running job. If you need to extend the time limit of a running job, you must contact an administrator. They can adjust the job's time limit if resources are available and it does not conflict with other jobs.

## How do I change or cancel a job after it starts running?

- To **cancel** a job, use:

!!! terminal
    
    ```bash
    scancel <jobid>
    ```

- To **change resources**, you must cancel the job and resubmit it with new resource requests.
