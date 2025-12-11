# FSL

[FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) is a library of analysis tools for FMRI, MRI and diffusion brain imaging data.

## via OnDemand

The FSL GUI tools (including FSLeyes) can be accessed via the Open OnDemand Applications. FSLeyes will be run with 3D hardware acceleration when started on a '3D-accelerated'/GPU partition (default); This should significantly improve rendering responsiveness. 

## via Apptainer

FSL is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image.
You can use the `apptainer/FSL` module to add convenient aliases to running any of the FSL binaries within the container:

!!! terminal

    ```bash
    module avail fsl
    module load apptainer/FSL/6.0.7.6
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    fsl......
    ```

Alternatively run with apptainer directly; i.e. to run binaries within the container, prefix any command with `apptainer run $APPTAINER_IMG/<apptainer_image.sif>`. 

To get an interactive shell into the container:

!!! terminal

    ```bash    
    apptainer run $APPTAINER_IMG/fsl.sif /bin/bash
    ```
    
Within the container, you'll find the FSL binaries in `/home/fsl/fsl/bin`

These can also be invoked directly within the context of the container, with:

!!! terminal

    ```bash
    apptainer run $APPTAINER_IMG/fsl.sif <fsl_binary>
    ```


## via Spack

Alternatively FSL (`fsl`) can also be self-installed using [Spack]({{spack}}).
