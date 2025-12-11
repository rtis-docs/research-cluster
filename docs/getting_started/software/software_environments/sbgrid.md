# SBGrid

!!! overview "On this Page"
      - What is SBGrid
      - How to use SBGrid
      - More information on SBGrid
 
  <!-- TODO See if overview is in line with content -->

SBGrid offers a comprehensive package of scientific software that is regularly updated and available on the cluster. 
It includes both module files and SBGrid's proprietary software loading utility. 
Currently, the suite comprises 543 applications, with multiple versions of each to accommodate the diverse needs of users. 
The SBGrid Consortium, which operates out of Harvard Medical School, is a research computing group funded by member research laboratories. 
It provides essential computing support to the global structural biology community.


**Note: SBGrid users MUST be registered with the SBGrid Consortium to use this software package.**

1. To sign up for SBGrid access, simply go to the [SBGrid Registration Page](https://www.sbgrid.org/members/registration/).
2. Take note of the SBGrid License Agreement.
3. Fill out the registration form.
4. Take a screenshot of your completed registration acknowledgement.
5. Send the screenshot to rtis.solutions.team@otago.ac.nz. 
6. *This process must be done for each lab.*



[SBGrid Information WIKI](https://sbgrid.org/wiki)
 
## SBGrid on the Research Cluster


### Modules

To use SBGrid via modules, use the following command `export MODULEPATH=/programs/share/modulefiles/x86_64-linux:"$MODULEPATH"` 

!!! note
    To make this permanent, add the above command to your `.bashrc`

Module Examples:
Once the modulepath is loaded as above `module avail` will list all modules including SBGrid, Spack, and RTIS custom modules 

`module spider alphafold` will search for all module packages include the SBGrid packages

!!! terminal

    ```bash
    module spider alphafold
    ```

    ```output
    sbgrid/alphafold:
     Versions:
        sbgrid/alphafold/2.1.2
        sbgrid/alphafold/2.2.0
        sbgrid/alphafold/2.2.2
        sbgrid/alphafold/2.2.3
        sbgrid/alphafold/2.2.4
        sbgrid/alphafold/2.3.0
        sbgrid/alphafold/2.3.1
        sbgrid/alphafold/2.3.2_20241024
        sbgrid/alphafold/2.3.2
        sbgrid/alphafold/3.0.0_20241202_aa724ca
        sbgrid/alphafold/3.0.0
    ```


To load the SBGrid software simply type `module load sbgrid/alphafold`. This will load the default version of the software.

To load a specific version use `module load sbgrid/alphafold/2.1.2`

To show which versions are loaded `module list`


### SBgrid Tools

To use SBGrid Tools, execute the following command `source /programs/sbgrid.shrc`  
 
!!! note
    To make this permanent, add the above command to your `.bashrc`



To load SBGrid software using the **SBGrid tools** instead of modules see
[SBGrid Getting Started](https://sbgrid.org/wiki/getting_started) 

`source /programs/sbgrid.shrc`

Once you are in the SBGrid environment you can use all SBGrid commands.

[https://sbgrid.org/wiki/examples](https://sbgrid.org/wiki/examples)

[SBGrid youtube](https://www.youtube.com/user/SBGridTV)
 
!!! related-pages "What's next?"
      - Looking for something else? See [Software Overview page](../)
      -  For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
      
  <!-- TODO Are these pages the next step or relevant? -->
