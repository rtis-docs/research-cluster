# R and RStudio



## RStudio

RStudio server is available through [OnDemand as a versioned apptainer image](../OnDemand/available_apps.md#apps-on-the-current-portal). Each container has a slightly different configuration and availability of system libraries and pre-installed packages.




## R


R is available through the module system on all the cluster nodes. To see which versions of R are available use

!!! terminal
    ```bash
    module spider r
    ```


## Managing Package Libraries with R and RStudio

The following will show you which paths R is using to search for packages that have been installed

!!! r-code

    ```
    .libPaths()
    ```

The order of the paths returned shows the precedence, with the first being the highest.

You can alter the paths being used with either of the following R commands

!!! r-code
    ```
    # use the specified path and fall back to other existing locations
    .libPaths(c("/new/path/to/use/", .libPaths()))

    # only use this path
    .libPaths("/new/path/to/use/")
    ```

This method can be useful for scripts but a better and more sustainable approach is to set your library paths using either the [.Rprofile](#rprofile) or [.Renviron](#renviron) files as described below.

### .Renviron vs .Rprofile

Although both methods can configure a custom package library, they serve different purposes.

.Renviron |	.Rprofile
---|---
Sets environment variables before R starts. |	Executes R code after R starts.
Preferred for defining R_LIBS_USER.	| Useful for calling .libPaths() or running other startup code.
Automatically works with R, Rscript, and batch jobs. | Can perform more complex configuration and conditional logic.
Simple and portable. | More flexible but also easier to misconfigure.

For most users, configuring `R_LIBS_USER` in `.Renviron` is the simplest and most robust solution.

### .Renviron

The `.Renviron` file can be used to supply system environment variables to R. It is often used as a way of making API keys accessible within R e.g. a github API token. Bit it can also be used to set where R looks for libraries.

For a list of environmental variables that can be defined in your `.Renviron` file from within R run: 
!!! r-code
    ```r
    ?"environment variables"
    ```

To set variables for your user, use `~/.Renviron`, to set variables for a RStudio project create `.Renviron` in the RStudio project directory.

#### Create or edit your `.Renviron` file


=== "Command line"

    !!! terminal
        ```bash
        nano ~/.Renviron
        ```

=== "Within RStudio:"

    !!! r-code
        ```
        file.edit("~/.Renviron")
        ```

#### Set the Library Location

Add a line such as: `R_LIBS_USER=/project/myproject/R/library`, or alternatively, for an R-version-specific library: `R_LIBS_USER=/project/myproject/R/%v`, where `%v` is automatically replaced by the major and minor R version (for example, 4.5).

!!! info
    Ensure you don't have any typos in the path.

    It is a good idea to version stamp your library so that if you switch between different versions of R the correct packages will be used.

With R 4.5.0, the resulting library path `R_LIBS_USER=/project/myproject/R/%v` becomes:

`/project/myproject/R/4.5`

This makes it unnecessary to edit `.Renviron` whenever the minor R version changes.

Changes made to your `.Renviron` file won't take effect in an existing R or RStudio session so you will need to exit and reopen.

You can then verify the path supplied in your `.Renviron` file is being used with

!!! r-code

    ```
    .libPaths()
    ```

### Rprofile

The `.Rprofile` file can be used to load specific R settings and can be set for at a user level with `~/.Rprofile` or if using an R-project, at the project level by making a `.Rprofile` file in the project directory.

To set a custom location for installing packages, open your `.Rprofile` e.g. `~/.Rprofile` for user level

!!! r-code
    ```
    file.edit("~/.Rprofile")
    ```


Then add the following into your `.Rprofile`

```
lib_path <- "/path/to/lib" # CHANGE THIS PATH

r_version <- paste(R.version$major,
                   strsplit(R.version$minor, "\\.")[[1]][1],
                   sep = ".")
platform <- R.version$platform
user_lib <- path.expand(sprintf("%s/R/%s-library/%s/",lib_path, platform, r_version))

if (!dir.exists(user_lib)) {
  message(sprintf("Creating user library: %s", user_lib))
  dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
}
.libPaths(c(user_lib, .libPaths()))
```

!!! warning
    Make sure to edit the path in the first line


Then reload your R session and you can confirm your library path will be used with:

!!! r-code

    ```
    .libPaths()
    ```

### Project level libraries with `renv`

The approaches above set library paths for you or for a project by hand. If different projects need different versions of the same package, `renv` manages that for you: each project gets its own library, and the exact versions are recorded in a lockfile you can commit and reinstall from later.

See [renv (R Package Environments)](../software_environments/renv.md) for setting this up on the cluster, including how to get prebuilt packages rather than compiling from source, and how to use a project from a Slurm job.


## Known Issues

### RStudio Server Shows Blank or Gray Screen, or Error “Status code 502”

When using RStudio Server through OnDemand, some users have found that the job starts normally, but upon connecting through OnDemand, a blank or gray screen appears instead of RStudio Server. Occasionally, RStudio Server will load successfully from this screen. Please wait at least a full minute on this screen before proceeding to the solution below.

#### Resolving

If the gray screen persists after one minute, or you receive the error:

`Status code 502 returned by RStudio Server when executing 'client_init'`

it is possible that RStudio Server is stuck trying to load.

As a workaround, try **reloading the tab and waiting another minute**. This can sometimes resolve the issue.

If the issue continues, **clearing RStudio’s temporary files** can help. These are stored at:

`~/.local/share/rstudio`

To do this safely, move the files to a backup location with the following command:

`mv ~/.local/share/rstudio ~/.local/share/rstudio.backup`

Then, try loading RStudio Server again. Note that it may still take a minute or two for the gray screen to clear, as described above.

!!! note
    This will likely reset your RStudio session. You may need to reopen previous projects and files, and any unsaved work may be lost.


#### Preventing

While the exact cause is unclear, possible reasons include:

RStudio Server’s temporary files being corrupted due to an improper shutdown.

RStudio Server attempting to reload large files from a previous session.

To minimize the chance of this happening:

**Properly shut down your RStudio session** before your job times out in OnDemand. Do this by clicking the **power button** in the top-right corner of RStudio Server.

**Prevent RStudio Server from saving your workspace** on exit. To do this:

- Click the “Tools” menu and select “Global Options”.
- In the “General” pane under the “Workspace” section:
    - Uncheck: “Restore .RData into workspace at startup:”
    - Set: “Save workspace to .RData on exit:” to Never
