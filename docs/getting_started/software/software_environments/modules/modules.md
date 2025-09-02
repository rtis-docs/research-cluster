# Modules (LMOD)

!!! overview "On this Page"
      - What is Modules (LMOD)
      - Basic Usage of Modules
 
  <!-- TODO See if overview is in line with content -->

Environment Modules is a tool that lets users easily switch between different versions of applications by managing the shell environment.

Basic usage

* `module avail` will list all available modules 
* `module spider <string>` will seach for all packages containing <string>
* `module load <name>` will load the <name> module. e.g.: `module load apptainer/gubbins`.

  * If you don't specify a version, the highest numeric version number is automatically selected. e.g. `module load r` will load the latest available R version
  * Alternatively you can `module load` an excplicit version, .e.g. `module load r/4.4.3`

* `module list` will show which modules/versions are loaded

!!! related-pages "What's next?"
      - Looking for something else? See [Software Overview page](/docs/getting_started/software/software_overview.md)
      -  For how to run a job on the cluster go to [Running Jobs]() <!-- TODO Fix link -->
      
  <!-- TODO Are these pages the next step or relevant? -->