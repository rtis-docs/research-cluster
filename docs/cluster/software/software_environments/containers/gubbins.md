# Gubbins

Genealogies Unbiased By recomBinations In Nucleotide Sequences - Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences.

[Gubbins](https://github.com/nickjcroucher/gubbins) is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image. 

You can use the `apptainer/gubbins` module which will add convenient aliases to Gubbins scripts, such as  `run_gubbins.py`, which will run within the container.

To use any of the aliases in a non-interactive/SLURM batch script, add the following in your script before using the alias: `shopt -s expand_aliases`.

See the [Gubbins manual](https://github.com/nickjcroucher/gubbins/blob/master/docs/gubbins_manual.md) for usage information. Example:

!!! terminal

    ```bash
    module load apptainer/gubbins
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    run_gubbins.py <FASTA alignment>
    ```
