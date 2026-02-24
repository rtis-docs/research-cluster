
!!! overview "On this Page"
     - What is the Projects data storage area
     - When to use the Projects area
  <!-- TODO Overview unclear -->


Projects storage is allocated and organised per department and group ``/projects/<division>/<department>/<Research_Group>``. The principle investigator for the group is responsible for the data contained within the project directory.

Project quotas are set upon initial set-up and can be revised upon request.

The projects storage is high-performance and is ideal for temporarily storing data that is **in use** for individuals and sharing within groups using the research infrastructure.

We recommend having a copy of your source data on HCS, and transferring a copy to `/projects/` for working on, then removing this working copy once finished and transferring results back to HCS.
 
To apply for a projects directory, please fill out the [storage-signup-form](../getting_started/access/signup.md) form.
 
 
## When to use /projects/ storage
 
Intermediate Data Storage: 
  
  - During complex computations, intermediate data or temporary results are often generated.

Checkpointing:
  
  - In long-running computations, checkpointing is used to save the state of a job at regular intervals.

Data Staging: 
  
  - Before running a job, input data can be staged (preloaded) into `/projects/` from HCS (or other sources) to ensure that the computation starts immediately without waiting for data transfers from slower storage systems.

Temporary Data Processing: 
  
  - For tasks that generate large amounts of temporary data, such as sorting, indexing, or image processing.
 
!!! warning
 
    Note that the **Research storage is not backed up** and it is the responsibility of the user to ensure their important data is safe. See [data transfer](../getting_started/data_transfer/data_transfer_overview.md) for options to move data you want to retain. If you need assistance with backing up your data, please email {{support_email}}.
 



!!! related-pages "What's next?"
    - To see where Projects fits within Storage check out [Storage Overview](../storage_options.md)
    - Find out how to move Data on and off the Research Cluster on [Data Transfer](../../getting_started/data_transfer/data_transfer_overview.md)
    - Your home directory
    - WEKA 
  <!-- TODO Are these pages the next step or relevant? -->
