# April 2026 Maintenance

## Open OnDemand Upgrade — Wednesday 29 April 2026


!!! info
      **Scheduled Maintenance:** Wednesday 29 April, 5:00 PM – 7:00 PM

## Summary


The Open OnDemand (OOD) web portal will be upgraded from version 3.x to version 4.1 on a new dedicated host. This upgrade delivers improved page loading performance, new features, and greater stability.


## Impact


- Users will be unable to log in to the OOD portal during the upgrade window.
- **Running SLURM jobs will not be affected.** Jobs started on the current portal will remain accessible after the upgrade.
- The cluster login node and SLURM scheduler will be unaffected.

### What's Changing


Following the upgrade, the production portal at `ondemand.otago.ac.nz` will run OOD 4.1. Some applications that are not available on the new version will remain accessible on the legacy instance at [https://ondemand-legacy.otago.ac.nz](https://ondemand-legacy.otago.ac.nz).

**Apps available on OOD 4.1** ([https://ondemand.otago.ac.nz](https://ondemand.otago.ac.nz)):

- Otago HPC Desktop
- Studio Server
- JupyterLab
- AFNI
- Blender
- DeepLabCut
- ESA SNAP
- Fiji
- FlexPDE
- Kilosort
- MATLAB
- NetLogo
- Phenix
- WhisperX UI
- XDSGUI
- phy

**Apps available on legacy instance only** ([https://ondemand-legacy.otago.ac.nz](https://ondemand-legacy.otago.ac.nz)):

- CCP4
- ChimeraX
- GLOBEClaritas
- CLC Genomics Workbench
- Connectome Workbench
- EcoAssist
- EPI2ME Desktop
- FSL
- GRASS GIS
- Ilastik
- MELTS
- Open WebUI – Ollama
- QGIS
- RELION
- SAGA GIS
- SaTScan
- Specify
- Stata
- UGENE
- XDSGUI


##Questions


If you have any questions or concerns, please contact the RTIS team at {{ support_email }}.
