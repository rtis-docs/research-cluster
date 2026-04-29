# September 2025 Maintenance

## Maintenance Completed: September 5–8, 2025


The scheduled maintenance on the Aoraki Research Cluster and associated services, which ran from **5:00pm Friday, 5 September – 7:00am Monday, 8 September 2025 (NZST)**, is now complete.

All cluster services, including OnDemand and CryoSPARC, are fully operational and the login node has been re-enabled.

## Planned Work Completed


The following system upgrades and changes were successfully performed during the maintenance window:

* **Enabled SLURM QOS (Quality of Service)** SLURM QOS levels are now introduced to support differentiated scheduling policies, job prioritization, and fair-share configurations.

* **Installed Powerscale Isilon multipath drivers** Multipath support for Isilon volumes is now enabled, improving fault tolerance and performance for storage connections.

* **Set SLURM temporary directory on Weka** SLURM job temporary storage has been redirected to a high-performance Weka filesystem location for better I/O performance.

* **Installed and Enabled DCGMI**
  NVIDIA Data Center GPU Manager (DCGMI) is now installed and operational. This suite of tools provides real-time health, power, performance, and utilization metrics for NVIDIA GPUs, helping administrators optimize GPU workloads and ensure system reliability.

* **Enabled SLURM Performance Statistics** SLURM Performance Statistics (SPS) is now active. This plugin collects and reports detailed job and system performance metrics, such as CPU, memory, and GPU usage, enabling advanced monitoring and accounting for optimizing workload efficiency and system utilization.

* **Set /opt/weka as a bind mount (formerly a symlink)** The change to use a proper bind mount for `/opt/weka` has been implemented for improved stability.

* **Restarted the login node to apply configuration changes** The login node was successfully rebooted to apply all system-level changes and complete the maintenance.
