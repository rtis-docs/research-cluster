# CryoSPARC 


All new users must register with Research Computing before accessing CryoSPARC.

**Sign up here**:  
[Research Computing Signup](https://rtis.cspages.otago.ac.nz/research-computing/cluster/index.html)

Once you have completed the form, please email us at **rtis.solutions@otago.ac.nz** so we can create a CryoSPARC account for you and send your login token.

If you plan to share files with a research group or if your work is private, let us know so we can set up an appropriate project folder for you.

## Accessing CryoSPARC


Most jobs can be submitted via the browser interface:  
CryoSPARC web login: [https://cryosparc-01.otago.ac.nz/](https://cryosparc-01.otago.ac.nz/)

This dashboard allows you to monitor job activity and see which lanes are in use.

CryoSPARC has two compute lanes:

- **Default**  
  This lane load-balances jobs between `gpu-07` and `gpu-08`.  
  Working on a specific node does not provide improved performance or priority.

  If you manage files or jobs via SSH, we recommend using `gpu-08`, which is the master node.

- **Aoraki (cluster)**  
  This lane submits jobs to the cluster’s high-performance GPU nodes.  
  These GPUs are more powerful and can speed up job finalization.  
  However, they may be in high demand due to usage by other users and applications.

  View current usage here:  
  [https://rtis.cspages.otago.ac.nz/research-computing/cluster/usage.html](https://rtis.cspages.otago.ac.nz/research-computing/cluster/usage.html)
