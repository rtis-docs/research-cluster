# DeepLabCut

## GUI

The DeepLabCut GUI can be accessed via the Open OnDemand Applications.
It is highly recommended to run this on a **GPU compute/CUDA** partition.

## Command line interface

DeepLabCut is made available on the cluster as a shared [Apptainer](../apptainer) container image. Scripted/commandline access requires Python to be run within the context of the container.

  * Open a terminal on one of the GPU nodes.
 
  * Start ipython in the container
  
!!! terminal
  
  ```bash
  apptainer run --nv /opt/apptainer_img/deeplabcut-2.3.9-cuda11.8.sif ipython
  ```
  
  * Then type: `import deeplabcut`
  
  * See [https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html#deeplabcut-in-the-terminal-command-line-interface](https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html#deeplabcut-in-the-terminal-command-line-interface)


### Slurm

DeepLabCut is made available on the cluster as a shared [Apptainer](../apptainer) container image. Scripted/commandline access requires Python to be run within the context of the container.

