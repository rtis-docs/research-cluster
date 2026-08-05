# Using Python with Slurm

!!! overview "On this Page"
    - Which Python to use, and why none of them arrive with NumPy
    - Building an environment once and using it from every job
    - A first batch job, and the two lines people forget
    - Using several cores without accidentally starting a thread per core in the node
    - Running one script over many inputs, and using a GPU

Python on Aoraki is deliberately plain. There is no cluster-wide scientific stack waiting to
be loaded: you build the environment your project needs, put it somewhere your jobs can
reach, and activate it at the top of every job script.

If you are new to Slurm, read the [Slurm Quickstart](../slurm_quickstart.md) first — this
page assumes you know what a job script is.

## Which Python Should I Use?

Table: The Python interpreters available on Aoraki

| Where it comes from | Versions | Use it when |
| :-- | :-- | :-- |
| `/usr/bin/python3`, always on your `PATH` | 3.9 | A short script that uses only the standard library |
| `module load python` | 3.10.8, 3.10.13, 3.13.0 (the default) | You want a particular interpreter to build a virtual environment on |
| `module load miniconda3` | whatever the environment pins | Your packages have non-Python dependencies — compilers, MKL, GDAL, bioinformatics tools |
| An Apptainer container | fixed by the image | Someone has already packaged the stack, as with `apptainer/pytorch` |

`module load python/2.7.18` also exists, for legacy code that cannot be moved. Nothing new
should use it.

!!! warning "The module gives you a bare interpreter"
    Loading a Python module gets you Python, `pip` and `venv` — and nothing else:

    !!! terminal

        ```bash
        module load python
        python3 -c "import numpy"
        ```

        ```output
        ModuleNotFoundError: No module named 'numpy'
        ```

    This catches people who expect a module system to hand over a ready-made scientific
    stack. It does not. Create an environment and install what you need into it.

### Why Not `pip install --user`

With no environment active, `pip install <package>` falls back to installing under
`~/.local/lib/python3.x/site-packages`. It works, and then causes three problems:

- **Every project on that Python version shares it**, so two analyses that need different
  versions of the same package cannot both work.
- **It counts against your home directory quota** of {{ home_quota }}. A couple of large
  packages will fill it — see [Storage and Quotas](../../../../general/faq/disk_usage.md).
- **It leaks into virtual environments.** Packages in `~/.local` are visible from inside a
  venv, so a job can succeed for reasons that are not in your environment definition and
  will not reproduce anywhere else.

Setting `PYTHONNOUSERSITE=1` in your job scripts blocks that last one. The examples below
all do.

## Building an Environment

Build it **once, on the login node**, and activate it from your job scripts. Put it in your
project directory rather than your home directory: environments are large, `/projects` is
not quota-constrained the way `/home` is, and colleagues can use an environment that lives
beside the data.

!!! terminal "Creating an environment"

    === "venv"

        ```bash
        PROJECT=/projects/sciences/biochemistry/mygroup

        module load python
        python3 -m venv $PROJECT/envs/analysis
        source $PROJECT/envs/analysis/bin/activate

        pip install --upgrade pip
        pip install numpy pandas matplotlib
        pip freeze > $PROJECT/envs/requirements.txt
        ```

    === "Conda"

        ```bash
        PROJECT=/projects/sciences/biochemistry/mygroup

        module load miniconda3
        source $(conda info --base)/etc/profile.d/conda.sh

        conda create -p $PROJECT/envs/analysis python=3.12
        conda activate $PROJECT/envs/analysis

        conda install numpy pandas matplotlib
        ```

Use a virtual environment when everything you need is on PyPI — it is smaller, faster to
build and easier to reproduce from a `requirements.txt`. Use Conda when a package needs
compiled libraries that pip would have to build from source. [Virtual
Environments](../../../software/software_environments/venv.md) and
[Conda](../../../software/software_environments/conda.md) cover each in full.

!!! note "A venv remembers the interpreter it was built with"
    A virtual environment is a thin layer over one specific Python. If you built it after
    `module load python`, load the same module in your job script before activating it.
    Skipping that gives you missing shared libraries rather than a clear error.

## Your First Python Batch Job

Two scripts: the Python you want to run, and the Slurm script that asks for resources and
runs it.

!!! python "Script: `summarise.py`"

    ```python
    import platform
    import sys

    import numpy as np

    print(f"Running on {platform.node()}")
    print(f"Interpreter: {sys.executable}")

    data = np.random.default_rng(seed=0).normal(size=1_000_000)
    print(f"mean={data.mean():.4f} sd={data.std():.4f}")
    ```

