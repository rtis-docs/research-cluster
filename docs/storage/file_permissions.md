# File Permissions

!!! overview "On this Page"
      - Viewing and modifying file permissions
      - Unix permissions and `chmod`
      - NFSv4 Access Control Lists (ACLs)

The storage on Aoraki uses two systems of file permissions:

Location | Unix permissions | ACL Permissions
---|---|---
/home/<username\> | :material-check: | :material-close:
/projects | :material-check: | :material-check:
/weka | :material-check: | :material-close:

## Unix Permissions

Unix file permissions control who can read, write, or execute a file or directory. They apply to three categories:

- **Owner** — the user who owns the file
- **Group** — users in the file's group
- **Others** — all other users

### Permission types

Symbol | Meaning
---|---
r | Read
w | Write
x | Execute
- | No permission

For example, given `-rwxr-xr--` the permissions would be:

- Owner: `rwx` — Read, write, execute
- Group: `r-x` — Read, execute only
- Others: `r--` — Read only

To view the Unix permissions on a file:

!!! terminal

    ```bash
    ls -l filename
    ```

### Modifying permissions with `chmod`

Use the `chmod` command to change file permissions. You can use either symbolic or numeric notation.

**Symbolic notation:**

!!! terminal

    ```bash
    # Give the owner read and write, group read only, others no access
    chmod u=rw,g=r,o= filename

    # Add execute permission for the owner
    chmod u+x filename

    # Remove write permission from group and others
    chmod go-w filename
    ```

**Numeric (octal) notation:**

Each permission has a numeric value: read (4), write (2), execute (1). Add the values together for each category.

!!! terminal

    ```bash
    # Owner: rwx (7), Group: r-x (5), Others: r-- (4)
    chmod 754 filename

    # Owner: rw- (6), Group: r-- (4), Others: --- (0)
    chmod 640 filename
    ```

To apply permissions recursively to a directory and its contents, use the `-R` flag:

!!! terminal

    ```bash
    chmod -R 750 directory/
    ```

## Access Control Lists (ACLs)

ACLs extend the standard Unix file permission model (owner/group/others) by allowing fine-grained access control for additional users and groups on a per-file or per-directory basis.

Where standard permissions (`chmod`) set access for owner, group, and others, ACLs additionally allow rules for:

- Specific users (e.g. `u:bob`)
- Specific groups (e.g. `g:research`)
- Default/inherited rules for new files in directories

### NFSv4 ACL format

Each ACL entry (ACE) has the form:

```
A:(flags):(who):(permissions)
```

Where:

- `A` = allow (`D` = deny)
- Flags indicate inheritance and type (e.g. `d` = inherit to subdirectories, `f` = inherit to files, `g` = group)
- Who identifies the target: `OWNER@`, `GROUP@`, `EVERYONE@`, or `u:username@domain` / `g:group@domain`

### ACE permissions

Permissions can be combined. The full list:

Permission | Function
---|---
`r` | Read data (files) / list directory (directories)
`w` | Write data (files) / create file (directories)
`a` | Append data (files) / create subdirectory (directories)
`x` | Execute (files) / change directory (directories)
`d` | Delete the file/directory
`D` | Delete child — remove a file or subdirectory from the given directory (directories only)
`t` | Read attributes of the file/directory
`T` | Write attributes of the file/directory
`n` | Read named attributes of the file/directory
`N` | Write named attributes of the file/directory
`c` | Read the file/directory ACL
`C` | Write the file/directory ACL
`o` | Change ownership of the file/directory
`y` | Synchronize — ensure changes are written to stable storage

### Permission aliases

Aliases `R`, `W`, and `X` work similarly to POSIX read/write/execute:

Alias | Name | Expands to
---|---|---
`R` | Read | `rntcy`
`W` | Write | `watTNcCy` (with `D` added for directory ACEs)
`X` | Execute | `xtcy`

### Viewing ACLs

To view the ACL on a file or directory:

!!! terminal

    ```bash
    nfs4_getfacl /projects/
    ```

    ```output
    # file: /projects/
    A::OWNER@:rwaDxtTnNcCy
    A::GROUP@:rxtncy
    A::EVERYONE@:rxtncy
    ```

Breaking down these entries:

Entry | Who | Permissions | Meaning
---|---|---|---
`A::OWNER@:rwaDxtTnNcCy` | File owner | `rwaDxtTnNcCy` | Full access
`A::GROUP@:rxtncy` | File group | `rxtncy` | Read + execute + metadata
`A::EVERYONE@:rxtncy` | Everyone else | `rxtncy` | Read + execute + metadata

### Setting and modifying ACLs

To set an ACE:

!!! terminal

    ```bash
    nfs4_setfacl [OPTIONS] COMMAND file
    ```

To interactively edit existing ACEs:

!!! terminal

    ```bash
    nfs4_editfacl [OPTIONS] file
    ```

#### Commands

Commands are used when setting ACEs with `nfs4_setfacl`:

Command | Function
---|---
`-a acl_spec [index]` | Add ACL entries at index (default: 1)
`-x acl_spec \| index` | Remove ACL entries or entry at index
`-A file [index]` | Read ACL entries to add from a file
`-X file` | Read ACL entries to remove from a file
`-s acl_spec` | Set ACL to acl_spec (replaces existing ACL)
`-S file` | Read ACL entries to set from a file
`-m from_ace to_ace` | Modify in place: replace `from_ace` with `to_ace`

#### Options

Option | Name | Function
---|---|---
`-R` | Recursive | Apply ACE to a directory's files and subdirectories
`-L` | Logical | Used with `-R`, follows symbolic links
`-P` | Physical | Used with `-R`, skips symbolic links

### Use cases

#### Share a folder with a specific group

First, make the top level of your home directory traversable by the group. This lets group members navigate to the shared folder without being able to read other contents of your home directory:

!!! terminal

    ```bash
    nfs4_setfacl -a A:g:<group>:X $HOME
    ```

Create a folder for the shared data:

!!! terminal

    ```bash
    mkdir ~/share_group
    ```

Move any existing data to be shared into this folder:

!!! terminal

    ```bash
    mv <src> ~/share_group/
    ```

Apply the ACL recursively to all current files and directories, and set a default ACL so that new files created in the folder automatically inherit the correct group permissions:

!!! terminal

    ```bash
    nfs4_setfacl -R -a A:dfg:<group>:RX ~/share_group
    ```

#### Using an ACL file

You can define ACL entries in a file and apply them in one command. This avoids duplicate entries and keeps permissions consistent:

!!! terminal

    ```bash
    cat << EOF > ~/group_acl.txt
    A:fdg:<group>:rxtncy
    A::OWNER@:rwaDxtTnNcCy
    A:g:GROUP@:tcy
    A::EVERYONE@:rxtncy
    EOF

    nfs4_setfacl -R -S ~/group_acl.txt ~/share_group
    ```

!!! warning
    Any existing data moved into the shared folder will retain its original permissions. You will need to reapply the ACL to those files manually to grant group read access.


!!! related-pages "What's next?"
    - Learn about storage options on [Storage Overview](storage_options.md)
    - Find out how to transfer data on [Data Transfer](data_transfer/data_transfer_overview.md)
