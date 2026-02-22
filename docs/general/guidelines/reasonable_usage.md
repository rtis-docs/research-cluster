# Reasonable Usage

Limitations implemented through QoS policies

## Per USER

- maximum of 5000 submitted jobs in the queue.
- Up to 10 onDemand jobs may be run and are not counted in this maximum.
- A user is limited to 2 simultaneously running GPU jobs per GPU partition (extra jobs will remain in the queue)

## Per job requesting GPUs

- Each job requesting GPU resources (including through onDemand) is limited to:
    - 2 GPUs
    - 16 CPUs (8 for RTX3090 and L40_24GB jobs)
    - 150GB System Memory (60GB for RTX3090 and L40_24GB jobs)
    - a single-node

## Per CPU only job

- Each OnDemand job is limited to a run on a single node
- Numbers of simultaneous jobs, CPUS, and System memory will be limited depending on the partition as follow:

Partition | Max Simultaneous Jobs |Max CPU/Job | Max System Memory/Job
---|---|---|---
Aoraki (default) | 100 | 126 | 1000 GB
Aoraki_bigcpu |50| 252| 1500 GB
Aoraki_fastcore| 50 | 94 | 1500 GB
Aoraki_bigmem|10 | 126| 2000 GB
Aoraki_long | 25 | 252 | 2000 GB
Aoraki_short| 250 | 32 | 256 GB
Aoraki_small| 30 | 8| 32 GB
onDemand | 10 | 252 | 2000 GB



Remember the Aoraki cluster is a shared resource and as such the following guidelines will help ensure resources are available to everyone

- Try to limit how many jobs you have in the queue and any given time, we suggest less than 1000
    - Limit how many array jobs are running simultaneously by using `%N` with your `--array` parameter, e.g. `--array=1-500%20` to limit to 20 simultaneous jobs   

!!! related-pages "What's next?"
    - [Cluster Overview](../overview.md)
    - [Slurm Overview](../../getting_started/running/batch/slurm_quickstart.md)

      

