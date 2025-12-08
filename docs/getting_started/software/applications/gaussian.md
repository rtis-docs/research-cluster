<!-- FIXME convert from rst to md -->

# Gaussian


Gaussian is available on Aoraki as a module.
To make it available in your shell, load it with:

!!! terminal 

    ```bash
    module load gaussian/16
    ```

This will add the g16 command to your path and set up the required environment variables.


## Interactive session

An interactive session is useful for quick tests and debugging.
The following command requests 4 CPUs, 32 GB of memory, and 1 hour of wall time on the aoraki partition:

!!! terminal

    ```bash
    srun --partition=aoraki --cpus-per-task=4 --mem=32G --time=01:00:00 --pty bash
    ```

Once connected to the compute node:

!!! terminal

    ```bash
    module load gaussian/16

    g16 water.gjf > water.log
    ```

If Gaussian writes a checkpoint file to scratch, copy it back:

!!!! terminal

    ```bash
    cp -p "$GAUSS_SCRDIR/water.chk" .
    ```

## SLURM batch job

For longer calculations, use a SLURM batch job.
Create a Gaussian input file (e.g., water.gjf) with your desired calculation settings.
Make sure to include the following lines in your input file to set the number of processors and memory: 

```text
%nprocshared=4
%mem=32GB
```

This matches the resources requested in the SLURM job script.

To submit a batch job, create a SLURM script (e.g., gaussian_job.slurm) with the following content:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=g16_water
    #SBATCH --partition=aoraki
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=32G
    #SBATCH --time=02:00:00
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err

    set -euo pipefail
    module purge
    module load gaussian/16

    export GAUSS_SCRDIR=/weka/scratch/gaussian/$USER
    mkdir -p "$GAUSS_SCRDIR"
    ulimit -s unlimited

    g16 water.gjf > water.log

    # Copy checkpoint file back if it exists
    if [ -f "$GAUSS_SCRDIR/water.chk" ]; then
        cp -p "$GAUSS_SCRDIR/water.chk" .
    fi
    ```

Submit the job with:

!!! terminal

    ```bash
    sbatch gaussian_job.slurm
    ```

Check the job status with:

!!! terminal 

    ```bash
    squeue -u $USER
    ```

After submission, the job will run in the background.

- You can monitor its progress using the SLURM commands like `squeue` or `sacct`.
- The output and error logs will be saved in the files specified by `--output` and `--error` in the SLURM script.

After the job completes, the output will be in `water.log`, and any checkpoint files will be copied back to your current directory.
You can view the output and error logs with:

!!! terminal

    ```bash
    less water.log
    ```

## Best practices

- Match resources: Set `%nprocshared` in your .gjf file to match `--cpus-per-task` in your SLURM script.
- Memory settings: Set `%mem` in the input file slightly below your SLURM `--mem` to avoid oversubscription.
- Batch for production: Use batch jobs for large calculations for better scheduling and reliability.
- Checkpoint files: If your job generates checkpoint files, ensure they are copied back to your working directory after the job completes.

## See also

- Gaussian website: https://gaussian.com/
