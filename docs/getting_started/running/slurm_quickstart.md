# Slurm Job Scheduling 

## Slurm Overview

The Otago cluster uses **S**imple **L**inux **U**tility for **R**esource
**M**anagement (SLURM) for job management.
Slurm is an open-source resource manager and job scheduling system for HPC
(**H**igh-**P**erformance **C**omputing) which manages jobs, job steps,
nodes, partitions (groups of nodes), and other entities on the cluster.
Its main purpose is to allocate and manage resources on a cluster, so that jobs
can be run in a way that maximizes utilization of the available resources. In order for SLURM to effectively manage resources, 
jobs are submitted to a queue and based on the requested resources the scheduler 
will run them to make best utilisation of the cluster. 

In contrast to the usual interactive mode of running commands on your computer, 
the main way of interacting with slurm is to 'batch' your jobs up and submit them. 
This 'batching' is usually in the form of a bash script which also includes meta information about 
the resource requirements such as the amount of time it's expected to take, along with the number of CPUs and RAM needed.
At a minimum, a time-limit needs to be specified for your job at submission.

The following is a summary of how to submit jobs and interact with the scheduler. 
Full documentation for slurm is available at [https://slurm.schedmd.com/documentation.html](https://slurm.schedmd.com/documentation.html)


## Slurm Workflow

What follows is a high-level overview of how Slurm works:

  1. Users submit jobs to Slurm using the ``sbatch`` command. A job is a set of
     instructions for running a particular program or set of programs.
  2. Slurm assigns resources to the job based on the requested resources and
     the availability of resources on the cluster. 
     This includes CPU cores, memory, GPUs, and other resources.
  3. Slurm creates a job step for each task in the job. 
     A job step is a subunit of a job that runs on a single node.
  4. Slurm schedules the job steps to run on the assigned resources. 
     It takes into account the job's dependencies, priorities, and other 
     factors to ensure that jobs run in the most efficient way possible.
  5. Once a job step is running, Slurm monitors it and manages it throughout 
     its lifecycle. 
     This includes managing I/O, handling errors, and collecting job
     statistics.
  6. When a job is complete Slurm notifies the user and provides them with the
     output and any error messages that were generated.

Slurm provides a powerful set of tools for managing large-scale compute
resources which allows users to run complex simulations and data analyses more
efficiently and effectively.




### Interacting with the SLURM scheduler




The following are commands that are used to find out information about the status of the scheduler and jobs that have been submitted

  ``sinfo``
     View the status of the cluster's compute nodes.
     The output includes how many nodes and of what types are currently 
     available for running jobs
  ``squeue``
     Check the current jobs in the batch queue system. 
     Use ``squeue --me`` to view your own jobs.
  ``scancel``
     Cancel a job based on its job ID. 
     ``scancel 123`` would cancel the job with ID ``123``. It is only possible to cancel your own jobs.
     ``scancel --me`` will cancel all of your jobs.
  ``sacct``
     Display the job usage metrics after a job has run. This is useful to see resource usage of a job, or determine if it failed.
     ``sacct -j <jobid>``

.. hint::
   ``sinfo`` will quickly tell you the state of the cluster and ``squeue`` 
   will show you all of the jobs running and in the queue. 




### Submitting Jobs


The following are commands that are used for submission of jobs
  ``sbatch``
      Submit a job to the batch queue system. 
      Use ``sbatch myjob.sh`` to submit the Slurm job script ``myjob.sh``.
      You can also provide or override the slurm parameters by supplying them at submission e.g. ``sbatch --job-name=my_job myjob.sh``. 
      The values supplied on the commandline will override the values inside your script.
  ``scancel``
      Cancel a job based on its job ID. 
  ``scancel 123`` would cancel the job with ID ``123``. It is only possible to cancel your own jobs.
  ``scancel --me`` will cancel all of your jobs.



Here we give details on job submission for various kinds of jobs in both batch
(i.e., non-interactive or background) mode and interactive mode.

In addition to the key options of account, partition, and time limit (see
below), your job script files can also contain options to request various
numbers of cores, nodes, and/or computational tasks. 
There are also a variety of additional options you can specify in your batch
files, if desired, such as email notification options when a job has completed.
These are all described further below.


**At a minimum, a time limit must be provided when submitting a job** with ``--time=hh:mm:ss`` (replacing hh,mm, and ss with number values). This can be provided either be as part of your jobscript or as a commandline parameter.


### Defining Jobs


In order to submit a job to the scheduler using ``sbatch`` you first need to define the job through a script. 

A job script specifies where and how you want to run your job on the cluster
and ends with the actual command(s) needed to run your job.
The job script file looks much like a standard shell script (``.sh``) file, but at the top also includes one or more lines that specify options for the SLURM scheduler.
These lines take the form of

.. code-block:: bash

  #SBATCH --some-option-here

Although these lines start with hash signs (``#``), and thus are regarded as
comments by the shell, they are nonetheless read and interpreted by the SLURM
scheduler.

It is through these ``#SBATCH`` lines that the system resources are requested for the allocation that will run your job. 
These parameters can also the supplied as part of calling ``sbatch`` at job submission. parameters supplied in this way will
override the values in your job script.

Common parameters include:

**Meta**
  ``--time=``
    (**required**) Time limit to be applied to the job. Supplied in format hh:mm:ss.
  ``--job-name=`` / ``-J``
    Custom job name
  ``--partition=``
    aoraki (default) or aoraki_gpu
  ``--output=`` / ``-o``
    File to save output from stdout
  ``--error=``/ ``-e``
    File to save output from stderr
  ``--dependency=``/ ``-d``
    Depends on a specified jobid finishing. Can be modifed by completion status. See documentation.
  ``--chdir=`` / ``-D``
    Directory to change into before running the job
 
**Memory**\ - Only need to supply one of these.
  ``--mem=`` 
    (default 8GB) Total memory for the job per node. Specify with units (MB, GB)
  ``--mem-per-cpu=`` 
    amount of memory for each cpu (slurm will total this). Specify with units (MB, GB)
    
  
**Parallelism**
  ``--cpus-per-task=`` / ``-c``
    Number of cores being requested (default = 1)
  ``--ntasks=``
    Number of tasks (default = 1)
  ``--array=``
    defines an array task
  ``--nodes=``/ ``-N``
    (default = 1). Number of nodes to run jobs across.
  

The full list of parameters and their descriptions is available at [https://slurm.schedmd.com/sbatch.html](https://slurm.schedmd.com/sbatch.html)

Here is an example slurm script that would request a single cpu with an allocation of 4 GB of memory, and run for a maximum of 1 minute:

.. code-block:: bash
  
  #!/bin/bash
  #SBATCH --job-name=my_job # define the job name
  #SBATCH --mem=4GB # request an allocation with 4GB of ram
  #SBATCH --time=00:01:00 # job time limit of 1 minute (hh:mm:ss)
  #SBATCH --partition=aoraki # 'aoraki' or 'aoraki_gpu' (for gpu access)
  
  # usual bash commands go below here:
  echo "my example script will now start"
  sleep 10 # pretend to do something
  echo "my example script has finished"



.. hint:: Finding Output

  Output from running a SLURM batch job is, by default, placed in a file named
  ``slurm-%j.out``, where the job's ID is substituted for ``%j``; e.g.
  ``slurm-478012.out``.
  This file will be created in your current directory; i.e. the directory from
  within which you entered the ``sbatch`` command.
  Also by default, both command output and error output (to stdout and stderr,
  respectively) are combined in this file.

  To specify alternate files for command and error output use:

  ``--output``
    destination file for stdout
  ``--error``
    destination file for stderr


## Slurm Scheduler Example


Here is a minimal example of a job script file. 
It will run unattended for up to 30 seconds on one of the compute nodes in the
``aoraki`` partition, and will simply print out the text ``hello world``.


.. code-block:: bash

    #!/bin/bash
    # Job name:
    #SBATCH --job-name=test
    #
    # Partition:
    #SBATCH --partition=aoraki
    #
    # Request one node:
    #SBATCH --nodes=1
    #
    # Specify one task:
    #SBATCH --ntasks-per-node=1
    #
    # Number of processors for single task needed for use case (example):
    #SBATCH --cpus-per-task=4
    #
    # Wall clock limit:
    #SBATCH --time=00:00:30
    #
    echo "hello world"  

If the text of this file is stored in ``hello_world.sh`` you could run and
retrieve the result at the Linux prompt as follows

.. code-block:: 

  $ sbatch hello_world.sh
  Submitted batch job 716
  $ cat slurm-716.out
  hello world

.. note::

  By default the output will be stored in a file called ``slurm-<number>.out``
  where ``<number>`` is the job ID assigned by Slurm




Memory Available
^^^^^^^^^^^^^^^^
Also note that in all partitions except for GPU and HTC partitions, by default
the full memory on the node(s) will be available to your job. 

You should specify the amount using either the total memory required with ``--mem`` (which is the same as ``--mem-per-node``), or the amount of ram required per task with ``--mem-per-task``.

On the GPU and HTC partitions you get an amount of memory proportional to the
number of cores your job requests relative to the number of cores on the node.
For example, if the node has 64 GB and 8 cores, and you request 2 cores, you'll
have access to 16 GB memory.






Parallelization
'''''''''''''''
When submitting parallel code, you usually need to specify the number of tasks,
nodes, and CPUs to be used by your job in various ways.
For any given use case, there are generally multiple ways to set the options to
achieve the same effect; these examples try to illustrate what we consider to
be best practices.

The key options for parallelization are:

    ``--nodes`` (or ``-N``)
      indicates the number of nodes to use
    ``--ntasks-per-node``
      indicates the number of tasks (i.e., processes one wants to run on each
      node)
    ``--cpus-per-task`` (or ``-c``)
      indicates the number of cpus to be used for each task

In addition, in some cases it can make sense to use the ``--ntasks`` (or
``-n``) option to indicate the total number of tasks and let the scheduler
determine how many nodes and tasks per node are needed.
In general ``--cpus-per-task`` will be ``1`` except when running threaded code.  

Note that if the various options are not set SLURM will in some cases infer
what the value of the option needs to be given other options that are set and
in other cases will treat the value as being ``1``. 
So some of the options set in the example below are not strictly necessary, but
we give them explicitly to be clear.

Here's an example script that requests an entire Otago node and specifies 20
cores per task.

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=test
    #SBATCH --account=account_name
    #SBATCH --partition=aoraki
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=20
    #SBATCH --time=00:00:30
    ## Command(s) to run:
    echo "hello world" 
    
Only the partition, time, and account flags are required.

## GPU Jobs


Please see example job script for such jobs.




## Job Accounting / Efficency


To view your job information you can use the ``sacct`` command. 

   To view detailed job information:

!!! terminal
    
    ```bash
    sacct --format="JobID,JobName,Elapsed,AveCPU,MinCPU,TotalCPU,Alloc,NTask,MaxRSS,State" -j <job_id_number>
    ```

    ```output
    sacct --format="JobID,JobName,Elapsed,AveCPU,MinCPU,TotalCPU,Alloc,NTask,MaxRSS,State" -j 321746
    JobID           JobName    Elapsed     AveCPU     MinCPU   TotalCPU  AllocCPUS   NTasks     MaxRSS      State
    ------------ ---------- ---------- ---------- ---------- ---------- ---------- -------- ---------- ----------
    321746       ondemand/+   23:11:07                        00:05.337          4                     CANCELLED+
    321746.batch      batch   23:11:08   00:00:00   00:02:56  00:05.337          4        1    683648K  CANCELLED
    ```



