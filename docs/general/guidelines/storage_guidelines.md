---
tags:
  - storage
---

# Storage Guidelines

Storage on the Research Cluster is a shared resource, and each area is provided for a particular purpose. These guidelines cover what each area is for, how to get one, how long data should stay there, and who is responsible for keeping it safe.

For the full detail on each area, see the [Storage Overview](../../storage/storage_options.md).

## At a Glance

| | [Home](../../storage/data_locations/homes.md) | [Projects](../../storage/data_locations/projects.md) | [Weka](../../storage/data_locations/weka.md) | [Otago HCS](../../storage/data_locations/hcs.md) |
| :-- | :-- | :-- | :-- | :-- |
| _Provided_ | With every account | On request | On request | Via AskOtago |
| _Intended for_ | Scripts and configuration | Data you are actively working on | High-throughput scratch | Long-term storage and backup |
| _Backed up_ | :material-check: | :material-close: | :material-close: | :material-check: |
| _Default quota_ | {{ home_quota }} | Set on request | 0 GB | Managed by Core Digital |

## Home Directories

Every user of the Research Cluster gets a home directory at `/home/<username>`. It is provided for managing your **scripts, configuration files, and other smaller files** used in your computations.

- The hard quota is **{{ home_quota }}**. Once you hit it you will not be able to write any more data.
- You will be emailed at your Otago address once you reach **30 GB**.
- Home directories **are** backed up: one snapshot per day for the last 7 days, one per week for the last 4 weeks, and one per month for the last 6 months.

Home directories are not the place for research datasets. If you are working with data at any scale, request a projects allocation.

## Projects and Weka

[`/projects`](../../storage/data_locations/projects.md) and [`/weka`](../../storage/data_locations/weka.md) are available **on request** through the [Storage Request](../../storage/storage_request.md) page.

Both are allocated to a group rather than an individual, so a request must name:

- The **department** the allocation belongs to, and
- The **principal investigator**, who is the data owner and is responsible for the data held in the allocation.

Quotas are set when the allocation is created and can be revised on request.

These areas are for data that is **in use**. The expected pattern is to copy your source data in from HCS, work on it, transfer the results back, and remove the working copy once you are finished. Weka in particular is scratch space — data written to `/tmp/` during a job is deleted when the job ends.

## Backups Are Your Responsibility

!!! warning "Only home directories are backed up"
    Nothing in `/projects` or `/weka` is backed up. If you delete something there, or a disk fails, it is gone. It is your responsibility to make sure your important data is safe.

Your research data should have a copy on **[Otago HCS](../../storage/data_locations/hcs.md)**, which is backed up and is the recommended long-term home for it. Treat the cluster copy as a working copy that you can afford to lose.

Recommended practice:

1. Keep the authoritative copy of your data on HCS.
2. Copy what you need into `/projects` to work on.
3. Transfer results back to HCS when you are done.
4. Remove the working copy from the cluster.

Setting up [Globus](../../storage/data_transfer/globus.md) to transfer between the two on a schedule is a good way to keep this up to date without having to remember. See [Data Transfer](../../storage/data_transfer/data_transfer_overview.md) for the options.

!!! note
    If you do not have an HCS share for your department or group, fill out the [HCS Access Form](https://www.otago.ac.nz/its/forms/high-capacity-central-storage-hcs).

## Questions

If you are unsure which storage area suits your work, how much to request, or how to go about backing up your data, email the eResearch Support team at **{{ support_email }}** — we are happy to help you work it out.

!!! related-pages "What's next?"
    - [Storage Overview](../../storage/storage_options.md)
    - [Storage Request](../../storage/storage_request.md)
    - [Data Transfer](../../storage/data_transfer/data_transfer_overview.md)
    - [File Permissions](../../storage/file_permissions.md)
    - [Reasonable Usage](reasonable_usage.md)
