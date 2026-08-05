# CryoSPARC

!!! overview "On this Page"
    - How to get a CryoSPARC account
    - How to reach the web interface
    - The compute lanes your jobs can run on, and how to choose between them

[CryoSPARC](https://cryosparc.com/) is a platform for cryo-EM single particle analysis. We host a shared instance for Otago researchers, backed by both dedicated CryoSPARC hardware and the Research Cluster's GPU nodes.

## Getting Access

CryoSPARC runs on the Research Cluster, so you need cluster access first.

1. [Sign up for the Research Cluster](../../getting_started/access/signup.md) if you do not already have an account.
2. Once that is done, email the eResearch Support team at **{{ support_email }}** so we can create your CryoSPARC account and send you a login token.

Tell us at this point if you will be sharing files with a research group, or if your work needs to stay private, so we can set up an appropriate project folder for you.

## Accessing CryoSPARC

Most work is done through the web interface:

[https://cryosparc.otago.ac.nz](https://cryosparc.otago.ac.nz){ .md-button }

From the dashboard you can queue and monitor jobs, and see which lanes are currently in use.

## Compute Lanes

CryoSPARC jobs do not all run on the same hardware. When you queue a job you pick a **lane**, and that decides where it runs.

| Lane | Runs on | Shared with | Queuing |
| :-- | :-- | :-- | :-- |
| **Default** | `gpu-07` and `gpu-08`, dedicated to CryoSPARC | Other CryoSPARC users only | Usually starts promptly |
| **Aoraki (cluster)** | The Research Cluster's GPU nodes | All cluster users and applications | May wait for free GPUs |

### Default

The default lane uses `gpu-07` and `gpu-08`, two nodes reserved for CryoSPARC. Jobs are load-balanced between them, and choosing a particular node gives you no extra performance or priority.

Because these nodes are not shared with general cluster work, your job is only ever competing with other CryoSPARC users. This makes the default lane the better choice for routine processing, where predictable start times matter more than raw GPU speed.

If you manage files or jobs over SSH, connect to `gpu-08` — it is the master node.

### Aoraki (cluster)

The Aoraki lane submits your job to the Research Cluster's GPU nodes as a [Slurm](../../getting_started/running/batch/slurm_quickstart.md) job. These GPUs are more powerful and can noticeably speed up job finalisation.

The trade-off is that they are shared with every other cluster user and application, so your job may sit in the queue before it starts. Use this lane for heavy steps where the faster hardware is worth the wait.

To see how busy the GPU nodes are before you queue a job, check [Current Utilisation](../../getting_started/current_utilisation.md). See the [Cluster Overview](../../general/overview.md) for the GPU partitions and the limits that apply to them.

!!! related-pages "What's next?"
    - To get an account, see [Signing Up](../../getting_started/access/signup.md)
    - For the cluster's GPU hardware and partitions, see the [Cluster Overview](../../general/overview.md)
    - To see how busy the cluster is, see [Current Utilisation](../../getting_started/current_utilisation.md)
    - For moving data on and off the cluster, see [Data Transfer](../../storage/data_transfer/data_transfer_overview.md)
    - For writing and submitting your own GPU jobs, see [Running Jobs](../../getting_started/running/running_jobs_overview.md)
