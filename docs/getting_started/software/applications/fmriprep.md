# fMRIPrep (Containerised)


fMRIPrep is a robust, community-maintained preprocessing pipeline for
functional MRI (fMRI) data. On this cluster, fMRIPrep is provided as a
containerized BIDS-App using Apptainer.

This ensures a consistent, reproducible software environment and avoids
the need for users to install or manage neuroimaging dependencies.

## Software Overview


* Application: fMRIPrep
* Version: 25.1.2
* Container runtime: Apptainer
* Interface: BIDS-Apps compliant command line
* Execution: SLURM batch jobs

## Loading the Module


Load the fMRIPrep module before running any jobs:

!!! terminal

    ```bash
    module load fmriprep/25.1.2
    ```

This makes the `fmriprep` command available on your `$PATH`.

## Basic Usage


The fMRIPrep command follows the standard BIDS-Apps interface:

   `fmriprep <bids_dir> <output_dir> <analysis_level> [options...]`

Required arguments:

* `<bids_dir>` – Path to the BIDS-formatted input dataset (read-only)
* `<output_dir>` – Directory where outputs will be written
* `<analysis_level>` – Processing level (usually `participant`)

Example::

   fmriprep /projects/mygroup/bids \
            /projects/mygroup/derivatives/fmriprep \
            participant

## Running with SLURM


fMRIPrep should be run on compute nodes using SLURM.

Example SLURM job script:

!!! terminal

    ```bash
    #!/bin/bash
    #SBATCH --job-name=fmriprep
    #SBATCH --cpus-per-task=16
    #SBATCH --mem=64G
    #SBATCH --time=12:00:00
    #SBATCH --output=fmriprep_%j.out
    #SBATCH --error=fmriprep_%j.err

    module load fmriprep/25.1.2

    export TEMPLATEFLOW_HOME=/opt/templateflow
    export FS_LICENSE=/opt/freesurfer/license.txt

    fmriprep /projects/mygroup/bids \
            /projects/mygroup/derivatives/fmriprep \
            participant \
            --participant-label sub-01
    ```

### Environment Variables


The following environment variables may be set in your job script:

`TEMPLATEFLOW_HOME`
   Path to a TemplateFlow cache directory. Using a shared cache avoids
   repeated downloads of templates.

`FS_LICENSE`
   Path to a valid FreeSurfer license file. This is required when
   FreeSurfer-based steps are enabled.

### Scratch / Working Directory


During execution, fMRIPrep uses a temporary working directory on the
compute node (preferentially `$SLURM_TMPDIR`). This directory is
created automatically by the wrapper script and does not require
manual configuration.

## Participant Selection


To run specific participants, use the `--participant-label` option:

!!! terminal

    ```bash
    fmriprep /projects/mygroup/bids \
        /projects/mygroup/derivatives/fmriprep \
        participant \
        --participant-label sub-01 sub-02
    ```

## Checking the Installation


To verify that fMRIPrep is available::

   module load fmriprep/25.1.2
   fmriprep --help

This should display the fMRIPrep help text.

## Further Information


* fMRIPrep documentation: [https://fmriprep.org](https://fmriprep.org)
* BIDS specification: [https://bids.neuroimaging.io](https://bids.neuroimaging.io)
* NiPreps project: [https://www.nipreps.org](https://www.nipreps.org)

If you encounter issues or have questions, please contact the
Research Computing support team.
