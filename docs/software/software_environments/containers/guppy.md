# Guppy (GPU)

Guppy is a data processing toolkit that contains the Oxford Nanopore Technologies' basecalling algorithms, and several bioinformatic post-processing features.

The GPU version of guppy is significantly faster than the CPU version, and should be run on a partition/node with CUDA (GPU compute) support.

The GPU-enabled guppy is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image. 

You can use the `apptainer/guppy` module to add a convenient alias to running `dorado` within the container.

To use any of the aliases in a non-interactive/SLURM batch script, add the following in your script before using the alias:

!!! terminal 

    ```bash
    shopt -s expand_aliases
    ```



!!! terminal
    
    ```bash
    module avail guppy
    module load apptainer/guppy-gpu/6.4.6
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    guppy_basecaller ....
    ```
    
Alternatively run with apptainer directly; i.e. To run binaries within the container, prefix any command with `apptainer run --nv <$APPTAINER_IMG/apptainer_image.sif>`. 
Make sure to specify `--nv` To enable GPU support.

!!! terminal

    ```bash
    apptainer run --nv $APPTAINER_IMG/guppy-gpu.sif guppy_basecaller <guppy options>
    ```


## Spack

Alternatively guppy (`ont-guppy`) can also be installed using [Spack]({{spack}}).
