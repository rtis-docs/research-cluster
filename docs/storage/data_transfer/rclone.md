# rclone (Kerberos auth for HCS)

This guide sets up `rclone` instead, which is multi-threaded

This is a one-time setup per user, plus a ~10-second re-auth step whenever
your Kerberos ticket expires (typically once per session/day).

---

## 1. Load the rclone module

```bash
module load rclone
```

Add this to your `~/.bashrc` (or shell profile) if you want it available on
every login without typing it each time.

## 2. Create the rclone remote (one-time setup)

Replace `hpcshare` with whatever name you like:

```bash
rclone config create hpcshare smb \
  host=storage.hcs-p01.otago.ac.nz \
  use_kerberos=true \
  kerberos_ccache=/tmp/krb5cc_$USER \
  --non-interactive
```

This writes a section to `~/.config/rclone/rclone.conf`:

```ini
[hpcshare]
type = smb
host = storage.hcs-p01.otago.ac.nz
use_kerberos = true
kerberos_ccache = /tmp/krb5cc_YOURUSERNAME
```

You only need to do this once — it's saved for future logins.

> **Why `kerberos_ccache` is set explicitly:** our default Kerberos cache is
> `KCM:` (sssd's cache manager), not a plain file, and rclone's Kerberos
> library can only read a file-based cache. Pointing it at
> `/tmp/krb5cc_$USER` gives rclone its own file ticket without touching your
> normal login ticket.

## 3. Get a ticket for rclone

Each session (or whenever your ticket expires), run:

```bash
kinit -c /tmp/krb5cc_$USER $USER@REGISTRY.OTAGO.AC.NZ
```

Enter your normal AD password when prompted. This does **not** replace or
affect your regular login ticket — it's a separate file-based one just for
rclone.

**Optional shortcut** — add this alias to `~/.bashrc`:

```bash
alias hpcshare-auth='kinit -c /tmp/krb5cc_$USER $USER@REGISTRY.OTAGO.AC.NZ'
```

Then you just run `hpcshare-auth` and enter your password when needed.

## 4. Test the connection

```bash
rclone lsd hpcshare:
```

This should list the top-level shares on the server (e.g. `sci-cosc`,
`its-rtis`, etc.) without any further prompts.

If you get `stat /tmp/krb5cc_...: no such file or directory`, your ticket
expired or you skipped step 3 — just re-run the `kinit -c` command.

## 5. Browse a specific share

```bash
rclone lsd hpcshare:sharename
rclone lsf hpcshare:sharename/some/subfolder
```

## 6. Transfer files

**Copy files from the share to your local/HPC storage:**

```bash
rclone copy hpcshare:sharename/path/on/share ~/local-dest --transfers=8 --checkers=8 -P -v
```

**Copy files the other way (local → share):**

```bash
rclone copy ~/local-source hpcshare:sharename/path/on/share --transfers=8 --checkers=8 -P -v
```

`-P` (`--progress`) shows a live, continuously-updating status line (speed,
ETA, % done, files queued/done). `-v` logs each file as it starts/completes,
so you can see exactly which file it's on rather than just an aggregate
percentage. Without these flags rclone is silent unless something goes
wrong — a transfer with no visible output is very likely still working, not
stuck, especially on shares with deep folder structures where metadata
operations can pause before the first byte moves.

- `--transfers=8` runs 8 files in parallel — this is the main reason it's
  much faster than Thunar/GVfs.
- Re-running the same `copy` command later only transfers files that are
  new or changed (rclone compares size + modification time automatically),
  so it's safe to re-run for incremental syncs.
- Use `rclone sync` instead of `copy` if you want the destination to be an
  exact mirror of the source (**this deletes files at the destination that
  aren't in the source** — always test with `--dry-run` first):

```bash
rclone sync hpcshare:sharename/path ~/local-dest --dry-run
```

## 7. Mount the share as a browsable folder (optional)

If you'd rather browse the share in Thunar than use the command line:

```bash
mkdir -p ~/smb-share
rclone mount hpcshare: ~/smb-share --vfs-cache-mode writes --daemon
```

Then open `~/smb-share` in Thunar like a normal folder. To unmount:

```bash
fusermount -u ~/smb-share
```

This works on any login node — no root, no static `/etc/fstab` entry needed
— which matters since you land on a different node each session.

---

## Quick reference (after initial setup)

```bash
module load rclone
hpcshare-auth                      # kinit for rclone (once per session)
rclone lsd hpcshare:               # sanity check
rclone copy hpcshare:share/path ~/local-dest --transfers=8 --checkers=8 -P -v
```


## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `stat /tmp/krb5cc_...: no such file or directory` | Ticket expired or never created | Re-run `kinit -c /tmp/krb5cc_$USER ...` |
| `"hpcshare" refers to a local folder` | Forgot the trailing colon | Use `hpcshare:` not `hpcshare` |
| Slow transfers even via rclone | Too few parallel transfers | Increase `--transfers` (e.g. `--transfers=16`) |