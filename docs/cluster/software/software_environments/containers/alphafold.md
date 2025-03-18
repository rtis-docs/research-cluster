# AlphaFold

_[AlphaFold](https://github.com/deepmind/alphafold)_ is an AI system developed by DeepMind that makes 
state-of-the-art accurate predictions of a protein's structure from its amino-acid sequence.

AlphaFold is made available on the cluster as a shared [Apptainer](../apptainer) container image. 
This should be run on a **GPU Compute** partition.

You can use the `apptainer/alphafold2` module to add a convenient alias: `run_alphafold_apptainer`, which will run 
the `run_alphafold.py` within the container;
The alias will also bind-mount the AlphaFold database base path (`$AF2DB`, which is set to `/opt/alphafold_databases/`) into the container on `/db`.

To use the `run_alphafold_apptainer` alias in a non-interactive/SLURM batch script, add the following in your script before using the alias:

!!! terminal
    ```bash
    shopt -s expand_aliases
    ```

See the AlphaFold documentation for usage information. Example:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH ....
    #SBATCH ....
    module load apptainer/alphafold2
    shopt -s expand_aliases
    
    INPUT=/home/doeja01p/alphafold_test/in
    OUTPUT=/home/doeja01p/alphafold_test/out
    
    run_alphafold_apptainer \
    --use_gpu_relax \
    --fasta_paths=${INPUT}/T1050.fasta \
    --output_dir=$OUTPUT \
    --max_template_date=2020-05-14 \
    --model_preset=monomer_casp14 \
    --benchmark \
    --data_dir=/db \
    --uniref90_database_path=/db/uniref90/uniref90.fasta \
    --mgnify_database_path=/db/mgnify/mgy_clusters_2022_05.fa \
    --template_mmcif_dir=/db/pdb_mmcif/mmcif_files \
    --obsolete_pdbs_path=/db/pdb_mmcif/obsolete.dat \
    --bfd_database_path=/db/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
    --uniref30_database_path=/db/uniref30/UniRef30_2021_03 \
    --pdb70_database_path=/db/pdb70/pdb70
    ```
