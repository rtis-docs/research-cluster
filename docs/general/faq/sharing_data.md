# Sharing and Moving Data

!!! overview "On this Page"
    - Why a colleague cannot read your files, and how to fix it
    - Where data a group works on should live
    - Choosing a transfer tool for the amount of data you have
    - Sharing with people outside the University

## A Colleague Cannot Read My Files

Start by looking at what the permissions actually are:

!!! terminal

    ```bash
    ls -ld /projects/.../shared_folder
    ls -l  /projects/.../shared_folder/data.csv
    ```

    ```output
    drwxr-x--- 3 abcde01 rtis.mygroup 4096 Aug  4 09:12 shared_folder
    -rw-r----- 1 abcde01 rtis.mygroup  2.1M Aug  4 09:15 data.csv
    ```

Three things have to be true for someone else to read a file:

1. **They are in the group that owns it** — the second name in the `ls -l` output. `groups`
   shows which groups you are in; `id <username>` shows someone else's.
2. **The group has read permission on the file** — the middle `r--` triplet.
3. **The group can traverse every directory above it.** This is the one people miss. A
   directory needs `x` for the group as well as `r`, and *every* parent directory in the path
   needs it too. A perfectly readable file inside a `drwx------` directory is unreachable.

To open a directory tree up to its group:

!!! terminal

    ```bash
    chmod -R g+rX /projects/.../shared_folder
    ```

`g+rX` adds group read everywhere, and group *execute* only on directories and on files that
were already executable — which is almost always what you want.

New files often come out with the wrong group. Setting the setgid bit on the directory makes
everything created inside it inherit the directory's group:

!!! terminal

    ```bash
    chmod g+s /projects/.../shared_folder
    ```

!!! note "`/projects` also supports ACLs"
    Unix permissions have only one group. When you need to give two different groups
    different access, or grant one person access without adding them to a group, `/projects`
    supports NFSv4 access control lists. `/home` and `/weka` do not. See
    [File Permissions](../../storage/file_permissions.md#access-control-lists-acls).

Nothing in your **home directory** should be shared — it is not the place for it, and other
users cannot reach it. Move the data to `/projects` instead.

## Where Should Data My Group Shares Live?

In a `/projects` allocation. These are allocated to a department and research group, at
`/projects/<division>/<school>/<dept>/<group>/`, with the principal investigator as the data
owner — so group access is the default rather than something you have to arrange.

If your group does not have one, request it through [Storage Request](../../storage/storage_request.md).
See [Storage Guidelines](../guidelines/storage_guidelines.md) for what belongs where.

## How Do I Copy Data On and Off the Cluster?

Match the tool to the amount of data:

Table: Choosing a transfer tool

| How much | Use | Why |
| :-- | :-- | :-- |
| A few small files | The [OnDemand file browser](../../getting_started/software/OnDemand/ood_file_manager.md) | Drag and drop, nothing to install, no VPN needed |
| Up to a few GB | [`scp` or `rsync`](../../storage/data_transfer/rsync.md) | Already installed; `rsync` resumes and skips unchanged files |
| Large volumes, or anything you will repeat | [Globus](../../storage/data_transfer/globus.md) | Restarts itself after a dropped connection, verifies what it moved, and runs unattended |
| To or from Otago HCS | [rclone](../../storage/data_transfer/rclone.md) or Globus | Both handle HCS; the OnDemand file browser does not |

!!! tip "Large transfers on the login node"
    Copying data is one of the things the login node is for, but keep it under about 30
    minutes — see [Login Node Usage](../guidelines/login_node_usage.md). For anything longer,
    use Globus, which does not need you to stay connected at all.

`rsync` over many small files is slow. Tar the directory first and move one large file
instead — it is usually far quicker.

## Can I Share Data with Someone Outside Otago?

Yes, with [Globus](../../storage/data_transfer/globus.md). It can transfer directly between
the cluster and an endpoint at another institution, and most New Zealand and international
research organisations already run one. Your collaborator needs a Globus account, which is
free and can use their own institutional login.

Do not try to solve this by loosening permissions on `/projects` — people outside the
University have no account on the cluster, so there is nothing to grant access to.

For sensitive or restricted data, check your obligations before moving it anywhere. Email
{{ support_email }} if you are unsure what is appropriate.

## How Do I Move Data to and from HCS?

[Otago HCS](../../storage/data_locations/hcs.md) is the backed-up, long-term home for
research data; the cluster holds the working copy. If you have a share, it is mounted at
`/mnt/auto-hcs/<share name>` and you can copy to and from it like any other path.

The recommended pattern is:

1. Keep the authoritative copy on HCS.
2. Copy what you need into `/projects` to work on.
3. Transfer results back to HCS when you are finished.
4. Remove the working copy from the cluster.

Setting up a scheduled [Globus](../../storage/data_transfer/globus.md) transfer means step 3
happens without you having to remember. If your department or group does not have an HCS
share, apply through the
[HCS Access Form](https://www.otago.ac.nz/its/forms/high-capacity-central-storage-hcs).

!!! related-pages "What's next?"
    - For all the transfer options, see [Data Transfer](../../storage/data_transfer/data_transfer_overview.md)
    - For permissions in detail, see [File Permissions](../../storage/file_permissions.md)
    - For what each storage area is for, see [Storage Guidelines](../guidelines/storage_guidelines.md)
    - If you are running out of space, see [Storage and Quotas](disk_usage.md)
