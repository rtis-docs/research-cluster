# SAS Studio

The eResearch Solutions SAS Studio server is available at
[https://rtis-sas.uod.otago.ac.nz](https://rtis-sas.uod.otago.ac.nz)

Log in using your University credentials to access the SAS Studio IDE.

## Accessing HCS shares from within SAS Studio


To access files on any of your HCS shares: Create a New > Folder Shortcut to the Directory: `/mnt/auto-hcs/<name of the HCS share>`. 

<!-- <img width="16" alt="New Icon" src="/assets/images/NewStarburst.png"> -->



In the New Folder Shortcut dialog, enter the full path manually as above; Don't use the Browse button to browse to this location, as it won't exist yet on the server. When this shortcut is accessed, it will automatically attempt to mount the HCS share.

For `storage.hcs-chc` (Christchurch) or `storage.hcs-wlg` (Wellington) shares, use `/mnt/auto-hcs-chc/<name of the HCS share>` and `/mnt/auto-hcs-wlg/<name of the HCS share>` respectively instead.

