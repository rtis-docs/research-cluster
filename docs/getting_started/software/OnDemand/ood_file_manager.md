---
tags:
    - OnDemand
    - storage
    - "data transfer"
---

# Using the OnDemand File Manager

!!! overview "On this Page"
    - What the OnDemand File Manager is
    - How to open it
    - What you can do with it
    - When to use something else instead

The OnDemand File Manager is the browser-based file browser built into the [Open OnDemand](ondemand.md) portal. It is the quickest way to look at, edit, upload and tidy up files on the cluster without opening a terminal.

## Opening the File Manager

1. Log in to [https://ondemand.otago.ac.nz](https://ondemand.otago.ac.nz).
2. From the top menu, select **Files > Home Directory**, or **Files > Projects** for your group's project storage.

![The Files app](../../../assets/images/ood_files_app.png){width="600px"}{ .left }

## What You Can Do

- **Browse directories:** Navigate through your [home directory](../../../storage/data_locations/homes.md) and your [projects](../../../storage/data_locations/projects.md) storage.
- **Upload and download:** Click **Upload** to add files from your computer, or select files and click **Download** to save them locally.
- **Create and delete:** Create new folders and files, and delete items you no longer need.
- **Rename and move:** Right-click a file or folder to rename or move it.
- **Edit files:** Click a text file to open it in the built-in editor for quick changes.
- **Hand off to Globus:** Use the **Open in Globus** button to start a [Globus](../../../storage/data_transfer/globus.md) transfer from the directory you are in.

## What It Can't Reach

The **Files** menu covers your home and projects directories. Other storage on the cluster is reachable, but not from this file browser:

- [**Weka**](../../../storage/data_locations/weka.md) — use a [shell session](ood_shell.md) or an [HPC Desktop](hpc_desktop.md).
- [**Otago HCS**](../../../storage/data_locations/hcs.md) — needs a Kerberos ticket, so mount it from a [shell session](ood_shell.md) or an [HPC Desktop](hpc_desktop.md).

## When to Use Something Else

The file manager is built for everyday operations — a handful of files at a time. For anything bigger:

- **Large or bulk transfers:** use [Globus](../../../storage/data_transfer/globus.md), [rclone](../../../storage/data_transfer/rclone.md), or [rsync and scp](../../../storage/data_transfer/rsync.md).
- **Anything scripted or repeated:** use a [shell session](ood_shell.md) and do it on the command line.

See [Data Transfer](../../../storage/data_transfer/data_transfer_overview.md) for a comparison of the options.

<!-- TODO needs some pictures for this page -->

!!! related-pages "What's next?"
      - For more information about OnDemand see the [Open OnDemand Overview](ondemand.md)
      - For where your data should live, see the [Storage Overview](../../../storage/storage_options.md)
      - Looking for something else? See the [Software Overview](../index.md)
