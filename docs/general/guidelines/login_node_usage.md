# Login Node Usage

The main purpose of the login node is to provide a mechanism for interacting with the scheduler to submit jobs.

The login node is a *shared resource* and is not intended to have computational jobs run on it. There is a limit of 8 CPUS and 60GB of memory per user, exceeding this will trigger warning emails and the possiblity of your tasks being cancelled in order to maintain the stability and accessibilty of the node for everyone. Tasks involving data copying/moving would ideally be kept to less than 30 minutes.

Examples of tasks that the login node is suitable for:

- Small file transfers through `scp` or `rsync`
- editing code/scripts
- moving or copying data on the file system (durations < 30min)
- compressing/tarring data small amounts of data (durations < 30min)

For the more intensive tasks we ask that you make use of either the [OnDemand HPC Desktop](/getting_started/software/onDemand/hpc_desktop) or create an interactive allocation through the scheduler so that resources can be allocated and dedicated to you.