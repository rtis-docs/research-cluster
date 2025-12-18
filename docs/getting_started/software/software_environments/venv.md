# Python virtual environments

!!! overview "On this Page"
      - What is Venv used for
      - How to use Venv
      - Use of Venv vs Conda
 
  <!-- TODO See if overview is in line with content -->

## Venv

The purpose of venv is to create isolated Python environments for individual projects. This allows each project to have its own dependencies and package versions without interfering with other projects or the system-wide Python installation. It ensures cleaner organization, avoids version conflicts, and enables easy reproduction of the environment using tools like requirements.txt. This is especially useful when collaborating with others or deploying code across different systems.

1. Create a Project Directory

    !!! terminal
        ```bash
        mkdir my_project
        cd my_project
        ```

2. Create a Virtual Environment
    
    !!! terminal
        ```bash
        python -m venv venv
        ```
    This creates a venv/ folder containing the isolated Python environment.

    You can name it anything (e.g., .venv is common too).

3. Activate the Virtual Environment

    !!! terminal
        ```bash
        source venv/bin/activate
        ```

4. Install Dependencies
    
    Use pip to install libraries:

    !!! terminal
        ```bash
        pip install requests flask
        ```

5. Freeze Dependencies
    Save your dependencies:

    !!! terminal
        ```bash
        pip freeze > requirements.txt
        ```

6. Create a .gitignore (if using git)

    Prevent `venv/` from being tracked:

    !!! terminal
        ```bash
        echo venv/ __pycache__/ *.pyc >> .gitignore
        ```

7. Run Your Python App
    You can now run your scripts:

    !!! terminal
        ```bash
        python main.py
        ```
            

8. Reproducing the Environment (for others)
    To recreate the environment:

    !!! terminal
        ```bash
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```


### Comparison of venv vs conda

| Feature                         | `venv` (Standard Python)                              | `conda` (Anaconda/Miniconda)                               |
| ------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------- |
| **Purpose**                     | Create isolated Python environments                   | Manage environments **and** packages (Python + non-Python) |
| **Included With**               | Standard in Python 3.3+                               | Requires installing Anaconda or Miniconda                  |
| **Language Support**            | Python only                                           | Supports multiple languages (Python, R, Julia, etc.)       |
| **Package Manager**             | Uses `pip`                                            | Uses `conda` (can also use `pip` inside conda)             |
| **Speed of Package Resolution** | Fast for pure Python; slower for complex dependencies | Faster for scientific packages due to prebuilt binaries    |
| **System Packages**             | Installs from PyPI                                    | Installs from conda channels (e.g., conda-forge)           |
| **Non-Python Dependencies**     | Manual (e.g., via apt/brew)                           | Built-in (e.g., OpenCV, HDF5, BLAS)                        |
| **Binary/Compiled Packages**    | Not handled natively; relies on wheels from PyPI      | Conda packages are often precompiled                       |
| **Environment Reproducibility** | Via `requirements.txt`                                | Via `environment.yml`                                      |
| **Cross-Platform Consistency**  | Less consistent (due to pip building from source)     | More consistent across OSes                                |
| **Footprint**                   | Lightweight (just Python + pip)                       | Heavier (especially full Anaconda distribution)            |


!!! related-pages "What's next?"
      - See [Conda](../software_environments/conda.md) for managing environments and packages
      - Looking for something else? See [Software Overview page](../software_environments/index.md)
      -  For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
      
  <!-- TODO Are these pages the next step or relevant? -->
