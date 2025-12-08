# PyTorch via module


This guide shows how to run **PyTorch with GPU acceleration** using the official
NVIDIA container.

## Why use this setup?


- Preinstalled PyTorch (v2.2+) with CUDA, cuDNN, and NCCL
- No need to install Conda or pip packages
- Reproducible containerized environment

## Loading the PyTorch Module


To load the PyTorch container module:

!!! terminal

   ```bash
   module load apptainer/pytorch
   ```

This provides the following helper commands:

- ``pytorch_exec``: Run a command inside the container
- ``pytorch_shell``: Open an interactive shell inside the container

### Interactive GPU Session


To run PyTorch interactively on a GPU node:

1. **Request a GPU node**

!!! terminal

   ```bash
   srun --partition=aoraki_gpu \
        --gres=gpu:1 \
        --cpus-per-task=4 \
        --mem=8G \
        --time=00:10:00 \
        --pty bash
   ```

2. **Load the module inside the GPU shell**

!!! terminal

   ```bash
   module load apptainer/pytorch/24.04
   ```

3. **Test PyTorch inside the container**

!!! terminal

   ```bash
   pytorch_exec python3 -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"
   ```

### SLURM Batch Job Example


To submit a test job to SLURM, save this to ``pytorch_test.slurm``:

!!! terminal
   
   ```bash

   #!/bin/bash
   #SBATCH --job-name=pytorch-test
   #SBATCH --partition=aoraki_gpu
   #SBATCH --gres=gpu:1
   #SBATCH --cpus-per-task=4
   #SBATCH --mem=8G
   #SBATCH --time=00:05:00

   module load apptainer/pytorch/24.04

   pytorch_exec python3 -c "
   import torch
   print('PyTorch:', torch.__version__)
   print('CUDA:', torch.cuda.is_available())
   print('GPU:', torch.cuda.get_device_name(0))
   print('cuDNN:', torch.backends.cudnn.enabled)
   print('NCCL:', torch.distributed.is_nccl_available())
   "
   ```

Submit with:

!!! terminal

   ```bash
   sbatch pytorch_test.slurm
   ```

### Running Your Own Scripts


To run your own PyTorch scripts inside the container:

!!! terminal

   ```bash
   pytorch_exec python3 my_training_script.py
   ```


