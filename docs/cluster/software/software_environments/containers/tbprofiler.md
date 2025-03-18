# TBProfiler

TBProfiler is made available as an [Apptainer](../apptainer) container.

You can use the `apptainer/TBProfiler` module which will add convenient aliases to `tb-profiler`, which will run within the container.

To use any of the aliases in a non-interactive/SLURM batch script, add the following in your script before using the alias:

!!! terminal

    ```bash
    shopt -s expand_aliases
    module load apptainer/TBProfiler
    tb-profiler --version
    ```
