# Array Jobs

Slurm array jobs allow you to submit many similar jobs at once, each with a unique task ID. This is useful for running the same script with different input parameters, files, or configurations. Each array task runs independently and can access its own task ID using the environment variable `SLURM_ARRAY_TASK_ID`.

## How Array Jobs Work

When you submit an array job, Slurm schedules multiple tasks, each with a different value of `SLURM_ARRAY_TASK_ID`. You specify the range of task IDs when submitting the job. For example, `--array=1-10` will run 10 tasks with IDs from 1 to 10.

Inside your job script, you can use the task ID to select input files, set parameters, or control the behavior of each task.

## Example Array Job Script

Below is an example Slurm batch script that demonstrates how to use the array task ID to process different input files:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --partition=aoraki
    #SBATCH --job-name=array_example
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=512MB
    #SBATCH --output=array_example_%A_%a.out
    #SBATCH --array=1-5

    echo "This is task ID $SLURM_ARRAY_TASK_ID"
    ```

To submit this array job, use:

!!! terminal

    ```bash
    sbatch array_example.sh
    ```

Alternatively, you can define the array size directly on the command line when submitting the job, overriding the value in the script:

!!! terminal

    ```bash
    sbatch --array=1-10 array_example.sh
    ```

This will run tasks with IDs from 1 to 10, regardless of the value set in the script.

Each task will process a different input file based on its task ID.

## Example: Using Task ID to Select a Filename from a List

Suppose you have a file called `file_list.txt` containing a list of filenames, one per line:

```text
input_a.txt
input_b.txt
input_c.txt
input_d.txt
input_e.txt
```

You can use the array task ID to select the corresponding line from this file in your Slurm script:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --partition=aoraki
    #SBATCH --job-name=array_example
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=512MB
    #SBATCH --output=array_example_%A_%a.out
    #SBATCH --array=1-5

    # Get the filename for this task by matching the task id to the line number
    FILENAME=$(sed -n "${SLURM_ARRAY_TASK_ID}p" file_list.txt)

    echo "Task ID $SLURM_ARRAY_TASK_ID will process $FILENAME"
    # Replace the following line with your actual processing command
    cat "$FILENAME"
    ```

This approach allows you to flexibly assign files to tasks based on the order in `file_list.txt`.

## Controlling the Number of Simultaneous Tasks

By default, Slurm may run all array tasks at once, depending on available resources. You can limit the number of tasks running simultaneously by adding a percent sign (`%`) and a number to the array specification. For example, `--array=1-10%3` will run at most 3 tasks at the same time.

!!! terminal

    ```bash
    # Submit an array job with 10 tasks, but only 3 running at once
    sbatch --array=1-10%3 array_example.sh
    ```

You can also set this in your batch script:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --array=1-10%3
    # ...other SBATCH options...

    echo "This is task ID $SLURM_ARRAY_TASK_ID"
    ```

This is useful for controlling resource usage and avoiding overloading the cluster.

