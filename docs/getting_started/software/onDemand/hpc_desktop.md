# OnDemand HPC Desktop
!!! overview "On this Page"
    - 
 
<!-- TODO Overview unclear -->
**SMB Local Mount from HPC Desktop GUI**  
<!-- TODO what does SMB stand for?-->
  1. Start an Otago HPC Desktop 
  2. Open a Terminal window on the desktop
  3. Type "kdestroy" to remove invalid older tickets
  4. Type "kinit" and Enter your password 
  5. Open File browser window  
  6. Connect and login to HCS by entering the smb://username@storage.hcs-p01.otago.ac.nz/share-name address  
  7. When the authentication window appears type in the domain "registry" if staff or "student" if you are using a student account, and your password  
  8. Press connect and wait a few seconds for authentication and your HCS files to appear in the window.  

![Connecting to HCS - create kerberos ticket with `kinit`](/assets/images/kinit.png){width="600px"}






![Connect to HCS - authenticating using samba in the file browser](/assets/images/smbauth.png){width="600px"}





![Connect to HCS - browsing hcs files in file browser](/assets/images/files.png){width="600px"}

!!! related-pages "What's next?"
      - For more information about on Demand see [Open OnDemand](../onDemand/ondemand.md)
      - Looking for something else? See [Software Overview page](../software_overview.md)
      -  For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
      
  <!-- TODO Are these pages the next step or relevant? -->