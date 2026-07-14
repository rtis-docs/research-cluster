!!! overview "On this Page"
      
      - Sign up for Globus
      - How to use Globus to transfer data between High Capacity Storage (HCS) and Research Storage (Ohau)
      - Using Globus Conect Personal to transfer data between the Ohau and your desktop

## Before You Start

!!! warning
    If you haven't already registered for Globus access, please see [Globus Registration](./globus_registration.md) to set up your account.


## Transferring data between Otago High Capacity Storage and Research Storage (Ohau) with Globus

**[Globus](https://www.globus.org/)** is a high-speed, secure data transfer platform that is available to all University of Otago researchers. 
It is a great way to transfer large amounts of data between Otago HCS and the Research Storage, as well as to external institutes.



### How to log in to Globus and transfer data


If you have used Globus before, this process will look a little bit different than you are used to, so please read ahead. You will need to ensure you are logging in to Globus via your University of Otago login.

Go to [app.globus.org](https://app.globus.org/) and search for "University of Otago" in the "Use your existing organizational login" section of the page. This will redirect you to a University of Otago login page. Please sign in with your Otago username and password.


<figure markdown="span" style="display: block; margin-left: 0; margin-right: auto;">
  ![Globus Login](../../assets/images/globus_login.png){ width="800" }
  <figcaption>Choose "University of Otago" from the organisation drop down.</figcaption>
</figure>

!!! note
    You may be prompted to link any existing Globus identities. Do this if you want to link your GlobusID account with your Otago account.


### Once you are logged in

1. Select the File Manager tab on the left side of the page, and search for "University of Otago - RTIS" in the Collection search box.
1. Use the RTIS endpoint to connect to Research Storage AND HCS.
1. Navigate to /fs in the path to find the RTIS-Storage and HCS collections (see image below). Note: The **University of Otago - HCS endpoint** is for off-campus transfers and should not be used for transfers between Ohau and HCS.
1. Click on the collection to connect to it, one on each side of the File Manager.
1. Select the directories or files you want to transfer, then click the Start arrow to begin the transfer in your desired direction.


<figure markdown="span" style="display: block; margin-left: 0; margin-right: auto;">
  ![Select "University of Otago" as the Collection ](../../assets/images/globus_rtis.png){ width="800" }
  <figcaption></figcaption>
</figure>


You should then see the RTIS-Storage collection as well as the HCS-Storage collection (with dtn_<username>). Click on the collection to connect to it, one on each side of the File Manager.

!!! warning
    <span style="font-size: 1.1em;">To transfer between HCS and Ohau -- both sides of the transfer must be set to **University of Otago - RTIS** </span>

<figure markdown="span" style="display: block; margin-left: 0; margin-right: auto;">
  ![Globus Login](../../assets/images/globus_collections.png){ width="800" }
  <figcaption></figcaption>
</figure>


Table: Mapping of key locations between Aoraki and Globus (University of Otago - RTIS endpoint)

| Directory| Aoraki Path | Globus Path |
|---|---|---|
| Home |/home/<account_name\> (~/) | /home-dtn/<account_name\> (~/) |
| Projects | /projects/ | /fs/RTIS-Storage/RTIS-Projects |
| HCS |/mnt/auto-hcs/<hcs sharename\> | /fs/HCS-Storage/<dtn-sharename\> |


!!! info
    The dtn-sharename may or may not match exactly to the hcs sharename but should be interpretable.

You can now transfer files between the two collections by selecting the directories or files you want to transfer and clicking the Start arrow pointing in the direction of your desired transfer.


<figure markdown="span" style="display: block; margin-left: 0; margin-right: auto;">
  ![Globus Login](../../assets/images/globus_transfer.png){ width="800" }
  <figcaption></figcaption>
</figure>


If you have any issues with Globus, please contact us at {{support_email}}.


### Transferring Data between Research Storage and your Desktop


The RTIS Globus endpoint works with [Globus Connect Personal](https://www.globus.org/globus-connect-personal) and will transfer data to and from your desktop or lab computer.

*Note - the **HCS endpoint** does not work with Globus Connect Personal on campus, but does allow you to share and receive data from other Globus users off campus*

To transfer data between your desktop and Research Storage, you will need to install the Globus Connect Personal application on your desktop. Follow the instructions on the [Globus Connect Personal](https://www.globus.org/globus-connect-personal) page to install it.

Once you have installed Globus Connect Personal, you can connect your desktop endpoint to the RTIS Globus endpoint and transfer data between your desktop and Research Storage.

!!! related-pages "What's next?"
    -  To transfer data between your desktop and Research Storage go to [Globus Connect Personal](https://www.globus.org/globus-connect-personal)
    - For software available on the cluster go to [Software](../../getting_started/software/applications/index.md)
    - Connect to the cluster and view your files [Connect to the Cluster](../../getting_started/access/access_overview.md)
    -  For how to run a job on the cluster go to [Running Jobs](../../getting_started/running/running_jobs_overview.md)
  
  
  
  
  
  <!-- TODO Are these pages the next step or relevant? -->
