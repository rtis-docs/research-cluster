# Data Transfer Overview

!!! overview "On this Page"
      - What storage locations are available
      - When to use each storage location
      - Backing up your data
 
  <!-- TODO See if overview is in line with content -->

In order to make the most of the compute platform, chances are you will have data you want to work with but in order to make use of it, you will need to transfer it to a place that the cluster can access.

The two locations that the cluster can access data are:

- Otago High Capacity Storage (HCS)
- The cluster research storage

For more details about the storage please see the [Storage overview](../../storage/storage_options.md)

There are several methods for moving data onto and off of the [research storage](../../storage/storage_options.md).


### Transfer Single/Few Files of Small Size

The file browser within Open OnDemand can be used to upload files directly into either your home or a project directory. It can't be used for accessing data on the Otago HCS.

!!! related-pages "What's next?"
    -  [File browser within Open OnDemand](../software/onDemand/ondemand.md#using-open-ondemand)
    -  For software available on the cluster go to [Software](../software/software_overview.md)
    -  For how to run a job on the cluster go to [Running Jobs]()
      <!-- TODO Fix link -->
  <!-- TODO Are these pages the next step or relevant? -->


### Transfer Multiple or Large Files

When it comes to transferring many files, or files that are large this is best done through either:

- [`scp` or `rsync`](rsync.md) to transfer through an `ssh` connection
- [Using globus](globus.md) for large amounts of data


!!! related-pages "What's next?"
      - For software available on the cluster go to [Software](../software/software_overview.md)
      -  For how to run a job on the cluster go to [Running Jobs]() <!-- TODO Fix link -->
      
  <!-- TODO Are these pages the next step or relevant? -->