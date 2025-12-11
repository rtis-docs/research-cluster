# Otago HCS (High Capacity Storage) 
!!! overview "On this Page"
      - To see where HCS fits within Storage check out [Storage Overview](../storage_options.md)
      - What is HCS (High Capacity Storage)
      - How to mount HCS on the Login node
      - How to mount HCS on the cluster nodes
      - How to Generate Auto Renewal Kereberos Tickets.
  <!-- TODO Fill out -->

HCS is the main data storage pool on the Otago campus. HCS is able to be mounted on desktop and lab computers. It is possible to mount HCS shares on the Cluster Login node to transfer data across but the connection is sub-optimal for high-speed computing and cannot (easily) be mounted across nodes in the cluster. We recommend that you use the HCS for your primary storage needs and transfer your data to your working area in `/projects/` when you want to work on it, and transfer results back to HCS for long term storage. 

!!! note
    If you do not have an HCS share available for your department/group, please fill out the _[HCS Access Form](https://www.otago.ac.nz/its/forms/high-capacity-central-storage-hcs)_ .

### Accessing HCS within the OnDemand HPC Desktop

**SMB Local Mount from HPC Desktop GUI**  

  1. Start an Otago HPC Desktop 
  2. Open a Terminal window on the desktop
  3. Type "kdestroy" to remove invalid older tickets
  4. Type "kinit" and Enter your password 
  5. Open File browser window  
  6. Connect and login to HCS by entering the smb://username@storage.hcs-p01.otago.ac.nz/share-name address  
  7. When the authentication window appears type in the domain "registry" if staff or "student" if you are using a student account, and your password  
  8. Press connect and wait a few seconds for authentication and your HCS files to appear in the window.  

<!-- TODO add paragraphs explaining the images -->
![Connecting to HCS - create kerberos ticket with `kinit`](/assets/images/kinit.png){width="600px"}






![Connect to HCS - authenticating using samba in the file browser](/assets/images/smbauth.png){width="600px"}


![Connect to HCS - browsing hcs files in file browser](/assets/images/files.png){width="600px"}


### Accessing HCS on the Login node


For small one job data transfers, you can mount your HCS share on the login node. This is not recommended for large data transfers or for data that will be used in a job as the connection is not optimal for high-speed computing. 
It can also be mounted on an HPC desktop for smaller data sets and transfers.

To mount your HCS share on the login node, you will need to have a valid Kerberos ticket. If you do not have a valid Kerberos ticket, you can generate one by running the ``kinit`` command and entering your University password.


Otago HCS (High Capacity Storage) shares can be accessed on the cluster provided you have security access and obtain a Kerberos ticket (password authentication).
    To access your HCS share:
    1. Check if you have a kerberos ticket ``klist``. If not, obtain Kerberos ticket ``kinit`` and entering your University password.
    3. Navigate to your HCS share ``/mnt/auto-hcs/<your_share_name>`` (the last portion of the HCS address)
        eg. if my share is ``\\storage.hcs-p01.otago.ac.nz\its-rtis`` then navigate to ``/mnt/auto-hcs/its-rtis``

  Occasionally, it may take up to a minute for this access to become available after running ``kinit``.

Otago MDS storage (Windows Managed Desktop Share) can be access on the cluster if you have a Kerberos ticket.
    To access your MDS share:
    1. Check if you have a Kerberos ticket ``klist``. If not, obtain Kerberos ticket ``kinit`` and entering your University password.
    2. Navigate to your HCS share ``/mnt/auto-mds/<your_first_inital_of_your_username>/<your_username>`` (the last portion of the HCS address)
        eg. if my MDS share is ``\\registry.otago.ac.nz\mdr\Profiles-V2\h\higje06p`` then navigate to ``/mnt/auto-mds/h/higje06p``

### Accessing HCS on the cluster nodes - Auks


The Auks Slurm plugin enables users to save their Kerberos ticket from the login node onto the Auks server. This saved ticket can then be used on any Slurm compute node to access HCS shares. The Kerberos ticket is automatically renewed by Auks and remains valid for up to 7 days. After this period, the ticket must be manually renewed. Once a user saves their Kerberos ticket, the renewal process happens automatically.

Whenever a user logs in to the Aoraki login node using their password, a new krbtgt (Kerberos Ticket-Granting Ticket) is issued. However, if the user logs in via SSH keys or accesses nodes through the OnDemand shell, they must manually obtain a new valid ticket by running the ``kinit`` command. When you type your password after running the ``kinit`` command, the terminal intentionally suppresses any visible feedback. Confirm your password by pressing Enter key. 


=== "STAFF"

    !!! terminal "code"

        ```bash
        kinit userx01p@REGISTRY.OTAGO.AC.NZ
        Password for userx01p@REGISTRY.OTAGO.AC.NZ:
        ```

=== "STUDENTS" 

    !!! terminal "code"

        ```bash
        kinit studx012@STUDENT.OTAGO.AC.NZ
        Password for studx012@STUDENT.OTAGO.AC.NZ:
        ```


A krbtgt (Kerberos Ticket-Granting Ticket) is valid for 10 hours, as indicated by the "Expires" date and time. During this period, the ticket can be renewed using the ``kinit -R`` command. This renewal extends the "Expires" time but does not change the "Renew Until" date and time. The Auks system handles this renewal process automatically for the user.

As long as a user has a valid krbtgt ticket, they can communicate with the Auks server seamlessly.

Check if you have a valid krbtgt ticket:  

!!! terminal

    ```bash
    [studx012@aoraki-login ~]$ klist
    ```

    ```output
    Ticket cache: KCM:40005987:63840
    Default principal: studx012@STUDENT.OTAGO.AC.NZ

    Valid starting Expires Service principal
    11/26/2024 08:56:14 11/26/2024 18:56:14 krbtgt/STUDENT.OTAGO.AC.NZ@STUDENT.OTAGO.AC.NZ
        renew until 12/03/2024 08:56:14
    ```

    ```bash
    [studx012@aoraki-login ~]$ kinit -R
    [studx012@aoraki-login ~]$ klist
    ```
    
    ```output
    Ticket cache: KCM:40005987:63840
    Default principal: studx012@STUDENT.OTAGO.AC.NZ

    Valid starting Expires Service principal
    11/26/2024 11:22:40 11/26/2024 21:22:40 krbtgt/STUDENT.OTAGO.AC.NZ@STUDENT.OTAGO.AC.NZ
        renew until 12/03/2024 08:56:14
    ```

Ping server to verify connection:

!!! terminal
    ```bash
    [studx012@aoraki-login ~]$ auks -p
    ```

    ```output
    Auks API request succeed
    ```

Save current krbtgt on the ausk server:


!!! terminal 
    
    ```bash
    [studx012@aoraki-login ~]$ auks -a
    ```
    
    ```output
    Auks API request succeed
    ```

Now you can use `--auks=yes` option with srun or `#SBATCH --auks=yes` in you slurm batch script:

!!! terminal
    ```bash
    srun --auks=yes --partition=aoraki ls -lah /mnt/auto-hcs/hcs_share_name
    ```

HCS shares are automatically mounted on each node when requested. The user's krbtgt, retrieved from the Auks server, is used to generate Kerberos tickets for communication with the HCS storage servers. However, obtaining these tickets can take some time. If the HCS share is not yet mounted on the node, the job or script may fail.

To mitigate this, it is recommended to include a command such as sleep 20 in batch scripts before accessing the automounted share. 

#### Generating Auto Renewal Kerberos Tickets


!!! info

    If you want to keep using your data over hours or days you will need to renew your Kerberos ticket.  Kerberos tickets are only valid for 1 hour and then need to be renewed either by generating one via the command line or 
    automatically by generating a keytab file and setting a cronjob to renew the ticket at a specified interval.

    To see if you have a valid Kerberos ticket you can type ``klist`` 

    1. You do not have a valid ticket if you get a message like: *klist: Credentials cache 'KCM:51776880' not found*
    2. You do have a ticket if you get a message similar to:


=== "STAFF"

    !!! terminal

    ```bash
    klist
    ```

    ```output
    Ticket cache: KCM:51776880 Default principal: higje06p@REGISTRY.OTAGO.AC.NZ

    Valid starting     Expires            Service principal
    27/09/23 15:01:57  28/09/23 01:01:57  krbtgt/REGISTRY.OTAGO.AC.NZ@REGISTRY.OTAGO.AC.NZ
        renew until 04/10/23 15:01:57
    ```

    **To generate an auto renewing ticket (so as to not expire):**

    - *Create a keytab file - replace *username* *with your otago username:*

    !!! terminal

    ```bash
    ktutil

    ktutil: addent -password -p <username>@REGISTRY.OTAGO.AC.NZ -k 1 -e aes256-cts (enter your password)
    Ktutil: wkt /home/<username>/<username>.keytab
    Ktutil: quit
    ```


    - To test: ``kinit  *username*@REGISTRY.OTAGO.AC.NZ -k -t 'username'.keytab``
    - ``klist`` (to check if ticket is valid)
    - Then create a cronjob to renew your ticket ``crontab -e`` then enter the following line to renew your ticket every hour:
    ``0 * * * * kinit  *username*@REGISTRY.OTAGO.AC.NZ -k -t /home/*username*/*username*.keytab``
    - Ensure the permissions on your .keytab file are ``0600`` to keep it secure!

=== "STUDENTS"

    !!! terminal

    ```bash
    klist
    ```

    ```output
    Ticket cache: KCM:51776880 Default principal: higje06p@STUDENT.OTAGO.AC.NZ

    Valid starting     Expires            Service principal
    27/09/23 15:01:57  28/09/23 01:01:57  krbtgt/STUDENT.OTAGO.AC.NZ@STUDENT.OTAGO.AC.NZ
        renew until 04/10/23 15:01:57
    ```
    
    **To generate an auto renewing ticket (so as to not expire):**

    - *Create a keytab file - replace *username* *with your otago username:*

    !!! terminal

    ```bash
    ktutil

    ktutil: addent -password -p <username>@STUDENT.OTAGO.AC.NZ -k 1 -e aes256-cts (enter your password)
    Ktutil: wkt /home/<username>/<username>.keytab
    Ktutil: quit
    ```


    - To test: ``kinit  <username>@STUDENT.OTAGO.AC.NZ -k -t 'username'.keytab``
    - ``klist`` (to check if ticket is valid)
    - Then create a cronjob to renew your ticket ``crontab -e`` then enter the following line to renew your ticket every hour:
    ``0 * * * * kinit  <username>@STUDENT.OTAGO.AC.NZ -k -t /home/<username>/<username>.keytab``
    - Ensure the permissions on your .keytab file are ``0600`` to keep it secure!


!!! related-pages "What's next?"
    Find out how to move Data on and off the Research Cluster on [Data Transfer](../../getting_started/data_transfer/data_transfer_overview.md) 
  <!-- TODO Are these pages the next step or relevant? -->