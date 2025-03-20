# Ollama 

[Ollama](https://ollama.com/) is a free and open source inference runtime for large language model (LLM) applications.

GPU acceleration is required for inference so it needs to be run on a **GPU** partition.

## Setup and basic operation


The container that has the Ollama software in it is called the Ollama Shell Environment. When you run it it loads up the Ollama inference server in the background and when that has loaded it then drops you into an Ubuntu 22.04 Bash shell where you can start to give commands via the command line:

!!! terminal

    ```bash
    [harsi12p@aoraki27 ~]$ ollama-env.sh
    NOTICE: Starting Ollama server in the background.
    NOTICE: Waiting for the server to come online (1/10)
    
    ## Ollama Container Shell Environment ##
    
    Any missing packages or libraries? Send requests to:
      Mail:     rtis.solutions@otago.ac.nz
      Subject:  Additions to Ollama shell environment (container_ollama_shellenv)
    
    Use the following environmental variables for this container instance:
      * OLLAMA_HOST     : 127.0.0.1:11444
      * OLLAMA_BASE_URL : http://127.0.0.1:11444
      * OLLAMA_MODELS   : /home/harsi12p/.ollama/models
      * HF_HOME         : ~/.cache/huggingface
      * OPENAI_URL_BASE : http://127.0.0.1:11444/v1
    
    Install any extra Python packages with:
      python install --user <<PACKAGE_NAME>>
    
    Press [CTRL] + [D] to exit.
    
    OllEnv harsi12p@aoraki27:~$
    ```

This has been done using a convience script called `ollama-env.sh`. Useful files such as this can be extracted from the container by running the following in an empty directory:

!!! terminal

    ```bash
    apptainer run /opt/apptainer_img/ollama_shellenv.sif --copy-execute-files
    ```

I recommend that you put ``ollama-env.sh`` in a directory that has been added to your ``PATH`` so you can call it regardless of where you are in the directory tree. If you don't want to do this you can run the container:

!!! terminal

    ```bash
    apptainer run --nv /opt/apptainer_img/ollama_shellenv.sif
    ```

The container picks an unused TCP port (not the dafault) and then starts the server on that. This is to provide isolation between different container instances.
The container sets the ``OLLAMA_HOST`` environmental variable that tells the ``ollama`` binary and Ollama python library where to send it requests. 


## Home directory quota constraints


A quota system is in place on Aoraki that limits the data in a users home directory to 15GB. This can be easy exceeded with LLM models. 
The possible solutions involve moving your data onto another storage medium (Ohau or HCS) and either setting environmental variables or copying data and then creating symlinks to the new data location. 
Other hidden directories can also contains large amount of hidden files: ``~/.cache`` and ``~/.local``. You can set the environmental variable ``OLLAMA_MODELS`` to a directory that is not in ``/home`` and Ollama will put any downloaded model files in there.


## Operation


**Command line**

Commands can be given at the command line. For example:

!!! terminal

    ```bash
    OllEnv harsi12p@aoraki27:~$ ollama run llama3
    >>> What is a cat? Give a response as a single sentence.
    A cat is a small, typically furry, carnivorous mammal of the family Felidae that purrs, scratches, and curls up in adorable ways to delight its human companions.
    >>> Send a message (/? for help) 
    ```

It may take anywhere from 10 seconds to two minutes to initially load the code and weights into VRAM. Pressing [CTRL] + [D] exits Ollama. You can use standard Unix pipes and redirection as well:

!!! terminal

    ```bash
    echo "What is a cat? Give a response as a single sentence." | ollama run llama3 > what-is-a-cat.txt
    ```

**ipython**

iPython provides syntax highlighting and completion in the terminal. For example:

!!! terminal

    ```bash
    OllEnv harsi12p@aoraki27:~$ ipython
    Python 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0]
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.26.0 -- An enhanced Interactive Python. Type '?' for help.
    
    In [1]: import ollama
    In [2]: res = ollama.generate("llama3", "What is a cat? Give a response as a single sentence.")
    In [3]: print(res["response"])
    A cat is a small, typically furry, carnivorous mammal that belongs to the family Felidae and is characterized by its agility, playful behavior, and distinctive vocalizations.
    ```

Pressing [CTRL] + [D] exits iPython. You have have to have run ``ollama run llama3`` or ``ollama pull llama3`` before you run any Python code using that LLM model.

**jupyter-notebook**

!!! terminal

    ```bash
    OllEnv harsi12p@aoraki27:~$ jupyter-notebook
    ```

Jupyter notebook pops up Firefox that is also included within the container. Because of this you have to be able to display X11 programs (through WSL on Windows and XQuartz on Mac) on your local machine. This requires a bit more setup to function correctly.

**Batch mode**
The container can also run in batch mode. This is done by giving a container a single parameter. What happens is that the container starts the Ollama server but instead of dropping you into an interractive bash shell it runs your command and then exits. For example:

!!! terminal
    
    ```bash
    apptainer run --nv /opt/apptainer_img/ollama_shellenv.sif 'echo "What is a cat? Give a response as a single sentence." | ollama run llama3 > what-is-a-cat-batched.txt'
    ```

This is useful if you have large inference jobs that you want to run and you want to use SLURM (for a significant speed and resource increase).

## Resources


LLM inference jobs are very heavy on VRAM (video card RAM) and also on CUDA cores. Under testing it was found that Ollama would only run one model in VRAM at a time. 
This would make using multiple models at the same time excruciating slow (i.e. having a standard inference and embedding model running at the same time). 
Because of this the number of models has been set to three. You can change this before you run the container by setting the following environmental variables:

!!! terminal

    ```bash
    export OLLAMA_KEEP_ALIVE=5m
    # How long to keep the model in VRAM before it is unloaded.
    
    export OLLAMA_MAX_LOADED_MODELS=3
    # How many models to have in VRAM at one time.
    
    export OLLAMA_NUM_PARALLEL=1
    # How many inference jobs to do in parallel.
    ```

You can check resource usage by using ``nvidia-smi`` and ``ollama ps``:

!!! terminal

    ```bash
    OllEnv harsi12p@aoraki27:~$ nvidia-smi
    Fri Aug 30 18:26:42 2024
    +-----------------------------------------------------------------------------------------+
    | NVIDIA-SMI 555.42.06              Driver Version: 555.42.06      CUDA Version: 12.5     |
    |-----------------------------------------+------------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
    |                                         |                        |               MIG M. |
    |=========================================+========================+======================|
    |   0  NVIDIA A100-PCIE-40GB          Off |   00000000:21:00.0 Off |                    0 |
    | N/A   27C    P0             32W /  250W |       1MiB /  40960MiB |      0%      Default |
    |                                         |                        |             Disabled |
    +-----------------------------------------+------------------------+----------------------+
    |   1  NVIDIA A100-PCIE-40GB          Off |   00000000:81:00.0 Off |                    0 |
    | N/A   26C    P0             36W /  250W |    5477MiB /  40960MiB |      0%      Default |
    |                                         |                        |             Disabled |
    +-----------------------------------------+------------------------+----------------------+
    
    +-----------------------------------------------------------------------------------------+
    | Processes:                                                                              |
    |  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
    |        ID   ID                                                               Usage      |
    |=========================================================================================|
    |    1   N/A  N/A   3034108      C   ...unners/cuda_v11/ollama_llama_server       5468MiB |
    +-----------------------------------------------------------------------------------------+
    ```

And for Ollama process information:

!!! terminal

    ```bash
    OllEnv harsi12p@aoraki27:~$ ollama ps
    NAME            ID              SIZE    PROCESSOR       UNTIL
    llama3:latest   365c0bd3c000    5.4 GB  100% GPU        4 minutes from now
    ```
