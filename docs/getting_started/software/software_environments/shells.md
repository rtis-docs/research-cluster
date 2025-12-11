# Shells (bash, zsh, fish, tcsh)


A shell is a command-line interface that interprets user commands and interacts with the operating system, allowing users to execute commands, 
navigate directories, and manage files. Common examples of shells include Bash, Zsh, and Fish. Different shells have different features, built-in commands and different syntax for scripting.

**Bash** (GNU Bourne-Again SHell) is the most common default shell in GNU/Linux distributions, and the default shell on the Cluster.


For non-interactive scripts (especially scripts for Slurm and workflows that may be shared with other people), we recommend sticking with 
the default bash, though some users may prefer to set an alternative shell for their interactive sessions. `cat /etc/shells` will list the different shells that are available cluster-wide.

Due to the way account information is sourced from the central directory, there is no trivial way to change your account's default login shell. 
The easiest workaround is to start your preferred shell from the bash login shell.

## zsh

To automatically launch `zsh` when you start a terminal session, add the following to your `~/.bashrc`:

!!! terminal

    ```bash
    export SHELL=/usr/bin/zsh
    exec /usr/bin/zsh
    ```

## fish

To automatically launch :code:`fish` when you start a terminal session, add the following to your :code:`~/.bashrc`:

!!! terminal

    ```bash
    export SHELL=/usr/bin/fish
    exec /usr/bin/fish
    ```