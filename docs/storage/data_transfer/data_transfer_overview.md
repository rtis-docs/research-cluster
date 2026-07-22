# Data Transfer Overview

To use the research cluster, you'll need to transfer data from your local machine to storage accessible by the cluster. There are two main storage locations:

- **Otago High Capacity Storage (HCS)** - for long-term, backed-up data storage
- **Cluster research storage (Ohau and WEKA)** - for temporary working data during jobs

Choose your transfer method based on how much data you need to move and your file size. For details on storage options, see [Storage overview](../../storage/storage_options.md).


## Small Files (Upload via Web Interface)

For uploading a single file or a few small files, use the file browser in Open OnDemand.

The file browser within Open OnDemand can be used to upload files directly into either your home or a project directory. It can't be used for accessing data on the Otago HCS.

!!! related-pages "What's next?"
    -  [Open OnDemand file browser](../../getting_started/software/onDemand/ondemand.md#using-open-ondemand)
    -  [Storage locations](../../storage/storage_options.md)


## Large or Multiple Files

For transferring many files or large files, use command-line tools via SSH connection:

- [`scp` or `rsync`](rsync.md) - for direct transfers via SSH
- [Globus](globus.md) - for high-volume data transfers and automated workflows
- [rclone](rclone.md) - for simple transfers to and from HCS


!!! related-pages "What's next?"
      - [Using rsync and scp for file transfer](rsync.md)
      - [Using Globus for large data transfers](globus.md)
