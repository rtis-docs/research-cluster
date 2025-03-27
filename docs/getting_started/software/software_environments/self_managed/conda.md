# Conda/Mamba


## Conda


### Installation

We recommend using _[Miniforge](https://conda-forge.org/miniforge)_ to manage conda environments and packages.
Miniforge is a community-led, minimal conda/mamba installer that uses _[conda-forge](https://conda-forge.org/)_ as the default channel.

!!! note

    **Due to licensing restrictions, we no longer endorse using Miniconda**. Use of Miniconda without removing the Main channel may be in violation of Anaconda's Terms of Service.

To install Miniforge under your user account, you can use the following commands:

!!! terminal
    ```bash
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    bash Miniforge3-Linux-x86_64.sh -b -u
    ```


## Conda environments


Activating the base environment.

!!! terminal
    ```bash
    source ~/miniforge3/bin/activate
    ```

Your command prompt will then change to include "(base) " at the start, in order to remind you that this environment is activated.  You can deactivate the environment by typing:

!!! terminal
    ```
    conda deactivate
    ```

**Creating and activating a sub-environment**
 |
Although once you have activated the base conda environment, you can in principle start to install packages immediately, your use of conda will generally be better organised if you do not install packages directly into the base environment, but instead use a named sub-environment.  You can have multiple sub-environments under a single base environment, and activate the one that is required at any one time.  Unless you install packages directly into the base environment, your sub-environments will work independently.

To create a named environment (for example, called "myenv"), ensure that the base environment is activated (the command prompt should start with "(base) "), and type:


!!! terminal
    ```bash
    # to create a named environment that will live in ~/.conda/envs
    conda create -n myenv

    # or you can create an environment in any* directory with
    conda create -p /path/to/put/your/environment
    ```

It will show the proposed installation location, and once you answer the prompt to proceed, will do the installation.  If you have followed these instruction, this location should be `/home/users/<your_username>/miniconda3/envs/myenv`.  You can alternatively give it a different location using the option `-p <path>` instead of `-n <name>`.
 *Note* do not create conda environments in subdirectories of `/mnt/auto-hcs/` - conda will either fail or have it will have issues.


Once you have created your sub-environment, you can activate it using `conda activate <name>` for example:

!!! terminal
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

Once you have activated a named environment, you can install packages with the conda install command, for example:

!!! terminal
    ```bash
    conda install gcc
    ```

You can also force particular versions to be installed.  See the conda cheat sheet for details.

To list the packages installed in the currently activated environment, you can type conda list.

#### Running packages from your conda environment

In order to run packages from a conda environment that you installed previously, you will first need to activate the environment in the session that you are using.  This means repeating some of the commands typed above.  Of course, you will not need to repeat the steps to create the environment or install the software, but the following may be needed again:


!!! terminal

    ```bash
    source activate

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
    
    ```bash
    source ~/miniforge3/etc/profile.d/conda.sh
    export PYTHONNOUSERSITE=1 # don't add python user site library to path

    conda activate myenv
    ```

### Adding custom conda environments to Jupyter

.. include:: /common/jupyter_kernels.rst
  :start-line: 2
  
