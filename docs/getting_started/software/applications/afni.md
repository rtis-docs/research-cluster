# AFNI (Analysis of Functional NeuroImages)

https://afni.nimh.nih.gov

For customising the behaviour of AFNI tools with a `~/.afnirc` config or via environment variables, see [https://afni.nimh.nih.gov/pub/dist/doc/program_help/README.environment.html](https://afni.nimh.nih.gov/pub/dist/doc/program_help/README.environment.html)

## GUI

The AFNI GUI can be accessed via the Open OnDemand Applications - [https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_afni_apptainer](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_afni_apptainer).

## Command line

The AFNI suite is made available on the cluster as a shared [Apptainer]( {{ apptainer }} ) container image. 
Binaries and scripts are run within the context of the container.

You can use the `apptainer/AFNI` module to add convenient aliases to running any of the AFNI binaries and scripts within the container:

!!! terminal

    module avail afni
    module load apptainer/AFNI
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    afni......

Alternatively run with apptainer directly; i.e. to run binaries within the container, prefix any command with `apptainer run $APPTAINER_IMG/<apptainer_image.sif>`. 

To get an interactive shell into the container:


!!! terminal
    
    apptainer run $APPTAINER_IMG/afni_24.2.03.sif /bin/bash


Within the container, you'll find the AFNI binaries and scripts in `/opt/afni/install`

These can also be invoked directly within the context of the container, with:


!!! terminal

    apptainer run $APPTAINER_IMG/afni_24.2.03.sif <command> 


