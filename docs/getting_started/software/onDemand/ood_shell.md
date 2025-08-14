# Accessing the Shell through Open OnDemand

Open OnDemand provides a convenient way to access a shell on the cluster directly from your web browser, without needing to install or configure an SSH client.

## How to Open a Shell Session

1. Log in to the Open OnDemand portal using your web browser.
2. In the top menu, go to **Clusters > Aoraki Cluster Shell Access** (or the relevant cluster name).
3. A new tab or window will open with a terminal session connected to the cluster.

## What You Can Do

- Run command-line programs and scripts.
- Submit and monitor Slurm jobs using commands like `sbatch`, `squeue`, and `sacct`.
- Navigate and manage your files using standard Linux commands.
- Use text editors such as `nano`, `vim`, or `emacs`.

## Tips

- The shell session runs on a login node, so avoid running heavy computations directly in this terminal. Start an OnDemand HPC Desktop session, or use Slurm to submit compute jobs.
- You can open multiple shell sessions if needed.
- If you are disconnected, simply reconnect through the Open OnDemand portal.

The Open OnDemand shell is a quick and user-friendly way to interact with the cluster for everyday tasks.


<!-- TODO link with the getting started section -->