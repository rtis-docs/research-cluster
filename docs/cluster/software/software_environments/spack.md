# Spack


[Spack](https://spack.io/) is a package manager that simplifies installing and running customised scientific software stacks. With Spack, you can build a package with multiple versions, 
configurations, platforms, and compilers, and all of these builds can coexist in parallel.

A shared library of common software has been preinstalled on the Research Cluster, available to use via a [Shared read-only Spack](#shared-read-only-spack) instance or via [environment modules](../modules). 

Users wanting to install their own Spack packages should install and manage their own local Spack instance (See [User-local Spack installation](#user-local-spack-installation)).

## Shared read-only Spack {shared-spack}


!!! note
    All pre-installed Spack packages are also available by default via [environment module](../modules) without needing to use Spack.


To initialise use of the read-only shared Spack instance, run:

!!! terminal

    ```bash
    source /opt/spack/spack/share/spack/setup-env.sh
    ```

(or equivalent `setup-env` script for non-default shells)

That will make the `spack` function available, and gives you read-only access to the shared library of pre-installed packages.

You could add this to your `~/.bashrc` file (or its equivalent when not using the default bash shell and `~/.bash_profile`) to automatically source the initialisation script the next time you open a terminal session:

!!! terminal
    
    ```bash
    echo 'source /opt/spack/spack/share/spack/setup-env.sh' >> ~/.bashrc
    ```



## User-local Spack installation

In order to install Spack packages youself, you need to set up **your own Spack instance**.

* Open a terminal and with your $HOME as the current working directory, follow the [Installation instructions on the Spack website](https://spack.readthedocs.io/en/latest/getting_started.html#installation) and [source the appropriate initialisation script](https://spack.readthedocs.io/en/latest/getting_started.html#shell-support):

!!! termial

    ```bash
    cd && git clone -c feature.manyFiles=true --depth=2 https://github.com/spack/spack.git
    source ~/spack/share/spack/setup-env.sh
    ```

* The sourcing of `setup-env` may be added to your `~/.bashrc` file (or its equivalent when not using the default bash shell 
    and `~/.bash_profile`) to automatically source the initialisation script the next time you open a terminal session:

!!! terminal 

    ```bash
    echo 'source ~/spack/share/spack/setup-env.sh' >> ~/.bashrc
    ```

* We highly recommend **chaining your user-local Spack to our shared Spack**, so you can make use of and build upon the shared packages already available. 
    In order to do so, you can run the following to create the upstreams configuration file `~/.spack/upstreams.yaml`:

!!! terminal 

    ```bash
    mkdir -p ~/.spack && cat <<EOF > ~/.spack/upstreams.yaml
    upstreams:
      system-spack:
        install_tree: /opt/spack/spack/opt/spack
    EOF
    ```

* Following the above instructions, Spack packages will be installed under `~/spack/` in your home directory, which can get 
sizable and will count towards your home directory storage quota. If you have a `/projects` folder set up, Spack can alternatively 
be installed there or [set up as an alternative prefix](https://spack.readthedocs.io/en/latest/getting_started.html#optional-alternate-prefix).
 
* If you installed Spack via the recommended `git clone`, you can **keep your local Spack instance up to date** by running :code:`cd $SPACK_ROOT && git pull`


## Usage on the Research Cluster 


Please refer to the [Basic usage documentation on the Spack website](https://spack.readthedocs.io/en/latest/basic_usage.html) for a comprehensive overview and 
examples of how to query, install, load and use packages and Spack environments.

