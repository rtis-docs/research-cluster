# ORCA


ORCA is a general-purpose quantum chemistry program package that features virtually all modern electronic structure methods. It is available on Aoraki as a module.

To make it available in your shell, load it with:

!!! terminal

    ```bash
    module load orca/6.1.0
    ```

This will add the ORCA executables to your path and set up the required environment variables.


## Interactive session

An interactive session is useful for quick tests and debugging.
The following command requests 4 CPUs, 16 GB of memory, and 1 hour of wall time on the aoraki partition:

!!! terminal

    ```bash
    srun --partition=aoraki --cpus-per-task=4 --mem=16G --time=01:00:00 --pty bash
    ```

Once connected to the compute node:

!!! terminal

    ```bash
    module load orca/6.1.0
    orca water.inp > water.out
    ```

ORCA will automatically use the number of CPUs allocated to your job.


## SLURM batch job

For longer calculations, use a SLURM batch job.
Create an ORCA input file (e.g., water.inp) with your desired calculation settings.

Example ORCA input file:


    ```text

    ! B3LYP def2-TZVP OPT FREQ
    %pal nprocs 4 end
    %maxcore 4000

    * xyz 0 1
    O  0.000000  0.000000  0.000000
    H  0.757000  0.587000  0.000000
    H -0.757000  0.587000  0.000000
    *
    ```

Make sure the `nprocs` value matches the `--cpus-per-task` in your SLURM script, and set `%maxcore` appropriately for your memory allocation.

To submit a batch job, create a SLURM script (e.g., orca_job.slurm) with the following content:

!!! terminal

    ```bash

    #!/bin/bash
    #SBATCH --job-name=orca_water
    #SBATCH --partition=aoraki
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err

    set -euo pipefail
    module purge
    module load orca/6.1.0


    # Run ORCA
    orca water.inp > water.out

    # Copy important files back if needed
    if [ -f "water.gbw" ]; then
        cp water.gbw "$SLURM_SUBMIT_DIR/"
    fi
    ```

Submit the job with:

!!! terminal

    ```bash
    sbatch orca_job.slurm
    ```

Check the job status with:

!!! terminal

    ```bash
    squeue -u $USER
    ```

Monitor the calculation progress by checking the output file:

!!! terminal

    ```bash
    tail -f water.out
    ```


### Best practices

- **Match resources**: Set `nprocs` in your .inp file to match `--cpus-per-task` in your SLURM script.
- **Memory settings**: Set `%maxcore` to about 80% of your total memory divided by the number of cores (in MB).
- **Scratch space**: ORCA can generate large temporary files. The script above sets up a scratch directory.
- **File management**: Copy important output files (.gbw, .xyz, .hess) back to your working directory.
- **Parallel efficiency**: ORCA scales well up to 8-16 cores for most calculations.

### Common ORCA keywords

- **DFT methods**: B3LYP, PBE0, M06-2X, wB97X-D3
- **Basis sets**: def2-SVP, def2-TZVP, def2-QZVP, cc-pVDZ, cc-pVTZ
- **Job types**: OPT (optimization), FREQ (frequencies), SP (single point)
- **Advanced**: CCSD(T), CASSCF, NEVPT2

### Example input files


Single point energy calculation:

    ```text
    ! B3LYP def2-TZVP
    %pal nprocs 4 end

    * xyz 0 1
    C  0.000000  0.000000  0.000000
    H  1.070000  0.000000  0.000000
    H -0.356667  1.008971  0.000000
    H -0.356667 -0.504485  0.874151
    H -0.356667 -0.504485 -0.874151
    *
    ```

Geometry optimization with frequencies:


    ```text

    ! B3LYP def2-TZVP OPT FREQ
    %pal nprocs 4 end
    %maxcore 4000

    * xyz 0 1
    C  0.000000  0.000000  0.000000
    O  1.200000  0.000000  0.000000
    *
    ```

## See also

- ORCA website: [https://orcaforum.kofo.mpg.de/](https://orcaforum.kofo.mpg.de/)
- ORCA manual: Available through the module documentation
