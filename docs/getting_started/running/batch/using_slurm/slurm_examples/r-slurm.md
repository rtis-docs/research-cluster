# Using R with Slurm

These examples can be found at [https://appsgit.otago.ac.nz/projects/RTIS-SP/repos/slurm-code-examples/browse](https://appsgit.otago.ac.nz/projects/RTIS-SP/repos/slurm-code-examples/browse) (need to be on the campus network to access)

Or downloaded and browsed on the cluster by:

!!! terminal 

    ```bash
    git clone https://appsgit.otago.ac.nz/scm/rtis-sp/slurm-code-examples.git
    ```



If you have downloaded the repository, the following code examples are in the ``r_examples`` subdirectory: 

!!! terminal
    
    ```bash
    cd slurm-code-examples/r_examples/
    ```

## SLURM job calling an R script

This pair of scripts represents how an Rscript can be run using the SLURM scheduler.

Create the R script ``hello_rscript.R`` with the following contents:

!!! r-code "Script: `hello_script.R`"

    ```r
    print("hello")
    ```


Create the slurm script ``run_hello_rscript.sh`` with the following contents:

!!! terminal "Script: `run_hello_rscript.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --ntasks=1

    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript hello_rscript.R
    ```



The job can now be submitted to the scheduler with:

!!! terminal

    ```bash
    [user@aoraki-login r_examples]$ sbatch run_hello_rscript.sh
    ```


## Example of using multiple cores within a single Rscript

The following are two examples creating a job that uses multiple cores on a single node *with R managing the the parallelism*. In R, either the ``parallel``  package or the ``future`` package are (mainly) used to do this. The ``parallelly`` package provides some bonus functionality to both.

The key difference to the previous example is that we need to define how to parallelise the code. This is done through ``parallel`` or ``future`` and we need to define the number of cores/cpus to use for the parallelism within the SLURM script through ``--cpus-per-task`` which gets stored in a BASH environment variable ``$SLURM_CPUS_PER_TASK``.  
There are multiple approaches to how this can be done but for this example two have been demonstrated

The overall task demonstrated is to calculate the means for sub-groups of a dataset in parallel. 


The first approach uses the packages ``parallel`` and ``doParallel`` to create and manage the parallelism within R.
It will create and register a 'cluster' of 'workers' within R and then pass each sub-task to a worker.


!!! r-code "Script: `r_multicore_example-parallel.R`"

    ```r
    library(parallelly)
    library(parallel)
    library(doParallel)

    # automatically detect number of available cores
    ncpu <- parallelly::availableCores()


    doParallel::registerDoParallel(cores = ncpu)

    # calculate the mean sepal length for each iris species in parallel
    mean_petal_lengths <- foreach(species = unique(iris$Species), .combine = 'c') %dopar% {
        m <- mean(iris[iris$Species == species, "Sepal.Length"])
        names(m) <- species
        return(m)
    }

    print(mean_petal_lengths)
    ```




!!! terminal "Script: `run_multicore_r_example-parallel.sh:`"
    
    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=4
    #SBATCH --ntasks=1

    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript r_multicore_example-parallel.R
    ```

Submitting the job:


!!! terminal

    ```bash
    [user@aoraki-login r_examples]$ sbatch run_multicore_r_example-parallel.sh
    ```


The following is same example as above but insetad implemented using the ``furrr`` package to parallelise ``purrr`` using ``future``.


!!! r-code "Script: `r_multicore_example-furrr.R`"

    ```r
    library(parallelly)
    library(furrr)


    ncpus <- parallelly::availableCores()
    plan("multisession", workers = ncpus)

    mean_species <- function(x){
        mean(iris[iris$Species == x, "Sepal.Length"])
    }

    species <- unique(iris$Species)
    mean_petal_lengths <- furrr::future_map_dbl(species, mean_species)
    names(mean_petal_lengths)  <- species           

    print(mean_petal_lengths)
    ```



!!! terminal "Script: `run_multicore_r_example-furrr.sh`"
    
    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=4
    #SBATCH --ntasks=1

    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript r_multicore_example-furrr.R 
    ```

Submitting the job:


!!! terminal

    ```bash
    [user@aoraki-login r_examples]$ sbatch run_multicore_r_example-furrr.sh
    ```

## SLURM array job with R

An array job allows you to define the resources for a single job but run many instances of it. 
Instead of submitting many individual jobs, it is best to use an array job as it is more effcient for the scheduler. 
A common use case would be to define a job for a sample, and then run the job on all samples in parallel.
SLURM facilitates this through the array job type. For an array job there are two bash environment variables that you can 
make use of: ``SLURM_JOBID`` which is the overall job, and ``SLURM_ARRAY_TASK_ID`` which is the id assigned to 
that specific "subjob". A common use for the task id would be to use it as an index on a sample sheet.

A second benefit of using an array over individually submitting many of the same job is that if you want to rerun a job, you can specify specific array indexes, instead of many differnt job ids.

To make use of these variables inside your R task, you can either pass them through as a commandline argument or you can access them from within R with `option()`

The scenario for the example will be again calculating the mean for each species in the ``iris`` data set but this time instead of using a single job with multiple cores, we'll use a single job per species utilising the SLURM array.

Here is an example of running 3 jobs in parallel using a slurm array passing the array index as a commandline argument to R


!!! r-code "Script: `r_array_job_args.R`"

    ```r
    args <- commandArgs(trailingOnly = TRUE)
    # args come in as strings so need to convert to numeric type
    id <- as.numeric(args[1]) 
    message(paste("SLURM_ARRAY_TASK_ID was: ", id))

    # determine which of the species is the target for the job
    job_species <- unique(iris$Species)[id]
    species_mean_sepal_length <- mean(iris[iris$Species == job_species, "Sepal.Length"])
    results <- data.frame(species = job_species, mean_sepal_length = species_mean_sepal_length)
    write.csv(results, paste0(job_species,".csv"), row.names = FALSE)
    ```



!!! terminal "Script: `run_array_job_example-args.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --ntasks=1
    #SBATCH --array=1-3 # run three of this job with the indexes 1,2,3

    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript r_array_job_example-args.R ${SLURM_ARRAY_TASK_ID}
    ```

Submitting the job:


!!! terminal
    
    ```bash
    [user@aoraki-login r_examples]$ sbatch run_array_job_example-args.sh
    ```

And here is an example of the same job but instead accessing the system environment variable from within R:



!!! r-code "Script: `r_array_job_example-env.R`"

    ```r
    # read the environment varible SLURM_ARRAY_TASK_ID and convert to numeric data type
    id <- as.numeric(Sys.getenv(x = "SLURM_ARRAY_TASK_ID"))
    message(paste("SLURM_ARRAY_TASK_ID was: ", id))

    # determine which of the species is the target for the job
    job_species <- unique(iris$Species)[id]
    species_mean_sepal_length <- mean(iris[iris$Species == job_species, "Sepal.Length"])
    results <- data.frame(species = job_species, mean_sepal_length = species_mean_sepal_length)
    write.csv(results, paste0(job_species,".csv"), row.names =  FALSE)
    ```




!!! terminal "Script: `run_array_job_example-env.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --ntasks=1
    #SBATCH --array=1-3 # run three of this job with the indexes 1,2,3

    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript r_array_job_example-env.R 
    ```


Submitting the job:


!!! terminal

    ```bash
    [user@aoraki-login r_examples]$ sbatch run_array_job_example-env.sh
    ```


One disadvantage of this approach is it can be harder to create and debug the R code as it relies on environmental variables being set prior to execution, 
rather than passing the values at runtime on the commandline through arguments.

## SLURM job dependencies with R

SLURM job dependencies allow you to link jobs together and subsequent jobs will only run depending on 
the running status of pre-requisite jobs. This allows you to create workflows with different job requirements for the different stages.

When submitting the ``-d`` (or ``--dependency=``) option is supplied to ``sbatch`` with the job id to make the job dependent on e.g. ``sbatch -d 1234``. 
The main advantage of using dependencies is that SLURM will cordinate the running (or cancelling if failed) of downstream dependent jobs. 
There are extra options for the dependencies such as ``-d afterok:<jobid>``, ``-d afterany:<job_id>``. See https://slurm.schedmd.com/sbatch.html for more infomation regarding the ``-d`` option.

In the previous example we outputted the mean for each group but it would be good to have a single output that summarised the results. We could 
create a second job that was dependant on the previous job compeleting before it ran to take the results and combine them together. This type of 
work flow is often referred to as a scatter-gather as there is a scattering phase to calculate results per group and a gathering phase to combine them back together.



!!! r-code "Script: `r_combine_results.R`"

    ```r
    results_list <-list()
    for(species in unique(iris$Species)){
        results_list[[species]] <- read.csv(paste0(species,".csv"), header=TRUE)
    }
    combined_results <- do.call(rbind, results_list)
    write.csv(combined_results, "combined_results.csv", row.names=FALSE)
    ```



!!! terminal "Script: `run_combine_example.sh`"

    ```bash
    #!/bin/bash
    #SBATCH --mem=512MB
    #SBATCH --time=00:01:00
    #SBATCH --cpus-per-task=1
    #SBATCH --ntasks=1


    # load R v4.4.3 through the modules
    module load r/4.4.3

    # run the rscript
    Rscript r_combine_results.R
    ```

Now in order to run this as a dependency we supply ``-d <jobid>`` to sbatch with the jobid of the job upon which we are depending to run first when submitting.

e.g.

!!! terminal

    ```bash
    [user@aoraki-login r_examples]$ sbatch run_array_job_example-args.sh 
    Submitted batch job 323173
    [user@aoraki-login r_examples]$ sbatch -d 323173 run_combine_example.sh 
    Submitted batch job 323174
    ```


This requires you to pay attention the job number however, so instead we can wrap the submission in a bash script to automatically grab the jobid:



!!! terminal "Script: `run_scatter_gather.sh`"

    ```bash
    # store the output from sbatch into a variable
    FIRST_JOB=$(sbatch run_array_job_example-args.sh)
    
    # extract out the job id from the variable
    # use space as a delimiter and take the 4th field
    FIRST_JOB_ID=$(echo "${FIRST_JOB}" | cut -d" " -f 4)
    
    # submit the second job setting the dependency on the first
    sbatch -d ${FIRST_JOB_ID} run_combine_example.sh
    ```



run the script to do the submission:

!!! terminal

    ```bash
    bash run_scatter_gather.sh
    ```
