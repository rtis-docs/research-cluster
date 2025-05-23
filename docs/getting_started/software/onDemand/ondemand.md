# Open OnDemand 



Open OnDemand launches applications as scheduled Slurm jobs on your behalf when requested, right in your browser without installing any software. This load balances your job across a cluster of computers and allows for shared access with users. 
Open OnDemand refers to these jobs as "interactive sessions." You can also access your files, view past jobs, and get shell access.


Slurm "Job time" is counted for interactive sessions as the total time the job runs. The job starts running as soon as a node is allocated for the job. The interactive session may still be running even if you do not have it open in your web browser. You can view all currently running interactive sessions under My Interactive Sessions. When you are done, you may stop an interactive session by clicking "Delete" on the session.

**There are several ways to monitor usage:**

- Since Open OnDemand submits jobs through Slurm, you can monitor usage as you would monitor your regular Slurm jobs.
- View currently running (and recent) sessions launched by Open OnDemand under My Interactive Sessions.
- View all currently running jobs under Jobs > Active Jobs.

## Using Open OnDemand

Here are the services provided via Open OnDemand.


### Files App

Access the Files App from the top menu bar under Files > Home Directory. Using the Files App, you can use your web browser to:

Create and delete files and directories.
(need to add section on HCS and Globus)
After you login you should see the OOD home page. 

![Open OnDemand Files App](/assets/images/ood_files_app.png){width="600px"}

### View Active Jobs


View and cancel active Slurm jobs from Jobs > Active Jobs. This includes jobs started via sbatch and srun as well as jobs started (implicitly) via Open OnDemand (as discussed above).

![Active Jobs](/assets/images/ood_activejobs.png){width="600px"}



### Shell Access

Open OnDemand allows Aoraki shell access from the top menu bar under Clusters > Aoraki Cluster Shell Access.

![Open OnDemand Shell](/assets/images/ood_shell.png){width="600px"}


### Interactive Apps

Open OnDemand provides additional interactive apps. You can launch interactive apps from the Interactive Apps menu on the top menu bar. The available interactive apps include:

Desktop App (for working with GUI-based programs)
Jupyter Server (for working with Jupyter notebooks)
RStudio Server (for working in RStudio sessions)

![Open OnDemand Files App](/assets/images/ood_interactive.png){width="600px"}


### Desktop App

The OOD Desktop App allows you to run programs that require graphical user interfaces (GUIs) on the Research Cluster

Intended Usage

When possible, you should carry out your computation via the traditional command line plus SLURM functionality. OOD Desktop is intended for use for programs that require GUIs. Furthermore, if you need to use Jupyter notebooks, RStudio, or the MATLAB GUI, we provide specialized interactive apps that you should use instead of the OOD Desktop App.

Before getting started, make sure you have access to the Research Cluster (by contacting RTIS).

Fill out the form presented to you and then press "Launch". (Note, as of this time, that the only partition that the Desktop app can be launched on when computing via Slurm is otago1, as we assume that most GUI usage would be for programs using one or a small number of cores). After a moment, the Desktop session will be initialized and allow you to specify the image compression and quality options. If you are unhappy with the default values, you can relaunch the session from this page with different choices. Then, press "Launch Desktop" and the Desktop will open in a new tab.


### Interacting with Files

Your Desktop session is running directly on the Research Cluster, and can interact with your files either through the command line as usual or through Desktop the file manager.


To open a command line terminal, right click anywhere on the Desktop and select "Open Terminal Here".


#### Using Otago HCS Data

1. Connect to the HCS Share
2. Copy your data to your projects directory
3. Process your data with the cluster
4. Copy your results back to the HCS Share 

Note: Connecting to Otago HCS is intended for copying data to the Research Clutster for processing. **It is not intended for data processing** as the speeds and accessibility are not suited to cluster computing.


#### Connecting to Otago HCS Shares


**AutoFS from the commandline**  

This will mount your HCS share on the local machine and allow you to access and sync files. Note that this is not high-speed access and handling large files may be slow. 

  1. Take note of your HCS share directory name, the part after `//storage.hcs-p01.otago.ac.nz/ **<yourshare>** `   
  2. Login to a commandline shell session 
  3. Type "kdestroy" to remove invalid older tickets
  4. Type "kinit" and Enter your password  
  5. List or navigate to yoru directory `/mnt/auto-hcs/*<yourshare>* ` 
  6. sync your files to your projects directory eg. `rsync -avz /mnt/auto-hcs/its-rtis/testfile /projects/rtis/higje06p/`  
  7. use your files to process on the compute cluster   






#### Copy your HCS data to your project directory

1\. Naviagate to your hcs data and copy it to your user projecy directory

![Connect to HCS](/assets/images/copydata.png){width="600px}


2\. When you have finished processing copy your data back to your HCS Share.








