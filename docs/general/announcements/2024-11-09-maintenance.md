# November 2024 Maintenance

## Aoraki Research Cluster November 2024 Maintenance Complete


The scheduled maintenance for the Aoraki Research Cluster was successfully completed on November 10, 2024. This upgrade includes several significant improvements aimed at enhancing performance, reliability, and resource management for all users.

### Key Enhancements:


### Fairshare Scheduling with SLURM Accounting

SLURM Accounting is now enabled to monitor resource usage effectively, supporting fairshare scheduling for a balanced distribution of workloads.


### Enhanced SLURM Clustered Database and Secondary Controller

A new SLURM clustered database and secondary controller have been implemented to improve resource management and redundancy. This addition strengthens failover capabilities, ensuring uninterrupted SLURM operations in the event of a single-point failure.


### GPU Visibility with Cgroups Device Constraints

Cgroups device constraints have been added to GPU nodes, allowing users to access only the GPUs they have requested. This change minimizes conflicts and promotes fair GPU sharing across workloads.



### AUKS SLURM Plugin for Kerberos Authentication
The AUKS SLURM plugin has been integrated, enabling jobs to access Kerberos-protected network resources for up to 7 days without user intervention, simplifying authentication needs during job execution.


#### 9-10 November 2024 - Aoraki Research Cluster Maintenance Updates


As part of the scheduled maintenance for the Aoraki Research Cluster over the weekend of 9-10 November 2024, we will be implementing several updates to enhance system performance, resource allocation, and overall reliability. Below are the key changes that will be applied during this outage:

1. **Implementation of New SLURM Clustered Database and Secondary Controller**
      - To improve resource management and increase redundancy, we will be introducing a new SLURM clustered database along with a secondary controller. This upgrade is critical to ensure better failover capabilities and maintain SLURM operations in the event of any single-point failure.
2. **Enabling SLURM Accounting for Fairshare Scheduling**
      - SLURM Accounting will be enabled to track resource usage and ensure that fairshare scheduling is properly implemented. This will help balance workload distribution across users, giving fair access to cluster resources based on usage history.
3. **CPU Reservation for Weka (Recommended for 100G)**
      - Each node will now have 2 CPUs reserved specifically for Weka filesystem network services. This is in line with the recommended configuration for 100G networking and will help to optimize I/O performance and system responsiveness, particularly for jobs involving large data.
4. **Cgroup Device Constraints for GPU Visibility**
      - Cgroup device constraints will be added to all GPU nodes. This change is essential for improving GPU allocation and visibility, ensuring that users can only see and use the GPUs they have specifically requested. Currently, users can see or attempt to use all GPUs on a node, even if those GPUs are allocated to other jobs. This update will prevent such conflicts and ensure fair resource sharing.
5. **Implementing GPU Sharding on L40 Nodes**
      - To further optimize GPU resource management, we will be introducing GPU sharding on the L40 nodes. This will allow better partitioning of GPU resources, giving users more flexibility and control over their workloads while minimizing GPU contention between jobs.
6. **Implementing AUKS SLURM Plugin**
      - The AUKS SLURM plugin extends the Kerberos authentication system in HPC environments. By integrating AUKS with SLURM, jobs can access network resources (HCS) that require Kerberos authentication without user intervention during job execution. After the initial user's Kerberos ticket is obtained on the login node and added to the SLURM AUKS repository, network resources are accessible on all cluster nodes for 7 days.

!!! related-pages "What's next?"
    - [Slurm Overview](../../getting_started/running/slurm_quickstart.md)
    - [Weka](../../storage/data_locations/weka.md)

  <!-- TODO Are these pages the next step or relevant? -->
  <!-- I'm unsure if there are other pages that are relevant to the content-->