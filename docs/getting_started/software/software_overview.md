# Software Overview

## Available Software

## Managing your own Software

### Software Environments

#### Containers

Containerization is a technology that allows you to package an application together with everything it needs to run — code, libraries, dependencies, and environment settings — into a single, portable unit called a container.

Think of a container like a lightweight, standalone mini-computer that runs consistently anywhere — on your laptop, on a server, or on a supercomputer — regardless of the underlying system.

##### Apptainer

What is Apptainer?

Apptainer (previously called Singularity) is a container platform designed specifically for High-Performance Computing (HPC) environments.

Why Apptainer over Docker in HPC?
- Docker needs root/admin access → Not allowed on most HPC clusters.
- Apptainer is designed to run containers as non-root → Safe for shared systems.

Apptainer integrates better with HPC tools (like MPI, GPUs, file systems).

What is Apptainer Good For?
- Packaging scientific software & dependencies.
- Running complex workflows reproducibly.
- Sharing pre-configured environments.
- Moving workloads between different systems easily (laptop → HPC → cloud).

#### Environments

##### LMOD/Modules

Lmod (Lua Modules) is an environment module system commonly used on High-Performance Computing (HPC) systems, clusters, and supercomputers. It helps users easily manage and switch between different software environments.

##### Conda/Mamba

Conda/mamba is an open-source package management and environment management system. It was developed to simplify installing, running, and managing software packages and their dependencies, especially for data science, machine learning, and scientific computing.

- Environments can be created locally and recreated on the research cluster
- Environments can be created per project
- Conda/Mamba manage software dependencies for reproducible research.
- Install non-Python libraries (like TensorFlow, OpenCV, etc.) easily.
    - bioconda is a great source of bioinformatic tools



##### Spack

Spack is a flexible, open-source package manager designed specifically for supercomputers, HPC clusters, and scientific computing. It helps users build, install, and manage multiple versions of scientific software and their complex dependencies.

##### SBGrid

SBGrid is a specialized software distribution and management system designed primarily for the structural biology community. It provides a curated collection of scientific software used in fields like:

- X-ray crystallography
- Cryo-electron microscopy (Cryo-EM)
- NMR spectroscopy
- Molecular modeling and visualization

##### venv

venv is a built-in Python tool (since Python 3.3) used to create virtual environments. A virtual environment is like a self-contained Python workspace — it has its own Python interpreter and its own set of installed packages, completely separate from the system Python.

Why is venv Useful?

When working on multiple Python projects:

- Different projects might need different versions of the same package.
- Installing everything globally could lead to version conflicts.

venv solves this by isolating environments.

What is venv Good For?

- Keeping project dependencies separate.
- Avoiding conflicts between package versions.
- Preventing changes to system-wide Python packages.
- Making projects easier to share & reproduce.

##### renv

`{renv}` is an R library that is used to create virtual environments of R packages. These environments can be at the user or project level and help to isolate the packages used for a project from the versions installed at a system level.

renv is useful for when you want to ensure your package versions are controlled by you, or if you want to ensure the same package versions are used across multiple devices or collaborators.

What is renv Good For?

- Keeping project dependencies separate.
- Preventing changes to system-wide R packages.
- Making projects easier to share & reproduce.