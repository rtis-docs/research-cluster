# Mathematica 


## Overview


Mathematica is available on the HPC cluster via the `Environment Modules` system. The software is installed centrally in:

!!! terminal

    ```bash
    /opt/mathematica
    ```

## Loading the Module


Before using Mathematica, load the environment module:

!!! terminal

    ```bash
    module load mathematica
    ```

You can verify it is working by checking the version:

!!! terminal

    ```bash
    math -version
    ```

## Using Mathematica with SLURM


You can use Mathematica either interactively or via batch jobs.

### Interactive Job Example (srun)


To launch an interactive Mathematica session on a compute node:

!!! terminal

    ```bash
    srun --pty --ntasks=1 --cpus-per-task=1 --mem=2G --time=00:30:00 bash
    module load mathematica
    math
    ```

This starts an interactive kernel on an allocated node.

### Batch Job Example (sbatch)


To run a Mathematica script (`script.m`) in batch mode:

!!! terminal
    ```bash
    #!/bin/bash
    #SBATCH --job-name=math_batch
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=4G
    #SBATCH --time=01:00:00
    #SBATCH --output=math_output.log

    module load mathematica/14.2.1

    math -script script.m
    ```

Replace `script.m` with your actual Mathematica file.

### Using WolframScript


WolframScript allows inline evaluation or execution of `.wls` scripts:

Run code directly:

!!! terminal

    ```bash
    wolframscript -code 'FactorInteger[123456]'
    ```

Or execute a script:

!!! terminal

    ```bash
    wolframscript -file myanalysis.wls
    ```

Submitting as a batch job:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=wolframscript_job
    #SBATCH --ntasks=1
    #SBATCH --mem=2G
    #SBATCH --time=00:10:00

    module load mathematica

    wolframscript -file myanalysis.wls
    ```



For official Wolfram documentation:

https://reference.wolfram.com/language/
