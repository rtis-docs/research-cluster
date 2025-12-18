# MATLAB


## MATLAB GUI

OnDemand features a [MATLAB application](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_matlab_apptainer) using containerised builds of MATLAB including a number of popular toolboxes.

### Toolboxes

Toolboxes and addons included:

* Communications_Toolbox
* Computer_Vision_Toolbox
* Deep_Learning_Toolbox
* DSP_System_Toolbox
* Image_Acquisition_Toolbox
* Image_Processing_Toolbox
* Mapping_Toolbox
* MATLAB_Compiler
* MATLAB_Compiler_SDK
* Navigation_Toolbox
* Optimization_Toolbox
* Parallel_Computing_Toolbox
* Partial_Differential_Equation_Toolbox
* Sensor_Fusion_and_Tracking_Toolbox
* Signal_Processing_Toolbox
* Simulink
* Statistics_and_Machine_Learning_Toolbox
* Wavelet_Toolbox

### License

Use of MATLAB on the cluster is covered by the University's campus license.

### Hardware-accelerated display


If your MATLAB work involves rendering/visualisation, you may benefit from using OpenGL 3D hardware acceleration for display.

When launching the OOD app, make sure to tick the `Request GPU` and `3D hardware-accelerated display` checkbox.

To verify from within MATLAB, enter: `rendererinfo()`. The Renderer should list an NVIDIA model; If this is 'llvmpipe', you are using software rendering instead.

## Commandline MATLAB

Commandline `matlab` is available by default. Additional versions will be made available via `module` going forward.

### via SLURM


Different containerised builds of MATLAB are available in /opt/apptainer_img/ folder:

!!! terminal

  ```bash
  /opt/apptainer_img/matlab-r2018a-GL.sif
  /opt/apptainer_img/matlab-r2023b-GL.sif
  /opt/apptainer_img/matlab-r2023b.sif
  /opt/apptainer_img/matlab-r2024a-GL.sif
  /opt/apptainer_img/matlab-r2024b-GL.1.sif
  /opt/apptainer_img/matlab-r2024b-GL.sif -> matlab-r2024b-u4-GL.sif
  /opt/apptainer_img/matlab-r2024b-u4-GL.sif
  ```

Start a new slurm interactive job on the cpu node:

!!! terminal

  ```bash
  [userxyz@aoraki-login ~]$ srun --ntasks=1 --partition=aoraki --cpus-per-task=2 --time=1-01:00 --mem=20G --pty --x11=all /bin/bash
  [userxyz@rtis-hpc-r01 ~]$ apptainer shell --bind "$(pwd)":/opt/workspace,/weka/rtis/userxyz/tmp:/tmp --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif
  Apptainer> export MLM_LICENSE_FILE=27001@slo-licence-svr.registry.otago.ac.nz
  ```
  