!!! terminal "Script: `run_summarise.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=summarise
    #SBATCH --partition=aoraki
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=4G
    #SBATCH --time=00:10:00

    PROJECT=/projects/sciences/biochemistry/mygroup

    module load python
    source $PROJECT/envs/analysis/bin/activate
    export PYTHONNOUSERSITE=1

    python -u summarise.py
    ```

Submit it:

!!! terminal

    ```bash
    [user@aoraki-login ~]$ sbatch run_summarise.sh
    ```

    ```output
    Submitted batch job 716
    ```

Three things in that script are worth understanding, because they are what usually goes
wrong:

- **Your `~/.bashrc` is not read by a batch job.** Anything you rely on having set up — the
  module, the environment — has to be in the script. A job that reports `ModuleNotFoundError`
  for a package you can import perfectly well in your terminal is almost always this. See
  [Why Does My Batch Job Say "command not found"](../../../../general/faq/software.md).
- **`python -u` turns off output buffering.** When Python writes to a file rather than a
  terminal it buffers output in blocks, so `print()` calls appear in `slurm-716.out` in a
  rush at the end — or not at all if the job is killed. `-u` makes progress visible as it
  happens. `export PYTHONUNBUFFERED=1` does the same thing.
- **Printing `sys.executable`** takes one line and tells you unambiguously which interpreter
  the job used. Worth keeping in any script whose environment you are still debugging.

## Using More Than One Core

Asking Slurm for cores does not make your code use them. Two separate mechanisms are
involved, and mixing them up is the most common cause of a Python job that is slower on 16
cores than on one.

### Threads Inside NumPy and SciPy

NumPy, SciPy and anything else built on OpenBLAS or MKL parallelise linear algebra
internally, choosing a thread count when they are first imported. Let them decide for
themselves and you can end up with far more threads than you have cores, all competing for
the same allocation. Set the count explicitly from what Slurm gave you:

!!! terminal "Script: `run_threaded.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=threaded
    #SBATCH --partition=aoraki
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=16G
    #SBATCH --time=01:00:00

    PROJECT=/projects/sciences/biochemistry/mygroup

    module load python
    source $PROJECT/envs/analysis/bin/activate
    export PYTHONNOUSERSITE=1

    # tell the maths libraries how many cores they actually have
    export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
    export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
    export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

    python -u matrix_work.py
    ```

Only some operations are threaded — large matrix products and decompositions are, most
element-wise work and anything in pure Python is not. If `seff` shows a CPU efficiency of
around 1/*n* for an *n*-core job, the work was not parallel and you should ask for one core.
See [Job Efficiency](../../efficiency.md).

### Parallelism You Write Yourself

For work that splits into independent pieces, use `multiprocessing` or
`concurrent.futures`. The number to give them is the number of cores Slurm allocated —
**not** `os.cpu_count()`, which reports every core in the node and will have you starting
128 processes inside an 8-core allocation.

!!! python "Script: `parallel_work.py`"

    ```python
    import os
    from concurrent.futures import ProcessPoolExecutor


    def n_allocated_cpus() -> int:
        """Cores this job may use, however it was started."""
        slurm = os.environ.get("SLURM_CPUS_PER_TASK")
        if slurm:
            return int(slurm)
        # falls back to the affinity mask, which Slurm also sets
        return len(os.sched_getaffinity(0))


    def process(sample: str) -> tuple[str, int]:
        # stand-in for the real per-sample work
        return sample, len(sample)


    if __name__ == "__main__":
        samples = [f"sample_{i:03d}" for i in range(100)]

        ncpus = n_allocated_cpus()
        print(f"Using {ncpus} worker processes", flush=True)

        with ProcessPoolExecutor(max_workers=ncpus) as pool:
            for name, result in pool.map(process, samples):
                print(f"{name}\t{result}")
    ```

!!! warning "Do not nest one kind of parallelism inside the other"
    Eight worker processes that each start eight BLAS threads is 64 threads on 8 cores, and
    it is reliably slower than doing nothing. When you parallelise in Python, set
    `export OMP_NUM_THREADS=1` in the job script and let the processes have a core each.

Both approaches stay on **one node**. `--cpus-per-task=8` asks for 8 cores on a single
machine, which is what `multiprocessing` and threaded BLAS need. Spreading Python across
several nodes needs MPI (`mpi4py`) or a distributed framework, and is worth a conversation
with us first — email {{ support_email }}.

## Running the Same Script Over Many Inputs

If you have 200 samples to process, do not submit 200 jobs in a loop. Use an
[array job](array-slurm.md): one submission, one set of resource requirements, and Slurm
runs an instance per index with `SLURM_ARRAY_TASK_ID` set.

Given a plain text file listing your inputs, one per line:

!!! terminal

    ```bash
    [user@aoraki-login ~]$ ls /projects/.../raw/*.csv > samples.txt
    [user@aoraki-login ~]$ wc -l samples.txt
    ```

    ```output
    200 samples.txt
    ```

!!! python "Script: `process_sample.py`"

    ```python
    import os
    import sys
    from pathlib import Path

    import pandas as pd

    task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])

    # line N of the sample list, counting from 1
    samples = Path("samples.txt").read_text().splitlines()
    infile = Path(samples[task_id - 1])

    print(f"Task {task_id}: {infile}", flush=True)

    df = pd.read_csv(infile)
    summary = df.describe()

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    summary.to_csv(outdir / f"{infile.stem}_summary.csv")

    print(f"Wrote {outdir / f'{infile.stem}_summary.csv'}", file=sys.stderr)
    ```

!!! terminal "Script: `run_array.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=process_samples
    #SBATCH --partition=aoraki
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=4G
    #SBATCH --time=00:20:00
    #SBATCH --array=1-200%20              # 200 tasks, at most 20 running at once
    #SBATCH --output=logs/%A_%a.out       # %A is the array job ID, %a the task ID

    PROJECT=/projects/sciences/biochemistry/mygroup

    module load python
    source $PROJECT/envs/analysis/bin/activate
    export PYTHONNOUSERSITE=1

    python -u process_sample.py
    ```

!!! terminal

    ```bash
    [user@aoraki-login ~]$ mkdir -p logs
    [user@aoraki-login ~]$ sbatch run_array.sh
    ```

The resource request applies to **each** task, not to the array as a whole: the script above
asks for one core and 4 GB two hundred times over. The `%20` throttle keeps you from filling
a partition on your own — see [Reasonable Usage](../../../../general/guidelines/reasonable_usage.md).

If a handful of tasks fail, resubmit just those indices rather than the whole array:

!!! terminal

    ```bash
    sbatch --array=17,42,108 run_array.sh
    ```

To combine the per-task outputs once the array finishes, submit a second job that depends on
it — see [Dependent Jobs](dependent_jobs.md).

## Python on a GPU

You need a GPU partition **and** a request for the GPU itself, plus a build of your framework
that was compiled against CUDA. The pip default for PyTorch is a CPU-only wheel on some
platforms, which is why so many GPU jobs quietly run on the CPU.

!!! python "Script: `gpu_check.py`"

    ```python
    import torch

    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    ```

!!! terminal "Script: `run_gpu.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=gpu_train
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gpus-per-node=1
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=32G
    #SBATCH --time=04:00:00

    PROJECT=/projects/sciences/biochemistry/mygroup

    module load python
    source $PROJECT/envs/torch/bin/activate
    export PYTHONNOUSERSITE=1

    nvidia-smi
    python -u gpu_check.py
    python -u train.py
    ```

Ask for at least two cores per GPU so the card is not left waiting on data loading. If
`torch.cuda.is_available()` returns `False` in a job that was allocated a GPU, the problem is
the installed build rather than Slurm — reinstall PyTorch from the CUDA index for the version
you need, or use the packaged container described in
[PyTorch](../../../software/applications/pytorch.md).

[Using a GPU with Slurm](gpu-slurm.md) covers the Slurm side, and
[GPU Questions](../../../../general/faq/gpu_jobs.md) covers choosing a partition, the limit
on running GPU jobs, and confirming that your code really is using the card.

## Working Interactively

Everything above assumes an unattended job. While you are still working out what the analysis
should do, use the **JupyterLab** app in
[OnDemand](../../../software/OnDemand/available_apps.md), which starts a notebook server in a
Slurm job with the resources you choose. To use one of your own environments as a kernel,
register it once:

!!! terminal

    ```bash
    source $PROJECT/envs/analysis/bin/activate
    pip install ipykernel
    python -m ipykernel install --user --name analysis --display-name "Python (analysis)"
    ```

It then appears under **Kernel → Change Kernel**. The equivalent for Conda environments is in
[Conda](../../../software/software_environments/conda.md#adding-custom-conda-environments-to-jupyter).

Move back to a batch script as soon as the work runs for more than a few minutes without your
attention — see [Interactive Jobs](../../interactive/interactive.md).

!!! related-pages "What's next?"
    - For every `#SBATCH` option and its Aoraki default, see [Job Script Options](../sbatch_options.md)
    - For environments in detail, see [Virtual Environments](../../../software/software_environments/venv.md) and [Conda](../../../software/software_environments/conda.md)
    - For many inputs, see [Array Jobs](array-slurm.md); for multi-stage workflows, see [Dependent Jobs](dependent_jobs.md)
    - To check what your job actually used, see [Job Efficiency](../../efficiency.md)
    - If a job failed, see [Why Did My Job Fail?](../../../../general/faq/slurm_job_failures.md)
