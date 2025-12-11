---
title: Software Applications # Title displayed at the top of the page
template: software_applications.html #custom template
hide:
    - toc # hides the table of contents on the page
---

<!--This page used custom template software_applications.html see software_applications.md-->

'Modules' are a convenient way to provide access to the wide range of applications we have already installed on the cluster.

| Command                               | Description                                          | Example                                |
| ------------------------------------- | ---------------------------------------------------- | -------------------------------------- |
| `module load <module name>`           | Loads <module name>, (default version)               | `module load Python`                   |
| `module load <module name>/<version>` | Loads <module name>, <version>                       | `module load Python/3.11.6-foss-2023a` |
| `module purge`                        | Removes all loaded modules                           |                                        |
| `module list`                         | Lists currently loaded modules.                      |                                        |
| `module spider`                       | Lists all _available_ modules.                       |                                        |
| `module spider <module name>`         | Searches (fuzzy) available modules for <module name> | `module spider python`                 |

For a full list of module commands run `man module` or visit the [lmod documentation](https://lmod.readthedocs.io/en/latest/010_user.html).


