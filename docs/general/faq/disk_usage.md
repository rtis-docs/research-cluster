# Disk Usage and Storage Management

## How much disk storage am I using?

For your home directory this will give you an indication of how much space each directory is currently occupying 

!!! terminal

    ```bash
    du -h -d 1 -c ~/
    ```

## What should I do if my home directory is full?

When your home directory is full on the cluster, you may encounter issues with logging in, running jobs, or saving files. Follow the steps below to diagnose and resolve the issue.

### Check what's using space

Use the following command to see which files and directories are taking up the most space:

!!! terminal

    ```bash
    du -ahx --max-depth=2 $HOME | sort -k1 -rh
    ```

- `du -ahx`: Lists all files and directories with sizes.
- `--max-depth=2`: Limits the depth of directory traversal (you can increase if needed).
- `sort -k1 -rh`: Sorts the results from largest to smallest in human-readable format.

### Clean up unnecessary files

Once you've identified the largest files or folders, you can:

- **Delete unnecessary files:**

!!! terminal

    ```bash
    rm large_file.bam
    ```

- **Compress and archive old directories:**

!!! terminal

    ```bash
    tar -czf old_data.tar.gz old_data/
    ```

### Move or migrate data

Research data and large files should not be stored in your home directory. Instead, request a project directory on shared or scratch storage. Contact the RTIS support team to request project or scratch storage.

### Manage Conda environments

Conda environments can consume significant space in your home directory. We recommend managing them carefully to reduce storage usage.

- Consider creating environments in a project directory instead of the default location in `$HOME/.conda`.
- Periodically remove unused environments.

For detailed advice, see our guide: https://researchcomputing.otago.ac.nz/cluster/storage.html#managing-conda-environments-to-conserve-home-directory-storage

### Prevent future issues

- Regularly monitor your disk usage.
- Avoid saving large SLURM job outputs in your home directory.
- Use project or scratch space for compute-intensive or large-scale data workloads.