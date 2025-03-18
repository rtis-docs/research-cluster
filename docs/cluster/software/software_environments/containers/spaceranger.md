# Space Ranger

Space Ranger is a set of analysis pipelines that process 10x Genomics Visium data with brightfield or fluorescence microscope images, allowing users to map the whole transcriptome in a variety of tissues.
Space Ranger v3.0 now supports Visium HD. 

Space Ranger is available on the cluster in: `/opt/spaceranger/spaceranger-3.0.1/spaceranger``

Space Ranger tutorial: [https://www.10xgenomics.com/support/software/space-ranger/latest/tutorials/count-ffpe-tutorial](https://www.10xgenomics.com/support/software/space-ranger/latest/tutorials/count-ffpe-tutorial)

To run spaceranger on the slurm cluster node create similar slurm script:

!!! terminal

    ```bash
    [account@aoraki-login spaceranger]$ cat spaceranger-slurm.sh 
    
    #!/bin/bash
    
    #SBATCH --job-name="spaceranger-16c-64g" 	 # job name
    #SBATCH --account=account                   # account       
    #SBATCH --partition=aoraki_bigcpu		 # partition to which job should be submitted
    #SBATCH --nodes=1                 		 # node count
    #SBATCH --ntasks=1                		 # total number of tasks across all nodes
    #SBATCH --cpus-per-task=16         		 # cpu-cores per task
    #SBATCH --mem=64G                  		 # total memory per node
    #SBATCH --time=0-10:00	 		 # wall time DD-HH:MM
    #SBATCH --output=/scratch/tempdir/drazentest/%x/%x_%j_%a.out
    #SBATCH --mail-user account@otago.ac.nz
    #SBATCH --mail-type BEGIN
    #SBATCH --mail-type END
    #SBATCH --mail-type FAIL

    echo "Script start"

    ## Load bcl2fastq2
    module purge
    module load bcl2fastq2

    /opt/spaceranger/spaceranger-3.0.1/spaceranger count --id="Visium_FFPE_Mouse_Brain" \
          --transcriptome=refdata-gex-mm10-2020-A \
          --probe-set=Visium_Mouse_Transcriptome_Probe_Set_v1.0_mm10-2020-A.csv \
          --fastqs=datasets/Visium_FFPE_Mouse_Brain_fastqs \
          --image=datasets/Visium_FFPE_Mouse_Brain_image.jpg \
          --slide=V11J26-127 \
          --area=B1 \
          --reorient-images=true \
          --localcores=16 \
          --localmem=64 \
          --create-bam=true

    echo "Script end"
    ```
 
As of May 30, 2024, SLURM/cgroup rules now enforce strict resource limits based on the job specifications in the SLURM script. For example, 
if your SLURM script requests 16 cores and 64 GB of RAM, the job will be restricted to these limits. Should the job exceed the 
64 GB RAM allocation, it will terminate with an "Out of memory" error. For different or larger datasets, please adjust the resource requests in your 
script accordingly to avoid such issues.

!!! terminal
    
    ```bash
    #SBATCH --cpus-per-task=16
    #SBATCH --mem=64G 
    ...

    --localcores=16 \
    --localmem=64 \
    ```

Submit slurm job:

!!! terminal
    
    ```bash
    [account@aoraki-login spaceranger]$ sbatch spaceranger-slurm.sh

    [account@aoraki-login slurm-mkdir]$ squeue --format="%.18i %.18P %.14u %.14a %.40j %.2t %.10M %.15l %.11D %.6C %.10m %.16b %.18N %.15R %15Q"|grep account
    511981   aoraki_bigcpu   account   account   spaceranger-16c-64g  R    0:05   1-10:00:00     1     16    64G       N/A      aoraki15      aoraki15 200040
    ```

After the SLURM job is done, please check the job's efficiency and adjust the script if needed.

!!! terminal

    ```bash
    [account@aoraki-login spaceranger]$ seff 511981
    ```

    ```output
    Job ID: 511981
    Cluster: aoraki
    User/Group: /lx_account
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 16
    CPU Utilized: 01:16:33
    CPU Efficiency: 31.83% of 04:00:32 core-walltime
    Job Wall-clock time: 00:15:02
    Memory Utilized: 43.62 GB
    Memory Efficiency: 68.15% of 64.00 GB
    ```

Generating FASTQs with bcl2fastq (Illumina Software)

[https://www.10xgenomics.com/support/software/cell-ranger/latest/analysis/inputs/cr-direct-demultiplexing-bcl2fastq](https://www.10xgenomics.com/support/software/cell-ranger/latest/analysis/inputs/cr-direct-demultiplexing-bcl2fastq)

bcl2fastq is available as a spack module.

!!! terminal

    ```bash
    [account@aoraki-login ~]$ module load bcl2fastq2
    [account@aoraki-login ~]$ bcl2fastq
    ```

    ```output
    BCL to FASTQ file converter
    bcl2fastq v2.20.0.422
    ```


Please refer to the Space Ranger web page for more information regarding running spaceranger.
[https://www.10xgenomics.com/support/software/space-ranger/latest](https://www.10xgenomics.com/support/software/space-ranger/latest)
