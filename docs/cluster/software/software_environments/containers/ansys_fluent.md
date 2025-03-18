# Ansys Fluent

[Ansys Fluent](https://www.ansys.com/products/fluids/ansys-fluent/) is proprietary fluid simulation software.

These containers can be run on both GPU and CPU partitions. There is about a 20-30% speedup with using a GPU. They can be operated interactively (either through a text user interface or a graphical user interface) once you have logged into a node (with ``srun``) or in "batch mode" where the container can be run through the job scheduler.


The ``ansys_fluent_2022r2.sif`` container contains a full Linux installation of ANSYS Fluent 2022R2. It is designed to be operated from within the cluster. 
It does not accept network commands from the ``Parallel Settings`` or ``Remote`` section of the Fluent Launcher running from the outside of the cluster.

**Versioning**

The Fluent 2022R2 container can only open Workbench and Fluent files that are created in version 2022R2 and earlier.


## Interactive mode


The container is run in `Interactive mode` by running the container with no arguments.

The supported version (2022R2) can be run on the cluster with:

!!! terminal
    
    ```bash
    apptainer run /opt/apptainer_img/ansys_fluent_2022r2.sif
    ```

This will load into an Ubuntu Linux Bash shell environment where the user can start to issue commands:

!!! terminal
    ```bash
    [user@aorakiXX ~]$ apptainer run /opt/apptainer_img/ansys_fluent_2022r2.sif
    ```
    
    ```output
    ## ANSYS Fluent 2022R2 Container ##
    
    For debugging information export the following before running ANSYS programs:
       export ANSYS_FRAMEWORK_DEVELOPMENT=1
       export WBTracing=true
    
    Example commands:
      runwb2                        # Fluent workbench in graphical mode 
      runwb2 -B                     # Fluent workbench in text mode (enters into an IronPython shell)
      runwb2 -B -R file_name.wbjn   # Fluent workbench in text mode and run the Python 2.7 commands in file_name.wbjn
      fluent                        # Run Fluent in graphical mode
    
    Press [CTRL] + [C] to cancel a program which is currently running.
    Press [CTRL] + [D] to exit this container instance.
    
    ANSFlu user@aorakiXX:~$
    ```

A convience script called ``fluent-2022r2.sh`` has been written that simplifies loading the container. 
This and other files (SLURM examples) can be extracted from the container by running the following in an empty directory:

!!! terminal

    ```bash
    apptainer run /opt/apptainer_img/ansys_fluent_2022r2.sif --copy-execute-files
    ```

I recommend that you put ``fluent-2022r2.sh`` in a directory that has been added to your ``PATH`` so you can call it regardless of where you are in the directory tree. 


## Graphical mode

In order to use Fluent through a graphical user interface you need to be able to display X11 programs (through WSL on Windows and XQuartz on Mac) on your local machine. 
This requires a bit more setup to function correctly. If you are having issues with this please contact RTIS for support.

Note that 3D software rendering is used which is alot slower than direct hardware acceleration that would be on somebodies local machine. This means that the graphical 
interface is useful for initial setup and validation (confirming that it works) rather than for design and analysis.

To start the Fluent workbench you have to enter into the container (as mentioned above) and then type:

!!! terminal

    ```bash
    runwb2
    ```

To start Fluent directly type:

!!! terminal
    ```bash
    fluent
    ```

## Text mode


The text mode is useful for running or developing journal files for automation purposes (traditionally ending in ``.wbjn``). These are Python 2.7 scripts 
that the ANSYS IronPython runtime uses to open, initialize, initiate, save and close a simulation.

You are free to use the code developed for 'Batch mode' (see below) by having a look at the script found (within the container) at:

!!! terminal

    ```bash
    /run-files/runwb2-wbprj.py
    ```

The Python journal files can also be generated though the graphical ANSYS Workbench. This is done by enabling journalling that records your actions in the GUI.
You can then play this back in text mode. To do this (in the Workbench) goto ``File => Scripting => Record Journal...``. The workbench will then ask you for the
journal file name and start recording your actions. This ``.wbjn`` file can be modified with a text editor. The workbench automatically records your actions when 
you enable automatic journalling. To enable this goto ``Tools => Options => Journals and Logs (side menu)`` and check "Record Journal File". You can also set the 
directory here as well.

To run or 'replay' the script/journal you run the following within the container:

!!! terminal

    ```bash
    # Journal file that was recorded through the GUI:
    runwb2 -B -R file_name.wbjn
    
    # or:
    runwb2 -B -R /run-files/runwb2-wbprj.py
    ```

In the above examples, the ``-B`` operates the workbench in batch mode (text mode), i.e it does not load up the GUI. The ``-R`` runs or replays the 
script/journal file that is given (in this case: `file_name.wbjn` and `/run-files/runwb2-wbprj.py`).

There is an open source project on github that also provides another example using design points (parameterization). 
This can be found here: [https://github.com/sikvelsigma/ANSYS-WB-Batch-Script](https://github.com/sikvelsigma/ANSYS-WB-Batch-Script).


## Batch mode


The container can be run in automated `Batch mode` where it runs in text mode only (it does not display a GUI). 
You give it the path to the workbench file ``.wbpj`` as a single parameter and it initalizes and 
runs the solvers within the provided workbench file. It exits after it finishes its simulation(s).

The steps that the container goes through are:

1. Searches the directory that the ``.wbpj`` file is in and then opens it.
2. Creates a list of Solution objects that have solvers.
3. For each object with a solver it initalizes it with the chosen method (see below).
4. Once the solver has been initalized any prior simulation data is deleted/cleaned and the simulation is started.
5. Once the simulation has completed the simulation is saved and the container exits.


### Environmental variables

Environmental variables are used to control the initialization of the model before the simulation is run:

**ANSFLU_INITIALIZE_METHOD:** The ``ANSFLU_INITIALIZE_METHOD`` is used to set the inititation method. The default is "hybrid". 
There is: `none`, `hybrid`, `standard`, `custom`. The default is `hybrid`. If `custom` is set you have to define the 
TUI initalization command in the ``ANSFLU_INITIALIZE_METHOD_CUSTOM`` environmental variable.

For example: 

!!! terminal

    ```bash
    export ANSFLU_INITIALIZE_METHOD="hybrid"
    fluent-2022r2.sh projectdir/model1.wbpj
    
    # or:
    export ANSFLU_INITIALIZE_METHOD="custom"
    export ANSFLU_INITIALIZE_METHOD_CUSTOM="/solve/initialize/init-flow-statistics"
    ```


An example of a workbench based simulation run:


!!! terminal

    ```bash
    [user@aorakiXX ~]$ fluent-2022r2.sh projectdir/model1.wbpj
    ```

    ```output
    WARN: CUDA not found. NVIDIA container will operate without GPU acceleration.
    
    *******************************************
    >> OPENING: model1.wbpj @ 2024-09-05 16:12:54
    
    *******************************************
    >> ENUMERATING 'model1.wbpj'
    
       SYSTEM OBJECT:
          UserId:  Geom 3
          Caption: MX1 Geometry
          Solver:  []
    
       SYSTEM OBJECT:
          UserId:  FLTG 8
          Caption: 400k cells
          Solver:  ['FLUENT']
    
    *******************************************
    >> SOLVING SOLUTIONS
    
       * SYSTEM: FLTG 8
         > INITIALIZATION
         > INITIALIZE: Hybrid method...
         > RUNNING
    
    *******************************************
    >> COMPLETED
    
       Started:   2024-09-05 16:12:54
       Completed: 2024-09-05 16:21:10
       Duration:  0:08:16
    
    *******************************************
    >> SAVING
    
    [user@aorakiXX ~]$
    ```

There can be only a single ``.wbpj`` workbench file present in that directory at a time. 
No job completion information is given while the simulation(s) are underway.

Example SLURM files are given (see above) to submit jobs to the SLURM job manager.

## Home directory quota constraints


A quota system is in place on Aoraki that limits the data in a users home directory to 15GB. This can be easy exceeded with CFD simulations with large datasets and multiple runs. 
The possible solutions involve moving your data onto another storage medium (Ohau or HCS) and running the container from that directory. 


## Resources


Ansys Workbench Scripting Guide:
[https://dl.cfdexperts.net/cfd_resources/Ansys_Documentation/Workbench/Workbench_Scripting_Guide.pdf](https://dl.cfdexperts.net/cfd_resources/Ansys_Documentation/Workbench/Workbench_Scripting_Guide.pdf)

Fluent TUI commands (text commands within Fluent):
[https://www.afs.enea.it/project/neptunius/docs/fluent/html/ug/node48.htm](https://www.afs.enea.it/project/neptunius/docs/fluent/html/ug/node48.htm)

Journaling and Scripting within Fluent (basics):
[https://www.afs.enea.it/project/neptunius/docs/fluent/html/wbug/node45.htm](https://www.afs.enea.it/project/neptunius/docs/fluent/html/wbug/node45.htm)

Running Fluent on a different HPC cluster using SLURM:
[https://www.hkhlr.de/sites/default/files/field_download_file/HKHLR-HowTo-Ansys_Fluent.pdf](https://www.hkhlr.de/sites/default/files/field_download_file/HKHLR-HowTo-Ansys_Fluent.pdf)

Starting Parallel Ansys Fluent on a Linux System: 
[https://ansyshelp.ansys.com/public/account/secured?returnurl=//Views/Secured/corp/v242/en/flu_ug/flu_ug_parallel_start_linux_unix.html](https://ansyshelp.ansys.com/public/account/secured?returnurl=//Views/Secured/corp/v242/en/flu_ug/flu_ug_parallel_start_linux_unix.html)


