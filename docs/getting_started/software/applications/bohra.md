# Bohra

[Bohra](https://github.com/MDU-PHL/bohra) is a microbial genomics pipeline.

Bohra is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image. 

You can use the `apptainer/bohra` module which will add convenient aliases to the `bohra` binary, which will run within the container.

See the [Bohra wiki](https://github.com/MDU-PHL/bohra/wiki) for usage information.

!!! terminal

    ```bash
    module load apptainer/bohra
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    bohra test
    bohra run ......
    ```


