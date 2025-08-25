TODO

!!! overview "On this Page"
      -
  <!-- TODO Overview unclear -->

The storage on Aoraki uses 2 systems of file permissioning. 

Location | Unix permissions | ACL Permissions
---|---|---
/home/<username\> | :material-check: | :material-close:
/projects | :material-check: | :material-check:
/weka | :material-check: | :material-close:

## Unix Permissions

Unix file permissions control who can read, write, or execute a file or directory. They apply to three categories:

- Owner – the user who owns the file
- Group – users in the file's group
- Others – all other users

📜 Permission Types

Symbol	| Meaning
---|---
r	| Read
w	| Write
x	| Execute
-	| No permission


For example, given `-rwxr-xr--` the permissions would be:

- Owner	`rwx`	Read, write, execute
- Group	`r-x`	Read, execute only
- Others	`r--`	Read only

To view or change the Unix permissions on a file

!!! terminal

    ```bash
    # View permissions
    ls -l filename
    ```

### Modifying permissions with `chmod`

TODO

## Access Control Lists (ACL)

ACLs extend the standard Unix file permission model (owner/group/others) by allowing fine-grained access control for additional users and groups on a per-file or per-directory basis.

Where the standard permissions (chmod) set access for:

- Owner
- Group
- Others

ACLs allow for:

- Specific users (e.g., user:bob)
- Specific groups (e.g., group:research)
- Default rules for directories (e.g., default:user:bob)


NFSv4 ACL Breakdown
Each line has the form:

bash
Copy
Edit
A:(type):[who]:permissions
Where:

A = allow (you might also see D = deny)

OWNER@, GROUP@, EVERYONE@ = NFSv4 built-in identities

u:username@domain = specific user

g:group@domain = specific group

Code |	Name |	What it allows
---|---|---
r	| Read Data	| Read file contents or list directory contents
w	| Write Data	| Modify file contents or create files in a directory
a	| Append Data	| Append to a file or create subdirectories in a directory
D	| Delete Child	| Delete files within a directory
x	| Execute	| Execute file or traverse directory
t	| Read Attributes	| View basic file metadata (size, timestamps)
T	| Write Attributes	| Modify basic file metadata (e.g. change timestamps)
n	| Read Named Attributes	| Access extended attributes
N	| Write Named Attributes	| Modify extended attributes
c	| Read ACL	| View the ACL of the file
C	| Write ACL	| Modify the ACL of the file
y	| Synchronize	| Ensure file changes are written to stable storage (fsync)



Example

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


    NFSv4 ACL Entries Explained
Entry	|Who it applies to	|Permissions	|Meaning
---|---|---|---
A::OWNER@:rwaDxtTnNcCy	|File owner	|rwaDxtTnNcCy	|Full access
A::GROUP@:rxtncy	|File group	|rxtncy	|Read + Execute + Metadata access
A::EVERYONE@:rxtncy	|Everyone else	|rxtncy	|Read + Execute + Metadata access



!!! related-pages "What's next?"
    
  <!-- TODO Unknown Next Page -->