# R and Rstudio



## Rstudio

RStudio server is available through [OnDemand as a versioned apptainer image](../onDemand/available_apps.md/#rstudio-server). Each container has a slightly different configuration and availability of system libraries and pre-installed packages.

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

For a list of environmental variables that can be defined in your `.Renviron` file from witin R run: 
!!! r-code
    ```r
    ?"environment variables"
    ```

To set variables for your user, use `~/.Renviron`, to set variables for a RStudio project create `.Renviron` in the Rstudio project directory.

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

The `.Rprofile` file can be used to load specific R settings and can be set for at a user level with `~/.Rpofile` or if using an R-project, at the project level by making a `.Rprofile` file in the project directory.

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

If your projects have need for different package versions it would be worth looking into the `renv` package for managing libraries and packages at the project level - [https://rstudio.github.io/renv/articles/renv.html](https://rstudio.github.io/renv/articles/renv.html)
