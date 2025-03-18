# ColabFold

Easy to use protein structure and complex prediction using AlphaFold2 and Alphafold2-multimer.

Local [ColabFold](https://github.com/sokrypton/ColabFold) is made available on the cluster as a shared [Apptainer](../apptainer) container image. 
This should be run on a **GPU Compute** partition.

You can use the `apptainer/colabfold` module which will add convenient aliases for: `colabfold_batch`, 
`colabfold_search`, `colabfold_split_msas`, which will run within the container;
The alias will also bind-mount the AlphaFold2 weights cache path (`/opt/colabfold/alpha2_weights_cache` on the nodes) into 
the container on `/cache`.

See the [LocalColabFold documentation](https://github.com/YoshitakaMo/localcolabfold) for usage information. Example:

!!! terminal

    ```bash
    module load apptainer/colabfold
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    colabfold_batch ./input.fasta ./out/
    ```


An example Slurm script to run ColabFold on the cluster is provided below:

!!! terminal

    ```bash
    #!/bin/bash
 
    #SBATCH --job-name=colabfold    # Job name
    #SBATCH --partition=aoraki_gpu  # Partition (queue) name
    #SBATCH --nodes=1               # Number of nodes
    #SBATCH --ntasks-per-node=1     # Number of tasks (1 task per node)
    #SBATCH --cpus-per-task=12      # Number of CPU cores per task
    #SBATCH --gres=gpu:1            # Number of GPUs required
    #SBATCH --mem=96G               # Job memory request
    #SBATCH --time=10:00:00         # Time limit hrs:min:sec
    #SBATCH --mail-user=USERNAME@otago.ac.nz
    #SBATCH --output=colabfold%j.log # Standard output log
    
    # Set variables
    base_name="$1"
    output_fasta="${base_name}_getorf.output.fa"
    
    # Load the apptainer/colabfold module (assuming it's in your PATH)
    module load apptainer/colabfold

    shopt -s expand_aliases  # Enable alias expansion
    
    # Check loaded modules (for debugging)
    module list
    
    # Ensure PATH includes module binaries (for debugging)
    echo "Current PATH: $PATH"
    
    # Run colabfold_batch command using alias
    colabfold_batch "./$output_fasta" ./out/
    ```