# Apptainer (Singularity)
!!! overview "On this Page"
      - How to use Apptainer
      - When to use each Software Options
      - How to use Bind Mounts in Apptainer
      - How to use GUI applications in Apptainer
      - How to use CUDA (GPU comupte) in Apptainer
 
  <!-- TODO See if overview is in line with content -->

Apptainer (formerly: Singularity) is a secure, HPC-friendly alternative to [Docker](https://docker.com). 

Apptainer has its own container image format, but is generally compatible with Docker images.
 
## Basic usage

The Apptainer user guide may be found at [https://apptainer.org/docs/user/main/](https://apptainer.org/docs/user/main/) , which explains, amongst other things, how to pull down Docker images from public repositories (such as Dockerhub) and make them work with Apptainer. Email {{support_email}} if you need any help with this. 

On the Research Cluster and other RTIS-managed shared servers, pre-existing shared Apptainer images (.sif) are generally located at `$APPTAINER_IMG`. 

For convenience, shared Apptainer images may have been wrapped in a **modulefile** that will create the necessary aliases to the relevant in-container binaries, so after loading the module these binaries can then be invoked as per usual. e.g.:

!!! terminal 

    ```bash
    module avail foo
    module load apptainer/foo/0.1
    foo_bin -v
    ```

where `foo_bin` will actually be an alias to `apptainer run $APPTAINER_IMG/foo_0.1.sif foo_bin`. 
Run `alias` to display a list of all defined aliases in your shell

To use these aliases in a non-interactive script or via SLURM, add the following in your script before using the alias:

!!! terminal 

    ```bash
    shopt -s expand_aliases
    ```

Available .sif images can also be run as an executable; 
i.e.: to start a container with the default run command: `$APPTAINER_IMG/<image.sif>`
(which is identical to: `apptainer run $APPTAINER_IMG/<image.sif>`)
or alternatively add a custom command to run: `$APPTAINER_IMG/<image.sif> <command in the container>` 
or to start an interactive shell in the container: `apptainer shell $APPTAINER_IMG/<image.sif>` 


## Bind mounts

Your `$HOME` directory, `/scratch`, and `/projects` will be available within the Apptainer container by default.
Other directories/files on the host filesystem will be inaccessible from within the container, unless explicitely mounted into the container (similar to Docker's volumes). 

If you need access to other arbitrary filesystem paths, specify these with the `--bind`/`-B` option 
e.g. To start the `foo.sif` container with the host directory `/some/host_path/test` mounted on `/tmp/test` within the container:

!!! terminal
    
    ```bash
    apptainer run --bind /some/host_path/test:/tmp/test $APPTAINER_IMG/foo.sif
    ```

Refer to https://apptainer.org/docs/user/main/bind_paths_and_mounts.html#user-defined-bind-paths for additional information and examples.
 

## GUI applications

GUI applications in an Apptainer container can be remotely started from within a graphical environment (e.g. OnDemand, :doc:`X2Go </common/x2go>`, :doc:`FastX </common/fastx>`, X11-forwarded SSH session).


### GUI applications with 3D acceleration (OpenGL)

This requires 

* an execution host with GPU(s) set up with NVIDIA drivers
* a specially crafted Apptainer container image containing the necessary libraries and settings for OpenGL and VirtualGL
* the Apptainer image ran with the `--nv` flag
* a Virtual-GL capable VNC client (such as the OnDemand noVNC browser client on the Research Cluster, or a native client supporting VirtualGL (TurboVNC, TigerVNC))


### CUDA (GPU compute) support

If the node/server has NVIDIA GPU cores available, starting the Apptainer container with the `--nv` flag will setup the container’s environment to use the NVIDIA GPU and the basic CUDA libraries to run a CUDA enabled application.


!!! related-pages "What's next?"
      - Looking for something else? See [Software Overview page](../../software_overview.md)
      -  For how to run a job on the cluster go to [Running Jobs](../../../running/running_jobs_overview.md)
      
  <!-- TODO Are these pages the next step or relevant? -->