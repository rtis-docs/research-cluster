# DeepPoseKit

[DeepPoseKit](https://github.com/jgraving/DeepPoseKit) is a Python toolkit with a high-level API for 2D pose estimation of user-defined keypoints using deep learning.

While DeepPoseKit can be self-installed e.g. using conda as per the project's installation instructions, the legacy codebase requires a specific set of outdated 
dependencies with a supported TensorFlow/CUDA combination.
We have bundled a working environment in an [Apptainer]({{apptainer}}) container which can be launched from the [OOD JupyterLab app](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_jupyter_apptainer/) or used on the commandline.

The [project website](https://github.com/jgraving/DeepPoseKit) links to a number of notebooks detailing usage and the general workflow.

## Jupyter

The DeepPoseKit variant can be selected in the [OOD JupyterLab app](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_jupyter_apptainer/). 
For CUDA support, make sure to select a GPU/CUDA partition.

Note that the annotation GUI unfortunately cannot be run from the web-based Jupyterlab and needs to be run from an interactive graphical environment;
This can be as a Jupyter notebook on your local workstation, or a jupyter server or python session run from an [OOD desktop session](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/bc_desktop/aoraki/) (see commandline use below).

## Commandline

DeepPoseKit has an interactive graphical annotation window (cf. 'step 2') that cannot be run from the web-based OOD JupyterLab. For this purpose, you could instead start a notebook server or run the python code from a terminal in a graphical [OOD desktop session](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/bc_desktop/aoraki):

!!! terminal
    
    ```bash
    module load apptainer/deepposekit
    start-notebook.py
    ```
    
and copy-paste the full `127.0.0.1` URL displayed into the browser (Firefox) within the desktop session to access the notebook.
(e.g. `http://127.0.0.1:8888/lab?token=2edd3d93b0411e75da1a14029d3c5b23a6214b5048d11e76` )


DeepPoseKit is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image. 

You can use the `apptainer/deepposekit` module to add a convenient alias to `python` in the container:

!!! terminal
    
    ```bash
    #SBATCH <slurm job script options>
    
    module load apptainer/deepposekit
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    python -c 'import deepposekit; print(deepposekit.__version__)'
    ```


Alternatively run with apptainer directly; i.e. to run binaries within the container, prefix any command with `apptainer -s run --nv <$APPTAINER_IMG/apptainer_image.sif>`.

For CUDA support, make sure to specify `--nv`. e.g. 

!!! terminal
    
    ```bash
    apptainer -s run --nv $APPTAINER_IMG/jupyter_deepposekit_<version>.sif python
    ```