Start matlab in gui mode (ssh connection to aoraki-login node has to have "`-X`" or "`-Y`" to enable X11 forwarding, and `srun`` command has to have "`--x11=all`":

!!! terminal
  
  ```bash
  Apptainer> matlab
  ```

Start matlab in non-gui mode:

!!! terminal
  
  ```bash
  Apptainer> matlab -nodesktop
  
  < M A T L A B (R) >
  Copyright 1984-2024 The MathWorks, Inc.
  R2024a (24.1.0.2537033) 64-bit (glnxa64)
  February 21, 2024

  To get started, type doc.
  For product information, visit www.mathworks.com.

  >>
  ```

To run a matlab script:

!!! terminal

  ```bash
  Apptainer> matlab -nodisplay < MATLAB_job.m
  ```

Start a new slurm interactive job on the gpu node:

!!! terminal

  ```bash
  [userxyz@aoraki-login ~]$ srun --ntasks=1 --partition=aoraki_gpu_H100 --nodelist=aoraki30 --cpus-per-task=1 --time=1-01:00 --gres=gpu:1 --mem=20G --pty --x11=all /bin/bash
  [userxyz@rtis-hpc-r30 ~]$ nvidia-smi
  ```

  ```output
  Wed Mar  5 12:19:20 2025
  +-----------------------------------------------------------------------------------------+
  | NVIDIA-SMI 555.42.06              Driver Version: 555.42.06      CUDA Version: 12.5     |
  |-----------------------------------------+------------------------+----------------------+
  | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
  |                                         |                        |               MIG M. |
  |=========================================+========================+======================|
  |   0  NVIDIA H100 NVL                Off |   00000000:61:00.0 Off |                    0 |
  | N/A   25C    P0             60W /  400W |       1MiB /  95830MiB |      0%      Default |
  |                                         |                        |             Disabled |
  +-----------------------------------------+------------------------+----------------------+
  
  +-----------------------------------------------------------------------------------------+
  | Processes:                                                                              |
  |  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
  |        ID   ID                                                               Usage      |
  |=========================================================================================|
  |  No running processes found                                                             |
  +-----------------------------------------------------------------------------------------+
  ```

  ```bash
  [userxyz@rtis-hpc-r30 ~]$ module load cuda/11.8
  [userxyz@rtis-hpc-r30 ~]$ apptainer shell --nv --bind "$(pwd)":/opt/workspace,/weka/rtis/userxyz/tmp:/tmp --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif
  Apptainer> export MLM_LICENSE_FILE=27001@slo-licence-svr.registry.otago.ac.nz
  Apptainer> matlab -nodesktop

  < M A T L A B (R) >
  Copyright 1984-2024 The MathWorks, Inc.
  R2024a (24.1.0.2537033) 64-bit (glnxa64)
  February 21, 2024

  To get started, type doc.
  For product information, visit www.mathworks.com.
  
  >> gpuDevice
  ```

  ```output
  ans =

  CUDADevice with properties:

                      Name: 'NVIDIA H100 NVL'
                     Index: 1
         ComputeCapability: '9.0'
            SupportsDouble: 1
     GraphicsDriverVersion: '555.42.06'
               DriverModel: 'N/A'
            ToolkitVersion: 12.2000
        MaxThreadsPerBlock: 1024
          MaxShmemPerBlock: 49152 (49.15 KB)
        MaxThreadBlockSize: [1024 1024 64]
               MaxGridSize: [2.1475e+09 65535 65535]
                 SIMDWidth: 32
               TotalMemory: 99989127168 (99.99 GB)
           AvailableMemory: 99438559232 (99.44 GB)
               CachePolicy: 'balanced'
       MultiprocessorCount: 132
              ClockRateKHz: 1785000
               ComputeMode: 'Default'
      GPUOverlapsTransfers: 1
    KernelExecutionTimeout: 0
          CanMapHostMemory: 1
           DeviceSupported: 1
           DeviceAvailable: 1
            DeviceSelected: 1
  ```

  ```bash
  >> gpuDeviceTable
  ```

  ```output
  ans =

  1x5 table

    Index          Name           ComputeCapability    DeviceAvailable    DeviceSelected
    _____    _________________    _________________    _______________    ______________

      1      "NVIDIA H100 NVL"          "9.0"               true              true
  ```

  ```bash
  >> rendererinfo()
  ```

  ```output
  ans = 

  struct with fields:

    GraphicsRenderer: 'OpenGL Software'
              Vendor: 'Mesa/X.org'
             Version: '4.5 (Compatibility Profile) Mesa 22.3.6'
      RendererDevice: 'llvmpipe (LLVM 15.0.6, 256 bits)'
             Details: [1x1 struct]
  ```

Submit a slurm batch job:

!!! terminal

  ```bash
  [userxyz@aoraki-login]$ cat /projects/userxyz/matlab.sh
  #!/bin/bash
  
  #SBATCH --job-name="matlab-xyz"                         # job name
  #SBATCH --partition=aoraki                              # partition to which job should be submitted aoraki_gpu...
  ##SBATCH --nodelist=aoraki15                            # optional node 
  ##SBATCH --gres=gpu:1                                   # optional gpu if running a gpu job on the gpu partition
  #SBATCH --nodes=1                                       # node count
  #SBATCH --ntasks=2                                      # total number of tasks across all nodes
  #SBATCH --cpus-per-task=1 		                # cpu-cores per task
  #SBATCH --mem=20G                                      # total memory per node
  #SBATCH --time=7-00:00                                  # wall time DD-HH:MM
  ##SBATCH --auks=yes                                     # optional if using HCS
  ##SBATCH --output=/projects/.../userxyz/%x/%x_%j_%a.out # optional output folder
  #SBATCH --mail-user userxyz@otago.ac.nz                 # optional email
  #SBATCH --mail-type BEGIN
  #SBATCH --mail-type END
  #SBATCH --mail-type FAIL
  
  echo "Script start"
  
  ## Export matlab licence
  export MLM_LICENSE_FILE=27001@slo-licence-svr.registry.otago.ac.nz
  
  ## GPU job
  ## apptainer exec --nv --bind "$(pwd)":/opt/workspace,/weka/rtis/userxyz/tmp:/tmp --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif matlab -nodisplay -nodesktop < MATLAB_job.m
  
  ## CPU job
  apptainer exec --bind "$(pwd)":/opt/workspace,/weka/rtis/userxyz/tmp:/tmp --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif matlab -nodisplay -nodesktop < MATLAB_job.m
  
  echo "Script end"
  ```

Submit a slurm array batch job:

!!! terminal

  ```bash

  [userxyz@aoraki-login]$ cat /projects/userxyz/matlab-array.sh
  #!/bin/bash
  
  #SBATCH --job-name="matlab-array                        # job name
  #SBATCH --partition=aoraki                              # partition to which job should be submitted aoraki_gpu...
  ##SBATCH --nodelist=aoraki15                            # optional node 
  ##SBATCH --gres=gpu:1                                   # optional gpu if running a gpu job on the gpu partition
  #SBATCH --nodes=1                                       # node count
  #SBATCH --ntasks=1                                      # total number of tasks across all nodes
  #SBATCH --cpus-per-task=1                               # cpu-cores per task
  #SBATCH --mem=20G                                       # total memory per node
  #SBATCH --array=1-8                                     # run 8 array jobs
  #SBATCH --time=0-01:00                                  # wall time DD-HH:MM
  ##SBATCH --auks=yes                                     # optional if using HCS
  ##SBATCH --output=/projects/.../userxyz/%x/%x_%j_%a.out # optional output folder
  #SBATCH --mail-user userxyz@otago.ac.nz                 # optional email
  #SBATCH --mail-type BEGIN
  #SBATCH --mail-type END
  #SBATCH --mail-type FAIL
  
  echo "Script start"
  
  ## Export matlab licence
  export MLM_LICENSE_FILE=27001@slo-licence-svr.registry.otago.ac.nz
  
  ## GPU job
  ## apptainer exec --nv --bind "$(pwd)":/opt/workspace --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif matlab -nodisplay -nodesktop -r "process_input(${SLURM_ARRAY_TASK_ID}); exit;"
  
  ## CPU job
  apptainer exec --bind "$(pwd)":/opt/workspace --pwd /opt/workspace /opt/apptainer_img/matlab-r2024a-GL.sif matlab -nodisplay -nodesktop -r "process_input(${SLURM_ARRAY_TASK_ID}); exit;"
  
  echo "Script end"
  ```

