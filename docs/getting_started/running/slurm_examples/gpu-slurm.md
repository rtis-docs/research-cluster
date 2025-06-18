# Using a GPU with Slurm

These examples can be found at https://appsgit.otago.ac.nz/projects/RTIS-SP/repos/slurm-code-examples/browse

Or downloaded and browsed on the cluster by:

!!! terminal

    ```bash
    git clone https://appsgit.otago.ac.nz/scm/rtis-sp/slurm-code-examples.git
    ```



The key things to remember are:

 * Submit to a partition with nodes with GPUs
 * Include the ``--gres`` flag.
 * Request at least two CPUs for each GPU requested, using ``--cpus-per-task``
 * You can request multiple GPUs with syntax like this (in this case for two
   GPUs): ``--gpus-per-node=2``
 * The partition is used to specify a specific GPU, or how much GPU memory is needed
    - aoraki_gpu will get you any free GPU
    - aoraki_gpu_H100 will get you an entire H100 with 80 GB of GPU memory
    - aoraki_gpu_L40 will get you an entire L40 with 48GB of GPU memory
    - aoraki_gpu_A100_80GB will get you an A100 with 80GB of GPU memory to use
    - aoraki_gpu_A100_40GB will get you an A100 with 40GB of GPU memory to use

!!! note 

    You may see some scripts use a command line ``--gres=gpu:2`` to specify two
    GPUS. This way of specifying the number of GPUs to use is in the process of
    being deprecated.

Running a GPU job on Slurm involves specifying the required resources and
submitting the job to the scheduler.
Here are the basic steps to run a GPU job on Slurm:

 1. Request the required resources.
    In order to run a GPU job on Slurm, you need to specify the number of GPUs
    and the amount of memory required.
    For example, to request a single GPU with 16GB of CPU memory, you would add the
    following line to your Slurm job script:

    !!! terminal
    
        ```bash
        #SBATCH --gpus-per-node=1
        #SBATCH --mem=16GB # 16 GB CPU Memory
        ```

 2. Load the necessary modules.
    Depending on the software and libraries you are using you may need to load
    additional modules to access the GPU resources. 
    This can usually be done using the module load command. 
    For example, to load the CUDA toolkit:

    !!! terminal
    
        ```bash
        lua
        module load cuda
        ```

 3. Write the job script.
    Create a job script that specifies the commands and arguments needed to run
    your GPU job.
    This can include running a CUDA program, a TensorFlow script, or any other
    GPU-accelerated code.

 4. Submit the job.
    Use the sbatch command to submit the job script to the Slurm scheduler.
    For example:

    !!! terminal
    
        ```bash
        sbatch my_gpu_job.sh
        ```
      
    Once your job is submitted, Slurm will allocate the requested resources and
    schedule the job to run on a node with the appropriate GPU.
    You can monitor the status of your job using the squeue command and view
    the output using the sacct command once the job completes.

Here's an example script that will return the information on the GPU available
on ``aoraki_gpu``:


!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --account=account_name
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gpus-per-node=1
    #SBATCH --mem=4GB
    #SBATCH --time=00:00:30
    nvidia-smi
    ``` 

!!! hint
   
    If you want to run a GPU job interactively you can create slurm session on a gpu node (Partition aoraki_gpu_L40 in this example) using the following command which simply adds the ``--gres=gpu:1`` flag to the ``srun`` command:

    ``srun --ntasks=1 --partition=aoraki_gpu_L40 --gres=gpu:1  --cpus-per-task=4 --time=0-03:00 --mem=50G --pty  /bin/bash``


For a slightly more involved example consider the following C code.

!!! terminal

    ```c

    #include<stdio.h>

    #define BLOCKS 2
    #define WIDTH 16

    __global__ void whereami() {
      printf("I'm thread %d in block %d\n", threadIdx.x, blockIdx.x);
    }

    int main() {
      whereami<<<BLOCKS, WIDTH>>>();
      cudaDeviceSynchronize();
      return 0;
    }
    ```

If this is stored in the file ``whereami.cu`` and compiled with 
``nvcc whereami.cu -o whereami`` we can use the Slurm job script

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --account=account_name
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gpus-per-node=1
    #SBATCH --mem=4GB
    #SBATCH --time=00:00:30
    whereami
    ```

to obtain output such as the following (ordering of lines may differ):

!!! terminal

    ```output
    I'm thread 0 in block 1 
    I'm thread 1 in block 1 
    I'm thread 2 in block 1 
    I'm thread 3 in block 1 
    I'm thread 4 in block 1 
    I'm thread 5 in block 1 
    I'm thread 6 in block 1 
    I'm thread 7 in block 1 
    I'm thread 8 in block 1 
    I'm thread 9 in block 1 
    I'm thread 10 in block 1 
    I'm thread 11 in block 1 
    I'm thread 12 in block 1 
    I'm thread 13 in block 1 
    I'm thread 14 in block 1 
    I'm thread 15 in block 1 
    I'm thread 0 in block 0 
    I'm thread 1 in block 0 
    I'm thread 2 in block 0 
    I'm thread 3 in block 0 
    I'm thread 4 in block 0 
    I'm thread 5 in block 0 
    I'm thread 6 in block 0 
    I'm thread 7 in block 0 
    I'm thread 8 in block 0 
    I'm thread 9 in block 0 
    I'm thread 10 in block 0 
    I'm thread 11 in block 0 
    I'm thread 12 in block 0 
    I'm thread 13 in block 0 
    I'm thread 14 in block 0 
    I'm thread 15 in block 0
    ```
