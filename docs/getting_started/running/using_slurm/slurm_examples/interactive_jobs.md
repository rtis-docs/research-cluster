# Interactive Jobs


In some instances, you may need to use software that requires user interaction
rather than running programs or scripts in batch mode. 
To do so, you must first start an instance of an interactive shell on a Otago
login node, within which you can then run your software on that node.
To run such an interactive job on a compute node, you'll use ``srun``. 
Here is a basic example that launches an interactive bash shell on that node
and includes the required account and partition options:

!!! terminal

    ```bash
    [user@aoraki-login ~]$ srun --pty --partition=aoraki --time=00:05:30 -N 1 -n 4 /bin/bash
    ```

Once your job starts, the prompt will change and indicate you are on a compute
node rather than a login node:

!!! terminal

    ```bash
    srun: job 669120 queued and waiting for resources  
    srun: job 669120 has been allocated resources  
    [user@aoraki13 ~]
    ```