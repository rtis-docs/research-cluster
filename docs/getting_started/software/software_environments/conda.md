# Conda/Mamba
!!! overview "On this Page"
      - About Conda and alternatives
      - How to install Conda
      - How to do additional configurations
      - What are Conda Environments
      - How to use CUDA (GPU comupte) in Apptainer
 
  <!-- TODO See if overview is in line with content -->

## Conda

For the most up-to-date and detailed documentation please refer to the official conda documentation at [https://docs.conda.io/en/latest/](https://docs.conda.io/en/latest/)

If you are looking to only manage python packages, consider the use of [venv](venv.md) which can be simpler.

!!!note "Mamba"
    Mamba is a drop in replacement for conda which has a faster package and dependency resolver. Mamba is available if you self-install using the _miniforge_ instructions below.

### Loading Conda

Conda is available through the [module system]( {{modules}} )

!!! terminal
    ```bash
    module load miniconda3
    source $(conda info --base)/etc/profile.d/conda.sh
    ```

This will load the latest version of conda installed on the system.

!!! note

    After loading conda, `source $(conda info --base)/etc/profile.d/conda.sh` is needed to load the conda functions into your environment and needs to be done everytime the miniconda module is loaded. This is done instead of using `conda init`. The use of `conda init` is not recommended as it hard codes a specific version of conda into your bashrc which can cause issues if you are not managing the installation of conda yourself.

    This also mirrors the requirement for when using conda in a slurm script as your bashrc is not parsed as part of a SLURM job.

#### Self installing

If you would prefer to install and manage your own version of conda you can do so, we recommend using _[Miniforge](https://conda-forge.org/miniforge)_ to manage conda environments and packages.
Miniforge is a community-led, minimal conda/mamba installer that uses _[conda-forge](https://conda-forge.org/)_ as the default channel.


To install Miniforge under your user account, you can use the following commands:

!!! terminal
    ```bash
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    bash Miniforge3-Linux-x86_64.sh -b -u
    ```

Once installed (the default location is `/home/<user>/miniforge3`), load conda using:

!!! terminal

    ```bash
    source ~/miniforge3/etc/profile.d/conda.sh
    ```

!!! note

    Installing miniforge and loading as above will also give you access to `mamba` which is a drop in faster replacement to `conda`.

### Extra Configuration

#### Cache location

By default conda will download the code for packages into a cache in your home directory. It is a good idea to change this to instead be your project directory (if you have one)

!!! terminal

    ```bash
    conda config --add pkgs_dirs /path/to/project/conda_pkgs
    ```

#### Bioconda

Bioconda ([https://bioconda.github.io](https://bioconda.github.io)) is a popular repository for bioinformatic software. To be able to make use of the bioconda repository you must configure conda to know about it. The following commands are from [https://bioconda.github.io/#usage](https://bioconda.github.io/#usage) and will configure conda to search and download from the bioconda repositiory when installing into enivronments.

!!! terminal
    ```bash
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    ```

These commands modify your `~/.condarc` file.

## Conda environments

Conda environments let you manage software (and it's dependencies). Ultimately, conda install software into specific directories and then alters your `PATH` for you to make them accessible. To utilise an environment it must first exist, and then be activated. 

There are two types of environments: _named_ and _prefix_. 

- _Named_ environments are installed within your home directory (subdirectories within `~/.conda/envs`) and will let you activiate by `conda activate <environment_name>`.

- _Prefix_ environments are installed into the location you specify at creation. If this location is accessible by others, they too can use the environment. For reproducibility it is useful to create an environment in a project directory and use that for operating on data there. When you change to a different project, you can activate the corresponding environment. This lets you manage your software at the project level.

!!!note
    As named environments are stored in your home directory these can take up a large portion of your home directory storage quota. They are also not accessible to others.

    The use of _prefix_ environments is encouraged as you can specify the location to store these (ideally in your project directory)


!!! warning
    We strongly recommend against using `conda init`. It inserts a snippet in your `~/.bashrc` file that will freeze the version of conda used, bypassing the environment module system.


**Creating and activating a sub-environment**

Although once you have activated the base conda environment, you can in principle start to install packages immediately, your use of conda will generally be better organised if you do not install packages directly into the base environment, but instead use a named sub-environment.  You can have multiple sub-environments under a single base environment, and activate the one that is required at any one time.  Unless you install packages directly into the base environment, your sub-environments will work independently.

!!! information "Managing Conda Environments to Conserve Home Directory Storage"

    To save home directory storage space, it is recommended to create Conda environments in a shared project directory. 
    This approach allows you to manage your Conda environments within your project directory and if needed share them with collaborators.
    If you do not yet have a shared project directory, please contact RTIS Solutions to request one.


To create a named environment (for example, called "myenv"), ensure that the base environment is activated (the command prompt should start with "(base) "), and type:


!!! terminal "Creating Conda Environments"

    === "Prefix"
        ```bash
        conda create -p /path/to/create/environment/
        ```

    === "Named"
        ```bash
        conda create -n myenv
        ```



It will show the proposed installation location, and once you answer the prompt to proceed, will do the installation.  If you have followed these instruction, this location should be `/home/users/<your_username>/miniconda3/envs/myenv`.  You can alternatively give it a different location using the option `-p <path>` instead of `-n <name>`.

!!! warning
    Do not create conda environments in subdirectories of `/mnt/auto-hcs/` - conda will either fail or have it will have issues.


Once you have created your sub-environment, you can activate it using `conda activate <name>` for example:

!!! terminal

    === "Prefix"
        ```bash
        conda activate /path/to/conda/environment
        ```

    === "Named"
        ```bash
        conda activate myenv
        ```

The command prompt will then change (e.g. to start with "(myenv) ") to reflect this.  Typing conda deactivate once will return you to the base environment; typing it a second time will deactivate conda completely (as above).
 | To List your conda environments type the following:

!!! terminal
    ```bash
    conda env list
    ```

#### Installing conda packages

Once you have activated an environment, you can install packages with the conda install command, for example:

!!! terminal
    ```bash
    conda install gcc
    ```

You can also force particular versions to be installed.  See the conda cheat sheet for details.

To list the packages installed in the currently activated environment, you can type conda list.

#### Cleaning up

##### Cleaning Cache

Once you've made your environments it can be a good idea to clean up your cache 

!!! terminal

    ```bash
    # remove index cache, lock files, unused cache packages, tarballs, and logfiles
    conda clean --all
    ```

#### Migrating an Existing Conda Environment


To move an existing Conda environment to a new location:

1. Export your current environment to a YAML file:

    !!! terminal

        ```bash
        conda env export --name existing_env > environment.yml
        ```

2. Create a new environment from the exported YAML file at your chosen location:

    !!! terminal

        ```bash
        conda env create --prefix /path/to/project_directory/env/conda_envs/myenv --file environment.yml
        ```

3. Activate the newly created environment:

    !!! terminal
    
        ```bash
        conda activate /path/to/project_directory/env/conda_envs/myenv
        ```

#### Creating an Alias for Easy Activation


To simplify environment activation, consider adding an alias to your shell configuration file (e.g., ``.bashrc`` or ``.bash_profile``):

!!! terminal

    ```bash
    alias activate_myenv="conda activate /path/to/project_directory/env"
    ```

Activate your environment using the alias:

!!! terminal

    ```bash
    activate_myenv
    ```

This method is Python-version agnostic and provides a convenient way to manage Conda environments in shared or collaborative project directories.

##### Removing environments

If you no longer need an environment the easiest way to remove it is:

!!! terminal

    === "Prefix"
        ```bash
        conda env remove -p /path/to/env
        ```

    === "Named"
        ```bash
        conda env remove -n env_name
        ```

#### Running packages from your conda environment

In order to run packages from a conda environment that you installed previously, you will first need to activate the environment in the session that you are using.  This means repeating some of the commands typed above.  Of course, you will not need to repeat the steps to create the environment or install the software, but the following may be needed again:


!!! terminal

    ```bash
    conda deactivate

    conda activate myenv
    ```

#### Installing pip packages

Many python packages that are available via PyPI are also available as conda packages in conda-forge, and it is generally best to use these via "conda install" as above.

Nonetheless, you can also install pip packages (as opposed to conda packages) into your conda environment.  However, first you should type:

!!! terminal
    ```bash
    conda install pip
    ```

before typing the desired commands such as


!!! terminal
    ```bash
    pip install numpy
    ```

If you do not install pip into your sub-environment, then either:

your shell will fail to find the pip executable, or
your shell will find pip in your base environment, which will lead to pip packages being installed into the base environment, resulting in potential interference between your conda environments
Explicitly installing pip into your sub-environment will guard against this.    


## Using conda with SLURM


In order to use conda environments within your slurm script you need to source the conda profile script so that the conda paths get set.

!!! terminal
    
    === "Modules"

        ```bash
        module load miniconda3
        source $(conda info --base)/etc/profile.d/conda.sh
        export PYTHONNOUSERSITE=1 # don't add python user site library to path

        conda activate /path/to/env/
        ```

    === "Self installed miniforge"

        ```bash
        source ~/miniforge3/etc/profile.d/conda.sh
        export PYTHONNOUSERSITE=1 # don't add python user site library to path

        conda activate /path/to/env/
        ```

### Adding custom conda environments to Jupyter

On the commandline, first create a conda environment and install the packages/software you wish into it. 
Then add the `ipykernel` and register it with Juptyer.

!!! terminal
    
    ```bash

    conda create --path /path/to/env

    conda activate /path/to/env

    conda install <packages/software of interest>

    conda install ipykernel

    python -m ipykernel install --user --name=myCondaEnvironment
    ```
    
Then in Jupyter the custom environment can be loaded by Kernel -> Change Kernel
  
!!! related-pages "What's next?"
      - Go to [Venv](venv.md) for creating isolated Python environments.
      - Looking for something else? See [Software Overview page](../applications/index.md)
      -  For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
      
  <!-- TODO Are these pages the next step or relevant? -->
