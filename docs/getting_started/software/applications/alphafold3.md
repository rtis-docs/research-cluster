<!-- FIXME: convert from rst to md -->
AlphaFold3 Module
------------


The AlphaFold3 module provides a simplified way to run AlphaFold 3 on our HPC system using an Apptainer container. This module handles all the necessary environment setup, including binding the correct database and model paths.

Loading the Module
^^^^^^^^^^^^^^^^^^
Before running AlphaFold3, you must first load the alphafold3/3.0.1 module. This command will also automatically load its dependency, the apptainer module.

.. code-block:: bash

    module load alphafold3/3.0.1

Running an AlphaFold3 Job
^^^^^^^^^^^^^^^^^^^^^^^^^
The module provides a wrapper script named af3 that simplifies the command line for running AlphaFold3. You do not need to specify any Apptainer-specific commands (:bash:apptainer exec, :bash:--bind, etc.). The af3 script handles this for you.

The basic syntax for the af3 wrapper is:

.. code-block:: bash

    af3 <path_to_input_json> <path_to_output_directory> [additional_alphafold_args]

Example: Running the Data Pipeline


To prepare the input features for a protein, you can run the data pipeline on its own. This is useful for testing or for pre-processing multiple inputs.

.. code-block:: bash

   # Example: Running the data pipeline
   af3 my_protein.json ./alphafold3_output --run_data_pipeline=true --run_inference=false

- :bash:`my_protein.json`: Your input JSON file.
- :bash:`./alphafold3_output`: The directory where the results will be saved.
- :bash:`--run_data_pipeline=true`: This flag tells AlphaFold3 to run the data preparation step.
- :bash:`--run_inference=false`: This flag tells AlphaFold3 **not** to run the full inference (folding) step, which requires the models.

Example: Running the Full Pipeline
To run the full end-to-end pipeline, including both data preparation and model inference (folding), you must ensure that the AlphaFold3 model weights have been downloaded to the path specified by the :bash:$AF3_MODELS environment variable.

.. code-block:: bash

    #Example: Running the full pipeline
    af3 my_protein.json ./alphafold3_output --run_data_pipeline=true --run_inference=true

Important Directories
The AlphaFold3 module sets up several environment variables that point to key directories. These can be helpful for understanding where data and models are located.

**$AF3_DB:** Points to the directory containing the public AlphaFold3 databases.

**$AF3_MODELS:** Points to the directory where the AlphaFold3 model weights should be stored.

**$AF3_SIF_PATH:** The full path to the Apptainer container image.

You can inspect these variables at any time by running:

.. code-block:: bash

    module show alphafold3/3.0.1

Using a GPU with SLURM
^^^^^^^^^^^^^^^^^^^^^^
To run a full AlphaFold3 job, you must request a GPU on a suitable compute node. The af3 wrapper automatically detects and uses available GPUs within the container. To submit a job to a GPU node, you should use a SLURM batch script.

Submitting a Job to the A100 or L40 Partitions
You can request a single GPU from either the a100 or l40 partitions. The :bash:--gres=gpu:1 option requests one generic GPU, and the :bash:--partition option specifies the partition you want to use.

Create a batch script (e.g., run_alphafold3.slurm) with the following content:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=af3_job
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=32G
    #SBATCH --time=24:00:00
    #SBATCH --partition=aoraki_gpu_L40    # or 'A100'
    #SBATCH --gres=gpu:1

    #Load the AlphaFold3 module
    module purge
    module load alphafold3/3.0.1

    #Run the AlphaFold3 job with the full pipeline
    af3 my_protein.json ./alphafold3_output --run_data_pipeline=true --run_inference=true

    echo "AlphaFold3 job finished."

Submit the script using the sbatch command:

.. code-block:: bash

    batch run_alphafold3.slurm

:bash:--job-name: A descriptive name for your job.

:bash:--nodes: Number of nodes to request (typically 1 for a single job).

:bash:--ntasks: Number of tasks to run (1 task per job).

:bash:--cpus-per-task: Number of CPU cores to reserve. AlphaFold3 benefits from multiple cores, especially during the data pipeline stage.

:bash:--mem: Amount of memory to reserve.

:bash:--time: Maximum wall-clock time for the job.

:bash:--partition: Specifies the partition to use (e.g., l40 or a100).

:bash:--gres=gpu:1: Requests one GPU from the specified partition.