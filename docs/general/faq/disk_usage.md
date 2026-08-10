# Storage and Quotas

!!! overview "On this Page"
    - Checking how much space you are using, and against what limit
    - What usually fills a home directory on this cluster, and how to clear it
    - Where research data belongs instead
    - Where temporary files go while a job runs

A full home directory does not just stop you saving files — it can stop jobs writing their
output, break Conda and pip, and prevent you logging in at all. It is worth checking before
it becomes a problem.

## How Much Space Am I Using, and What Is My Limit?

`df` shows your home directory's total size and how much of it is used:

!!! terminal

    ```bash
    df -h ~
    ```

The hard quota on home directories is **{{ home_quota }}**. You will be emailed at your
Otago address once you reach **30 GB**, which is the point to do something about it — at the
hard quota you cannot write at all.

For the breakdown, `du` shows what is using the space, largest first:

!!! terminal

    ```bash
    du -h -d 1 ~ | sort -rh | head -20
    ```

Add `-d 2` or `-d 3` to go deeper once you know which directory to look inside.

## My Home Directory Is Full. What Is Taking Up the Space?

Almost always one of these, and rarely your actual research data:

Table: The usual culprits in a full home directory

| Location | What it is | What to do |
| :-- | :-- | :-- |
| `~/.conda`, `~/miniforge3` | Conda environments and packages | Move environments to `/projects`, and run `conda clean --all`. See [Conda](../../getting_started/software/software_environments/conda.md) |
| `~/.cache/pip` | Cached Python wheels | `pip cache purge` |
| `~/.apptainer`, `~/.singularity` | Cached container layers | Delete the cache directory, or set `APPTAINER_CACHEDIR` elsewhere |
| `~/R/`, `~/.local/lib` | R and Python packages installed into your home directory | Keep, but be aware they grow. Consider a project library |
| `~/spack` | Spack builds | See [Spack](../../getting_started/software/software_environments/spack.md) for building into `/projects` instead |
| `slurm-*.out` | Accumulated job output, one file per job | Delete the old ones, or send output elsewhere with [`--output`](../../getting_started/running/batch/sbatch_options.md#output-and-errors) |
| `~/ondemand` | OnDemand session logs | Safe to delete when no session is running |

Once you have found the large items:

!!! terminal

    ```bash
    rm -rf ~/.cache/pip                  # delete what you do not need
    tar -czf old_results.tar.gz results/ && rm -rf results/   # or compress it
    ```

!!! warning "There is no undo"
    `rm -rf` is immediate and permanent. Home directories are snapshotted daily, so a
    mistake there can often be recovered by emailing {{ support_email }} — but nothing in
    `/projects` or `/weka` is backed up at all.

## Where Should My Research Data Go Instead?

Not in your home directory. Home is for scripts, configuration and small files; research
datasets belong in a `/projects` allocation, and high-throughput scratch work in `/weka`.

The [Storage Guidelines](../guidelines/storage_guidelines.md) cover what each area is for,
who it is allocated to, and how long data should stay there.

## Where Do Temporary Files Go During a Job?

Every job gets its **own private** `/tmp`, `/var/tmp` and `/dev/shm` on the node it runs on.
They are not shared with other jobs, and they are **deleted when the job ends**.

That makes `/tmp` the right place for scratch files your job creates and does not need
afterwards — it is fast, and it does not count against your home quota. But anything you
want to keep has to be copied out before the job finishes:

!!! terminal

    ```bash
    # at the end of your job script
    cp /tmp/final_output.bam /projects/.../results/
    ```

A job that writes results to `/tmp` and then exits leaves nothing behind.

## Is My Data Backed Up?

Only your home directory. It is snapshotted daily for a week, weekly for a month, and
monthly for six months.

`/projects` and `/weka` are **not backed up**. If you delete something there it is gone.
See [Backups Are Your Responsibility](../guidelines/storage_guidelines.md#backups-are-your-responsibility)
for the recommended pattern of keeping the authoritative copy on HCS.

## How Do I Get More Space?

Home directory quotas are fixed — the limit exists so that home directories can be backed
up. If you need more space, the answer is a different storage area, not a bigger home.

- To request a `/projects` or `/weka` allocation, see [Storage Request](../../storage/storage_request.md).
- To increase an existing allocation, a project manager can request a quota change through
  [Coldfront](../../getting_started/access/coldfront/manager.md).
- If you are not sure what you need, email {{ support_email }} and we will work it out with you.

!!! related-pages "What's next?"
    - For what each storage area is for, see [Storage Guidelines](../guidelines/storage_guidelines.md)
    - For the full detail on each area, see the [Storage Overview](../../storage/storage_options.md)
    - To move data on and off the cluster, see [Sharing and Moving Data](sharing_data.md)
    - For Conda environments in particular, see [Conda](../../getting_started/software/software_environments/conda.md)
