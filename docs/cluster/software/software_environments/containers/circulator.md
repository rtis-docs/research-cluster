# Circlator

Circlator is made available as an [Apptainer](apptainer.md) container. 

You can direcly run 'circlator' from the container with:

!!! terminal

    ```bash
    circlator_1.5.5.sif circlator test outdir
    ```

Alternatively you can enter an interactive shell in the container with:

!!! terminal

    ```bash
    circlator-1.5.5.sif /bin/bash
    ```

and run circlator from there.


This assumes all input and output files are located in your home directory, which gets automatically made available in the container by Apptainer. 
Other paths will have to be explicitely mapped, in which case we need to use the apptainer run command excplictely pointing to the location of the container image. 
e.g. to map the `/scratch/foo/data` directory on `/data` in the container:

!!! terminal
    
    ```bash
    apptainer run --bind /tmp/test $APPTAINER_IMAGES/circlator_1.5.5.sif circlator test /tmp/test/outdir
    ```

