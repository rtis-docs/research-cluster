## EPI2ME Desktop

Oxford Nanopore's [EPI2ME Desktop](https://labs.epi2me.io/about/) is a data analysis platform providing a user-friendly graphical interface to running various bioinformatics pipelines.

!!! note
    Apart from the list of ONT workflows prepopulated in the `Available Workflows` tab, EPI2ME Desktop allows for the importation of other **generic Nextflow workflows**, 
    such as the 100+ curated pipelines of []nf-core](https://nf-co.re/pipelines).
    
    Under Workflows, click `Import workflow` and copy-paste the workflow's git repository URL.
    (i.e. `https://github.com/nf-core/<wf>`)

The EPI2ME GUI can be accessed [via the Open OnDemand Applications](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_epi2me_apptainer).

* Individual pipeline tasks will be sent to the Slurm cluster scheduler and **scheduled as separate jobs** with their own allocated resources (as per the workflow defaults, or as specified in the `Nextflow configuration` tab).

* For pipelines requiring GPU compute, there is no need to run the EPI2ME OOD app on a GPU partition -In fact, the OOD app form doesn't give you that option-; Individual tasks requiring GPUs will be automatically scheduled on GPU-capable cluster nodes.

* In the EPI2ME Launch Wizard, there is also no need to change the Profile setting (in `Nextflow configuration`); This instance has been patched to default to the `singularity` profile (which uses apptainer).


To accomplish this, running the OnDemand app for the first time will automatically create the global nextflow config `$HOME/.nextflow/config` to support running the tasks via the cluster scheduler and make use of the GPU partition when appropriate. However if this file already exists, you may need to manually add this functionality:

!!! terminal
  
  ```bash
    process {
      executor = 'slurm'
      time = 6.h
      withLabel: 'gpu' {
        queue = 'aoraki_gpu'
      }
    }
  ```

!!! warning

    EPI2ME Desktop isn't designed with HPC cluster use in mind. As such we have had to devise a number of workarounds to make this work and integrate with the cluster scheduler. 
    While initial testing has been promising, the added complexity of running EPI2ME Desktop this way, as well as the application's general lack of (Nextflow) configurability *may* introduce 
    hard-to-troubleshoot issues.
    
    Consider running the workflows directly from the commandline using [Nextflow]({{nextflow}}) instead.


