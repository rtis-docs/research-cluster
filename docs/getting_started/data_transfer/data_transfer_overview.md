# Data Transfer Overview

In order to make the most of the compute platform, chances are you will have data you want to work with but in order to make use of it, you will need to transfer it to a place that the cluster can access.

The two locations that the cluster can access data are:

- Otago High Capacity Storage (HCS)
- The cluster research storage

For more details about the storage please see the [Storage overview](../../storage/storage_options.md)

There are several methods for moving data onto and off of the [research storage](../../storage/storage_options.md).


### Transfer Single/Few Files of Small Size

The [file browser within Open OnDemand](../software/onDemand/ondemand.md#using-open-ondemand) can be used to upload files directly into either your home or a project directory. It can't be used for accessing data on the Otago HCS.



### Transfer Multiple or Large Files

When it comes to transferring many files, or files that are large this is best done through either:

- [`scp` or `rsync`](rsync.md) to transfer through an `ssh` connection
- [Using globus](globus.md)