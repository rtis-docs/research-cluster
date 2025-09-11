# May 2024



**CHANGES AND FIXES IMPLEMENTED:**

Breaking changes:

- Memory usage is now limited to the amount specified in your Slurm job script.
- Partitions now have time limits. All jobs must now include a specified time variable.

Other changes/fixes:

- Storage has been updated to allow permissions to be applied more effectively.
- A more robust login node has been introduced, featuring the same CPU architecture as the cluster nodes, which is ideal for compiling software.
    - If prompted during SSH login regarding host key change use ``ssh-keygen -f "~/.ssh/known_hosts" -R "aoraki-login.otago.ac.nz"`` to remove the old key and reattempt to SSH.
- New compute and GPU nodes have been added, including 5 high-memory (2TB) nodes, 4 high-CPU nodes, 4 A100 GPU nodes, and 1 H100 GPU node, in addition to our existing compute nodes.
- New Slurm partitions have been created.

!!! related-pages "What's next?"
    - [Login node SSH](../../getting_started/access/login_ssh.md)
    - [Slurm Overview](../../getting_started/running/slurm_quickstart.md)
    - [Research HPC Cluster (Aoraki)](../../general/overview.md)

  <!-- TODO Are these pages the next step or relevant? -->
  <!-- I'm unsure if there are other pages that are relevant to the content-->