# Nextflow


[Nextflow](https://nextflow.io/) is a workflow framework that eases the writing and sharing of data-intensive computational pipelines.


## Usage on the Research Cluster

Nextflow and its dependencies can be made available with `module load nextflow`.

There are a few important steps to take to make sure the pipeline can run on the cluster and integrate with the scheduler;

* Create a global Nextflow configuration file at `$HOME/.nextflow/config` that tells nextflow to use the 'slurm' scheduler and which SLURM partition to use for 'gpu'-labeled tasks. By default Nextflow will merge this global config file with any other local nextflow.config files and parameters. 
(See [https://www.nextflow.io/docs/latest/executor.html#slurm](https://www.nextflow.io/docs/latest/executor.html#slurm) for additional SLURM options.)

```

    process {
      executor = 'slurm'
      time = 6.h
      withLabel: 'gpu' {
        queue = 'aoraki_gpu'
      }
    }
```

In your workflow's working directory, running `nextflow config -profile singularity` will show what the merged configuration looks like.

* Make sure to set the 'profile' parameter to `singularity`, or in some cases `apptainer` when running a workflow. Workflows most likely have the standard profile set to use Docker, which is not available in HPC environments.

!!! terminal

    ```bash
    nextflow run <workflow> <workflow parameters> -profile singularity
    ```


## nf-core

[https://nf-co.re/](https://nf-co.re/) is a curated set of over 100 Nextflow analysis pipelines.


## EPI2ME


[EPI2ME](https://labs.epi2me.io/) is Oxford Nanopore's data analysis platform providing a user-friendly graphical interface to running ONT's bioinformatics Nextflow pipelines, as well as other generic Nextflow pipelines.

More info [here](../../getting_started/software/onDemand/available_apps.md#epi2me-desktop).
