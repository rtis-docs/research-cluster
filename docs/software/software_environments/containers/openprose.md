.. _openpose-apptainer:

# OpenPose


**OpenPose** is a real-time multi-person keypoint detection library developed by the CMU Perceptual Computing Lab. It supports body, face, hand, and foot pose estimation using deep learning.

It must be run on a partition/node with **GPU compute/CUDA** support and is optimized for NVIDIA GPUs, particularly A100 and H100. OpenPose processes image directories or video files and outputs pose estimations in JSON and/or image formats.

The OpenPose container is available on the cluster as a shared [Apptainer]({{apptainer}}) image, installed at: `/opt/apptainer_img/openpose.sif`



### Using the Module

You can use the `apptainer/openpose` module to load OpenPose with convenient aliases for execution:


!!! termianl 

    ```bash
    module avail openpose
    module load apptainer/openpose/1.7
    # Required if using aliases in a batch script
    shopt -s expand_aliases

    openpose --image_dir <input_folder> \
             --write_json <output_json_folder> \
             --display 0 \
             --render_pose 0
    ```


Example test run:

!!! terminal

    ```bash
    openpose --image_dir /projects/rtis/higje06p/openpose/openpose/examples/media/ \
             --write_json /projects/rtis/higje06p/openpose/output/ \
             --display 0 \
             --render_pose 0
    ```


#### Running a GPU Job on the Cluster


To run OpenPose on a GPU node interactively via SLURM:

!!! terminal

    ```bash
    srun --partition=aoraki_gpu_A100_40GB \
         --gres=gpu:1 \
         --cpus-per-task=8 \
         --mem=32G \
         --time=01:00:00 \
         --pty bash

    module load apptainer/openpose/1.7
    openpose --help
    ```

#### OnDemand Desktop GUI Use


You can also run OpenPose interactively on a GPU node via Open OnDemand:

1. Navigate to: [https://ondemand.otago.ac.nz](https://ondemand.otago.ac.nz)
2. Go to **Interactive Apps > Otago HPC Desktop (experimental)**
3. Select the following options:

   - GPU: Enabled
   - Advanced Options: De-select "Shared GPU"
   - Number of GPUs: 1
   - Partition: `aoraki_gpu_A100_40GB`
   - Cores: 4
   - Memory: 16 GB
   - Walltime: 8 hours (adjust as needed)

4. Launch the session and open a terminal in the remote desktop.

Example non-GUI container run:

!!! terminal

    ```bash
    apptainer exec --nv \
      --bind /home/$USER:/home/$USER \
      /opt/apptainer_img/openpose.sif \
      bash -c "mkdir -p /home/$USER/openpose_output/json && \
      cd /apps/openpose && \
      ./build/examples/openpose/openpose.bin \
        --video examples/media/video.avi \
        --model_folder /apps/openpose/models/ \
        --write_json /home/$USER/openpose_output/json/ \
        --render_pose 0 --display 0"
    ```

To run with GUI display enabled:

!!! terminal
    
    ```bash
    apptainer exec --nv \
      --env DISPLAY=$DISPLAY \
      --bind /tmp/.X11-unix:/tmp/.X11-unix \
      --bind /home/$USER:/home/$USER \
      /opt/apptainer_img/openpose-1.7-h100.sif \
      bash -c "cd /apps/openpose && \
      ./build/examples/openpose/openpose.bin \
        --video examples/media/video.avi \
        --model_folder /apps/openpose/models/ \
        --display 2 \
        --render_pose 1"
    ```

#### Working with Apptainer Directly


Alternatively, run OpenPose manually using `apptainer exec`. Example:

.. code-block:: bash

    apptainer exec --nv $APPTAINER_IMG/openpose.sif [command]

You must use `--nv` to enable NVIDIA GPU support.

Make sure input/output paths are within bound directories (e.g., `$HOME`, `/projects`) or manually specify them with `--bind`.

##### Common OpenPose CLI Flags


- `--image_dir <dir>`: Directory of input images
- `--video <file>`: Input video file
- `--write_json <dir>`: Output directory for JSON pose data
- `--write_images <dir>`: Output directory for rendered images
- `--write_video <file>`: Output rendered video
- `--model_folder <dir>`: Model path (in-container path: `/apps/openpose/models/`)
- `--display 0`: Disable window display
- `--render_pose 0`: Disable rendering (useful for headless performance runs)

To list all available CLI options:

.. code-block:: bash

    openpose --help

### Further Information


Refer to the official OpenPose GitHub repository for detailed documentation:

[https://github.com/CMU-Perceptual-Computing-Lab/openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

