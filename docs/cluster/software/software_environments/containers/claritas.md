# GLOBEClaritas


[GLOBEClaritas](https://www.petrosys.com.au/claritas) is a proprietary software package for 2D and 3D land and marine seismic data processing. 

!!! warning

    This application and the OnDemand app is currently being **tested** and may not fully work as expected yet.


## License

GLOBEClaritas is licensed software. Running it on the Research Cluster will require you to bring your own network license server configuration file.

By default, both the GUI and the commandline tools will expect your `serverLicense.lic` to exist as `$HOME/.claritas/serverLicense.lic`. 
This can be overridden in the OnDemand app form, or for commandline usage by setting the `$CLARITAS_LICENSE` environment variable.


## Shared projects

By default, the **projects registry** (`projects`) will be set to `$HOME/.claritas/projects`. The OnDemand app will create a blank file for you when starting 
the app the first time; If using the commandline tools exclusively, you will need to create this file yourself (e.g. `mkdir ~/.claritas; touch ~/claritas/.projects`). 
This project registry file in your `$HOME` directory will be **accessible to your user account only**. 

For **shared projects**, a shared space with write access for all participants should be set up under `/projects`. All users should then be pointing their GLOBEClaritas 
sessions to the same :`projects` file, and any new projects should be created under the shared `/projects` space. 

In the GUI OnDemand app launch form, the path to the shared `projects` file can be specified. The OOD app will create a blank projects file at the given location on first run. 

For commandline usage, set the `$CLARITAS_PROJECTS` environment variable to the `projects` file path. This file will need to be manually created if it doesn't exist yet.


## GUI

The GUI can be accessed [via the Open OnDemand Applications](https://ondemand.otago.ac.nz/pun/sys/dashboard/batch_connect/sys/ood_claritas_apptainer).




## Commandline tools

GLOBEClaritas is made available on the cluster as a shared [Apptainer]({{apptainer}}) container image. Commandline tools have to be run within the context of the container.

You can use the `apptainer/GLOBEClaritas` module to add convenient wrapper aliases to any of the Claritas binaries. i.e.

!!! terminal

    ```bash
    module load apptainer/GLOBEClaritas
    claritas_info
    ```


The aliases will also bind-mount the GLOBEClaritas projects registry path (`$CLARITAS_PROJECTS`, which is set to `$HOME/.claritas/projects` by default) as well as the 
license server file (`$CLARITAS_LICENSE`, set to `$HOME/.claritas/serverReference.lic` by default) into the container. **Both of these files need to exist in order to run any commands in the container.**

To use aliases in a non-interactive/SLURM batch script, add the following in your script before using the alias:

!!! terminal
    
    ```bash    
    # The following is required to use aliases in a non-interactive/SLURM batch script:
    shopt -s expand_aliases
    module load apptainer/GLOBEClaritas
    ```

### Slurm

TODO

