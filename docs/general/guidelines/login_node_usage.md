# Login Node Usage

The main purpose of the login node is to provide a mechanism for interacting with the scheduler to submit jobs.

The login node is a *shared resource* and is not intended to have computational jobs run on it. There is a limit of 8 CPUS and 60GB of memory per user, exceeding this will trigger warning emails and the possibility of your tasks being cancelled in order to maintain the stability and accessibility of the node for everyone. Tasks involving data copying/moving would ideally be kept to less than 30 minutes.

Examples of tasks that the login node is suitable for:

- Small file transfers through `scp` or `rsync`
- editing code/scripts
- moving or copying data on the file system (durations < 30min)
- compressing/tarring data small amounts of data (durations < 30min)

For the more intensive tasks we ask that you make use of either the [OnDemand HPC Desktop](../../getting_started/software/OnDemand/hpc_desktop.md) or [create an interactive allocation through the scheduler](../../getting_started/running/interactive/interactive_shell.md) so that resources can be allocated and dedicated to you.

!!! related-pages "What's next?"
      - [OnDemand HPC Desktop](../../getting_started/software/OnDemand/hpc_desktop.md)
      - [Interactive Sessions from the Command Line](../../getting_started/running/interactive/interactive_shell.md)
      - [Slurm Quickstart](../../getting_started/running/batch/slurm_quickstart.md)
