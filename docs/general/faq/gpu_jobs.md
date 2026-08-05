# GPU Questions

!!! overview "On this Page"
    - Choosing a GPU partition
    - Why a GPU job waits even when nodes look free
    - The partitions that need access granted first
    - Checking that your code is really using the GPU, and asking for part of one

## Which GPU Partition Should I Use?

Every GPU model has its own partition, and there is a general pool that takes whichever of
its nodes is free first.

Table: GPU partitions and what is in them

| Partition | GPUs per node | GPU memory | Use it when |
| :-- | :-- | :-- | :-- |
| `aoraki_gpu` | mixed | 40–80 GB | You just need *a* GPU. Draws on the A100, H100 and L40 nodes, so it usually starts soonest |
| `aoraki_gpu_H100` | 4 × H100 | 80–96 GB | Large models, or you need the fastest available card |
| `aoraki_gpu_A100_80GB` | 2 × A100 | 80 GB | The model does not fit in 40 GB |
| `aoraki_gpu_A100_40GB` | 2 × A100 | 40 GB | Standard training and inference work |
| `aoraki_gpu_L40` | 3 × L40 | 48 GB | Good all-rounder; also supports [sharing a card](#can-i-use-part-of-a-gpu) |
| `aoraki_gpu_L4_24GB` | 7 × L4 | 24 GB | Inference and smaller models; often idle |
| `aoraki_gpu_RTX3090` | 1 × RTX 3090 | 24 GB | Small jobs on the standalone workstations |
| `aoraki_gpu_H200` | 8 × H200 | 144 GB | The largest models. [Access must be requested](#why-was-my-job-rejected-from-a-gpu-partition) |
| `aoraki_gpu_RTX6000` | 8 × RTX 6000 | 98 GB | Large models. [Access must be requested](#why-was-my-job-rejected-from-a-gpu-partition) |

Node lists, per-job limits and full hardware details are in the
[Cluster Overview](../overview.md#partitions).

!!! tip "Pick the smallest card that fits"
    An H100 that you use at 20% starts later and costs the cluster more than an L4 that you
    use fully. If your model fits in 24 GB, `aoraki_gpu_L4_24GB` will usually get you working
    sooner.

## How Do I Ask for a GPU?

You need both a GPU partition **and** a request for the GPU itself. Asking for a GPU
partition alone gets you a node with a GPU that your job is not allowed to touch.

!!! terminal

    ```bash
    #SBATCH --partition=aoraki_gpu
    #SBATCH --gpus-per-node=1
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=32G
    #SBATCH --time=04:00:00
    ```

Request at least two CPUs per GPU so the card is not left waiting for data. Full worked
examples are in [Using a GPU with Slurm](../../getting_started/running/batch/slurm_examples/gpu-slurm.md),
and the interactive equivalent is in
[Interactive Sessions](../../getting_started/running/interactive/interactive_shell.md#gpu-sessions).

## Why Is My GPU Job Queued When the Nodes Look Idle?

`sinfo` reporting a node as allocated tells you nothing about how many of its GPUs are
taken, and "idle CPUs" on a GPU node is normal — the `aoraki_small` and `aoraki_short`
partitions deliberately use them.

The three usual explanations:

- **You are already running two GPU jobs in that partition.** There is a cap of **2 running
  GPU jobs per GPU partition** per user. Further jobs wait with
  `(QOSMaxJobsPerUserLimit)`. An interactive session or an OnDemand app holding a GPU counts
  against this, so end sessions you are not using.
- **The GPUs are busy even though the CPUs are not.** Check what is actually allocated:

    !!! terminal

        ```bash
        sinfo -p aoraki_gpu -o "%10N %10T %20G %30C"
        ```

    The `GRES` column shows what each node has; `squeue -p aoraki_gpu` shows who is using it.

- **You asked for more than one node.** GPU jobs are limited to a single node. Requesting
  `--nodes=2` with GPUs will never start.

[Why Is My Job Not Starting?](job_start_time.md#what-does-the-reason-in-brackets-mean)
explains the other pending reasons.

## Why Was My Job Rejected from a GPU Partition?

`aoraki_gpu_H200` and `aoraki_gpu_RTX6000` are newer hardware with **restricted access**.
Submitting to them without it fails immediately with an invalid account or partition error,
or the job sits pending and never runs.

Access is granted per user, on request. Email {{ support_email }} describing the work and
why it needs that hardware.

`aoraki_nzbri` is restricted to a specific research group and is not available generally.

## Is My Code Actually Using the GPU?

A surprising number of GPU jobs run entirely on the CPU — a framework installed without CUDA
support, or a device that was never selected. `seff` will not tell you: it reports CPU and
memory efficiency and says nothing about the GPU.

**Check inside the job.** Adding this to your script confirms the GPU was visible and shows
what it did:

!!! terminal

    ```bash
    nvidia-smi                     # at the start: is the GPU there?
    python my_training_script.py
    nvidia-smi --query-accounted-apps=gpu_util,mem --format=csv   # at the end
    ```

**Check while it runs**, from a login shell, using the job's ID:

!!! terminal

    ```bash
    srun --jobid=<jobid> --overlap nvidia-smi
    ```

If `nvidia-smi` shows the card at 0% while your job is busy, the problem is in your software
rather than in Slurm. In PyTorch, `torch.cuda.is_available()` returning `False` usually means
a CPU-only build was installed — see [PyTorch](../../getting_started/software/applications/pytorch.md).

## Can I Use Part of a GPU?

Yes, on some partitions. Slurm **shards** divide a card into slices that separate jobs can be
scheduled onto, which suits inference, development and anything that cannot keep a whole GPU
busy.

Table: Where GPU sharing is available, and how finely

| Partition | Card | Shards per card |
| :-- | :-- | :-- |
| `aoraki_gpu_L40` | L40 | 20 |
| `aoraki_gpu_L4_24GB` | L4 | 10 |
| `aoraki_gpu_RTX3090` | RTX 3090 | 10 |

Request shards instead of whole GPUs:

!!! terminal

    ```bash
    #SBATCH --partition=aoraki_gpu_L40
    #SBATCH --gres=shard:4
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00
    ```

Do not combine `--gres=shard:` with `--gpus-per-node=` in the same job — ask for one or the
other.

!!! warning "Shards divide access, not memory"
    A shard is a share of the card's scheduling, **not** a reserved slice of its memory. Jobs
    sharing a GPU draw from the same pool of GPU memory, so a neighbour that allocates the
    whole card can make your job fail with an out-of-memory error even though your request
    was satisfied. Size shard jobs to a modest fraction of the card's memory, and use whole
    GPUs for anything where a failure part-way through would be expensive.

If you are unsure whether sharing suits your workload, email {{ support_email }} — it is
worth a short conversation before you build a pipeline around it.

## Do I Need to Load CUDA?

If you are compiling CUDA code, or using software that expects `nvcc` and the CUDA
libraries, yes:

!!! terminal

    ```bash
    module load cuda
    ```

Frameworks installed through Conda or pip — PyTorch, TensorFlow, JAX — usually bundle their
own CUDA runtime and do not need the module. Loading it anyway can occasionally cause a
version clash, so if a framework worked and then stopped after you added `module load cuda`,
try removing it.

See [Using Modules](../../getting_started/software/software_environments/modules.md) for
finding the versions available.

!!! related-pages "What's next?"
    - For worked GPU job scripts, see [Using a GPU with Slurm](../../getting_started/running/batch/slurm_examples/gpu-slurm.md)
    - For an interactive GPU session, see [Interactive Sessions](../../getting_started/running/interactive/interactive_shell.md#gpu-sessions)
    - For the hardware in each node, see the [Cluster Overview](../overview.md#node-hardware)
    - For GPU use over the last week, see [Current Utilisation](../../getting_started/current_utilisation.md)
    - If the job failed rather than waited, see [Why Did My Job Fail?](slurm_job_failures.md)
