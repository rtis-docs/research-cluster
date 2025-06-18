# Research HPC Cluster (Aoraki)


Shared computing resources available to Otago researchers include high performance computing, fast storage, GPUs and virtual servers.



## Otago Resources


The RTIS Research cluster provides researchers with access to shared resources, such as **CPUs, GPUs, and high-speed storage**. 
Also available are specialised software and libraries optimised for scientific and datascience computing. 

If you need special software or configurations please ask the RTIS team at rtis.solutions@otago.ac.nz

## Cluster Overview

![](/assets/images/cluster_photo.jpg)


We offer a variety of SLURM partitions based on different resource needs. The default partition provides balanced compute and memory capabilities. Additional partitions include those optimized for GPU usage and those with expanded memory capacity. On every cluser node there are 2 cores reseved for the OS (weka storage), reducing the available compute cores by 2.  


{{ read_csv('docs/assets/tables/partitions.csv') }}


- **Partition**: Name of the partition, with an asterisk (*) denoting the default partition. Aoraki_small and aoraki_short are specialized partitions that utilize typically idle CPU cores on GPU nodes, designed to handle small or short-duration jobs efficiently. 
- **Time Limit**: Maximum time a job can run in that partition. The time limit for running jobs can be extended upon request. In such cases, the extended time limit may exceed the partition's standard wall time.
- **Nodes**: Number of nodes available in the partition.
- **Nodelist**: The specific nodes allocated to that partition.
- **Max Cores per Node**: Maximum number of CPU cores available on a node.
- **Max Memory (MB) per Node**: The maximum amount of memory (in MB) available on each node in partition.
- **GRES per Node**: Generic Resources (e.g., GPUs) available in the partition.


{{ read_csv('docs/assets/tables/specs.csv') }}


