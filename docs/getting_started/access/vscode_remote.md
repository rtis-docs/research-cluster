# VSCode on Aoraki

!!! overview "On this Page"
    - How to connect VS Code to an Aoraki compute node via Slurm
    - How to configure SSH and VS Code settings
    - How to customise your Slurm resource allocation

!!! warning
    You must be on campus or connected to the campus VPN to access Aoraki. You also need SSH key-based authentication set up — see [SSH](login_ssh.md) if you haven't done this yet.

## Overview

Visual Studio Code's [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension lets you develop directly on a remote machine. On Aoraki, a proxy script runs `salloc` on your behalf when VS Code connects, allocating a compute node through Slurm and transparently forwarding all VS Code traffic to it.

This means you work on a compute node with dedicated CPU, memory, and (optionally) GPU resources — not on the shared login node.

!!! info "How it works"
    1. SSH executes the proxy script as your remote command on the login node.
    2. The proxy calls `salloc` with the resource arguments you configured, allocating a compute node.
    3. The proxy intercepts the VS Code backend's TCP listener port and substitutes a local port on the login node.
    4. All subsequent VS Code traffic is tunnelled through the proxy to the compute node transparently.

## Prerequisites

- An [Aoraki cluster account](signup.md)
- [SSH key-based authentication](login_ssh.md) set up and working
- [Visual Studio Code](https://code.visualstudio.com/) installed with the **Remote - SSH** extension (`ms-vscode-remote.remote-ssh`)

## Step 1: Configure SSH

Add the following host entry to your SSH configuration file:

=== "Windows"

    Open `%USERPROFILE%\.ssh\config` in a text editor (create the file if it does not exist) and add:

    ```text
    Host aoraki-vscode
      HostName aoraki-login.otago.ac.nz
      User <otago-username>
      RequestTTY force
      ForwardAgent yes
      ControlMaster no
      ControlPath none
      ServerAliveInterval 30
      ServerAliveCountMax 6
      RemoteCommand module load vscode-remote; vscode-shell-proxy.py -vv -l /tmp/vscode-proxy-[PID].log --salloc-arg=--time=10:00:00 --salloc-arg=--cpus-per-task=1 --salloc-arg=--mem=10G --salloc-arg=--partition=aoraki
    ```

    !!! info
        The `RemoteCommand` value must be on a **single line** with no line breaks.

=== "macOS / Linux"

    Open `~/.ssh/config` in a text editor (create the file if it does not exist) and add:

    ```text
    Host aoraki-vscode
      HostName aoraki-login.otago.ac.nz
      User <otago-username>
      RequestTTY force
      ForwardAgent yes
      ControlMaster no
      ControlPath none
      ServerAliveInterval 30
      ServerAliveCountMax 6
      ForwardX11 no
      ForwardX11Trusted no
      RemoteCommand module load vscode-remote; vscode-shell-proxy.py -vv -l /tmp/vscode-proxy-[PID].log --salloc-arg=--time=10:00:00 --salloc-arg=--cpus-per-task=1 --salloc-arg=--mem=10G --salloc-arg=--partition=aoraki
    ```

    !!! info
        The `RemoteCommand` value must be on a **single line** with no line breaks.

Replace `<otago-username>` with your Aoraki username in both the `User` and (if applicable) any path fields.

!!! tip "Default resource allocation"
    The example above requests a **10-hour** allocation with **1 CPU** and **10 GB** of memory on the `aoraki` partition. Increase these if your workload needs more — see [Customising your Slurm allocation](#customising-your-slurm-allocation) below.

## Step 2: Configure VS Code settings

By default, the Remote - SSH extension ignores `RemoteCommand` directives in your SSH config. You need to enable this setting explicitly.

=== "Windows"

    Windows also needs the extension to use a local server and dynamic forwarding rather than a UNIX socket. Add the following to your **user** `settings.json`:

    1. Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> and run **Preferences: Open User Settings (JSON)**.
    2. Merge these entries into the existing top-level JSON object:

    ```json
    {
        "remote.SSH.enableRemoteCommand": true,
        "remote.SSH.useLocalServer": true,
        "remote.SSH.enableDynamicForwarding": true,
        "remote.SSH.remoteServerListenOnSocket": false,
        "remote.SSH.connectTimeout": 300,
        "remote.SSH.logLevel": "trace"
    }
    ```

    !!! info
        If `settings.json` already contains settings, don't paste the outer braces — add the entries inside the existing object and make sure each line ends with a comma except the last.

=== "macOS / Linux"

    1. Open VS Code.
    2. Open **Settings** (<kbd>⌘</kbd>+<kbd>,</kbd> on macOS, <kbd>Ctrl</kbd>+<kbd>,</kbd> on Linux).
    3. Search for `remote.SSH.enableRemoteCommand`.
    4. Tick the checkbox to enable it.

!!! warning
    Without `remote.SSH.enableRemoteCommand`, VS Code will connect to the **login node** directly, ignoring the proxy script entirely. You won't have a Slurm allocation and will be working on the shared login node.

## Step 3: Connect

1. Open VS Code.
2. Press <kbd>F1</kbd> and run **Remote-SSH: Connect to Host…**
3. Select or type `aoraki-vscode`.
4. VS Code will open a new window. Once connected, the bottom-left corner shows **SSH: aoraki-vscode**.

The first connection may take a minute or two while Slurm finds an available compute node and VS Code installs its server-side components. Subsequent connections are faster.

!!! info
    A "waiting for server" spinner while connecting is normal — Slurm is queuing your job.

## Customising your Slurm allocation

The `--salloc-arg` options in your SSH config are passed directly to `salloc`. Common adjustments:

| Option | Description |
|--------|-------------|
| `--time=HH:MM:SS` | Maximum wall-clock time. Your session ends when this limit is reached. |
| `--cpus-per-task=N` | Number of CPU cores. |
| `--mem=XG` | Amount of RAM (e.g. `10G`, `32G`). |
| `--partition=<name>` | Slurm partition. Use `aoraki` for general CPU work. |
| `--gres=gpu:1` | Request a GPU (adjust count as needed). |

For example, to request a GPU with more memory:

```text
RemoteCommand module load vscode-remote; vscode-shell-proxy.py --salloc-arg=--time=10:00:00 --salloc-arg=--cpus-per-task=4 --salloc-arg=--mem=20G --salloc-arg=--partition=gpu --salloc-arg=--gres=gpu:1
```

## Ending your session

Close the VS Code remote window. The SSH connection drops, which signals the proxy to terminate `salloc` and release your Slurm allocation.

You can confirm the allocation has been released:

```bash
ssh <otago-username>@aoraki-login.otago.ac.nz squeue -u <otago-username>
```

## Troubleshooting

**VS Code hangs on "waiting for server"**
:   Your Slurm allocation is still pending. Check with `squeue -u $USER` on the login node. If the job is in state `PD` it is waiting for resources — consider requesting fewer CPUs/memory or a shorter `--time`.

**Connection drops unexpectedly**
:   Your Slurm wall-clock limit was reached. Increase `--time` in your SSH config.

**"Module not found" or Python errors on connect**
:   The `vscode-remote` module automatically loads its Python dependency. Check that both are available: `module avail vscode-remote` and `module avail python`. If either is missing, contact the RTIS team.

**Debugging with log files**
:   Add `-vv -l /tmp/vscode-proxy.log` to the end of the `RemoteCommand` (before any line break). Retrieve the log after a failed attempt:

    ```bash
    ssh <otago-username>@aoraki-login.otago.ac.nz cat /tmp/vscode-proxy.log
    ```

!!! related-pages "What's next?"
    * Submit batch jobs from your VS Code terminal: [Slurm quickstart](../running/batch/slurm_quickstart.md)
    * Available software on the cluster: [Application Libraries](../software/applications/index.md)
    * Need help? Contact the [RTIS team](../../general/support.md)
