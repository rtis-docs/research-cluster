

# November 2024


- **SLURM Controller Daemon Upgrade**  
  Upgraded `slurmctld` daemon to version 23.02.0-json, enabling both Lua and JSON capabilities.

- **Secondary SLURM Control Node**  
  Added a secondary SLURM control node.

- **SLURM Database Migration**  
  Migrated the SLURM database to a Galera cluster.

- **Enhanced SLURM Database Backup and Monitoring**  
  Added new backup and monitoring features for the SLURM database.

- **GPU Cgroups Constraints**  
  Implemented Cgroups constraints on GPU resources to ensure fair resource distribution.

- **Weka Storage Upgrade**  
  Upgraded Weka storage to version 4.2.17.

- **Weka Container Configuration Update**  
  Configured Weka containers to use 2 CPUs on each node.

- **CPU Reservation for Weka in SLURM Configuration**  
  Updated SLURM configuration to reserve CPU resources specifically for Weka operations.

- **SLURM Accounting User and Group Import**  
  Imported all users and groups into SLURM accounting for enhanced tracking and management.

- **AUKS Installation and Configuration**  
  Installed and configured AUKS to enable Kerberos authentication across cluster nodes.

- **Node Renaming for Active Directory Compliance**  
  Renamed all nodes to comply with the Active Directory naming scheme and rejoined the domain.

- **OnDemand Reconfiguration**  
  Reconfigured OnDemand to utilise new node names.

- **L40 GPU Node Activation for OnDemand Desktop Use**  
  Enabled the L40 GPU Nodes for use in OnDemand desktop environments.

!!! related-pages "What's next?"
    - [Slurm Overview](../../getting_started/running/batch/slurm_quickstart.md)
    - [Weka](../../storage/data_locations/weka.md)

  <!-- TODO Are these pages the next step or relevant? -->
  <!-- I'm unsure if there are other pages that are relevant to the content-->
  