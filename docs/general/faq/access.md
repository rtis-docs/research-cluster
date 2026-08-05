# Access and Login

!!! overview "On this Page"
    - Why a connection is refused, and the VPN requirement
    - SSH keys that do not work
    - A login that fails or hangs after your password
    - Telling the login node and compute nodes apart

## Why Can I Not Connect to the Cluster?

The most common reason is the network you are on. SSH to `aoraki-login.otago.ac.nz` is only
reachable **from the University network** — either on campus, or connected to the campus
VPN. From home without the VPN the connection will simply time out.

Work through these in order:

1. **Are you on campus or on the VPN?** If not, connect to the VPN and try again.
2. **Do you have an account?** Cluster access is not automatic with a University account.
   See [How do I get an account?](#how-do-i-get-an-account)
3. **Is it just you?** [https://ondemand.otago.ac.nz](https://ondemand.otago.ac.nz) does not
   need the VPN. If OnDemand works and SSH does not, the problem is your network or SSH
   configuration rather than your account.
4. **Is there maintenance on?** Check the **Announcements** section for scheduled outages.

If none of those explains it, email {{ support_email }} with the exact error message and the
output of `ssh -v <username>@aoraki-login.otago.ac.nz`.

## Why Am I Still Asked for a Password After Setting Up an SSH Key?

Your key is not being offered, or the server is not accepting it. In order of likelihood:

- **The key was never copied to the cluster.** Run `ssh-copy-id`, or register it through
  OnDemand — see [Setting up SSH key access](../../getting_started/access/login_ssh.md#setting-up-ssh-key-access).
- **You are connecting as the wrong user.** Use your University username, not your email
  address. (OnDemand is the opposite: it wants the full email address.)
- **Your home directory or `~/.ssh` has permissions that are too open.** SSH refuses keys in
  that case. On the cluster, `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys`.
- **Your home directory is full**, so `authorized_keys` could not be written. See
  [below](#my-login-fails-or-hangs-straight-after-my-password-what-is-wrong).

`ssh -v` will show which keys your client offered and how the server responded.

## My Login Fails or Hangs Straight After My Password. What Is Wrong?

Check whether your **home directory is full**. Your shell has to write to your home
directory as it starts, so at the hard quota a login can hang, drop straight back out, or
land you at a `-bash-5.1$` prompt with none of your usual settings.

The quickest way to confirm it is to log in to
[OnDemand](https://ondemand.otago.ac.nz) and use the **Files** app, which will show your
home directory even when a shell login will not complete.

See [Storage and Quotas](disk_usage.md) for what usually fills a home directory and how to
clear it. If you cannot get in at all, email {{ support_email }} — we can free enough space
to get you back to a working shell.

## How Do I Get an Account?

Cluster access is provisioned separately from your University account. Fill in the
[account request form](../../getting_started/access/signup.md); requests are normally
processed within one business day and you will be emailed when it is ready.

Storage allocations are requested separately again — see
[Storage Request](../../storage/storage_request.md).

## Should I Use SSH or OnDemand?

Both reach the same cluster, the same files and the same scheduler. Use whichever suits the
task.

| | [SSH](../../getting_started/access/login_ssh.md) | [OnDemand](../../getting_started/software/OnDemand/ondemand.md) |
| :-- | :-- | :-- |
| Needs the VPN off campus | Yes | No |
| Best for | scripting, `sbatch`, `rsync`, anything repeatable | notebooks, RStudio, graphical software, browsing files |
| Survives a dropped connection | No, unless you use `tmux` | Yes — sessions keep running |
| Setup | SSH key, one time | None |

## Which Machine Am I On?

!!! terminal

    ```bash
    hostname
    ```

`aoraki-login` is the login node — shared by everyone, and not where your analysis should
run. A name like `aoraki07` or `aoraki-g01` is a compute node, which means you are inside a
Slurm allocation.

## Why Was My Program Killed as Soon as It Started?

If you were on the login node, it was probably killed for using too much of it. Each user is
limited to **8 CPUs and 60 GB of memory** there, and exceeding that triggers a warning email
and possible cancellation.

The login node is for editing scripts, moving data and submitting work. To actually run
something, ask Slurm for an allocation — see
[Interactive Sessions from the Command Line](../../getting_started/running/interactive/interactive_shell.md)
or the [Slurm Quickstart](../../getting_started/running/batch/slurm_quickstart.md), and
[Login Node Usage](../guidelines/login_node_usage.md) for what is and is not reasonable
there.

!!! related-pages "What's next?"
    - To set up SSH, see [SSH](../../getting_started/access/login_ssh.md)
    - To use the browser instead, see [Logging in to OnDemand](../../getting_started/access/ondemand_web.md)
    - Once you are in, see [Running Jobs](../../getting_started/running/running_jobs_overview.md)
    - For what the login node is for, see [Login Node Usage](../guidelines/login_node_usage.md)
