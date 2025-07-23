# scp or rsync

The `scp` or `rsync` commands can be used to transfer data on or off the Research Cluster using a local terminal. For transferring data through a web interface the OnDemand File Manager can be used.

This method is recommended for small numbers/sizes of files. For transferring large amounts of data [Globus](globus.md) is the recommended solution.


## scp

`scp` is a commandline program that uses transfers data via `ssh`. It is most useful for copying small files or directories between computers where you are not concerned about resuming transfers in the event of disconnection.

### Transferring onto the cluster

!!! terminal

    ```bash
    scp /local/path/to/file <otago-username>@aoraki-login.otago.ac.nz:/destination/path/on/aoraki
    ```

#### Copying data from the cluster

!!! terminal

    ```bash
    scp  <otago-username>@aoraki-login.otago.ac.nz:/path/on/aoraki/to/file /destination/local/path
    ```


## rsync

Rsync has additional functionalies from `scp`' such as the ability to resume transfers if the connection is interrupted.

### Transferring to the cluster

!!! terminal

    ```bash
    rsync /local/path/to/file <otago-username>@aoraki-login.otago.ac.nz:/destination/path/on/aoraki
    ```

### Copying from the cluster

!!! terminal

    ```bash
    rsync  <otago-username>@aoraki-login.otago.ac.nz:/path/on/aoraki/to/file /destination/local/path
    ```