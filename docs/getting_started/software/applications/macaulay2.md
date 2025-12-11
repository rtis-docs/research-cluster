# Macaulay2 

Macaulay2 is a software system for research in algebraic geometry and commutative algebra. It is designed to be easy to use and provides a powerful programming environment.
It is particularly well-suited for computations in algebraic geometry, commutative algebra, and related areas.

Macaulay2 is provided via an Apptainer container and can run in either **CPU** or **GPU** mode. Use the module ``macaulay2/1.24.11`` to access the environment.

## CPU Mode (Default)


Macaulay2 can run in a regular CPU environment by default. No additional configuration is needed.

Loading the Module:

!!! terminal

    ```bash
    module load macaulay2
    M2
    ```
Helper commands:

- ``M2-help`` – Show help information
- ``M2-script`` – Run a script non-interactively
- ``M2-interactive`` – Start in quiet mode (no banner)

Inside Macaulay2:

!!! terminal

    ```m2
    R = QQ[x, y]
    I = ideal(x^3 + y^2 - 1)
    gens gb I
    ```

Interactive CPU Access with srun:

To start an interactive session on a general compute node (CPU-only):

!!! terminal

    ```bash
    srun --partition=aoraki --mem=4G --cpus-per-task=2 --time=00:30:00 --pty bash
    ```
Once on the node:

!!! terminal

    ```bash
    module load macaulay2
    M2
    ```

## GPU Mode (Requires GPU Node)


To use GPU acceleration, you must be on a GPU-capable node and request a GPU using SLURM.

Set `USE_GPU=1` before loading the module to enable GPU support:

Interactive GPU Access with srun:

To run interactively on the `aoraki_gpu` partition:

!!! terminal

    ```bash
    srun --partition=aoraki_gpu --gres=gpu:1 --mem=8G --cpus-per-task=2 --time=00:30:00 --pty bash
    ```

Then:

!!! terminal

    ```bash
    export USE_GPU=1
    module load macaulay2
    M2
    ```

GPU SLURM Batch Job Example:

Create a file named ``macaulay2_gpu.slurm`` with the following content:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=m2-gpu
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gres=gpu:1
    #SBATCH --time=00:10:00
    #SBATCH --mem=4G
    #SBATCH --cpus-per-task=2
    #SBATCH --output=m2-gpu-%j.out

    export USE_GPU=1
    module load macaulay2

    M2 <<'EOF'
    R = QQ[a,b]
    I = ideal(a^4 + b^4 - 1)
    gens gb I
    EOF
    ```

Submit the job:

!!! terminal

    ```bash
    sbatch macaulay2_gpu.slurm
    ```

## Troubleshooting


- ``M2: command not found``:
  Ensure the module is loaded.

- GPU not detected:
  Make sure you set ``export USE_GPU=1`` *before* loading the module, and requested a GPU in your SLURM job.

- To verify GPU access inside the container:

!!! terminal

    ```bash
    apptainer exec --nv /opt/macaulay2/1.24.11/macaulay2.sif nvidia-smi
    ```
