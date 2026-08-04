---
tags:
  - OnDemand
---

# Available Apps

!!! overview "On this Page"
    - Which applications you can launch from OnDemand
    - How to launch one
    - Which applications are only on the legacy portal

These are the applications you can launch from the **Interactive Apps** menu in [Open OnDemand](ondemand.md). Each one runs as a Slurm job on a compute node — you fill in a short form for cores, memory, wall time and any app-specific options, press **Launch**, then click **Connect** when the job starts.

If the software you need is not listed here, you may still be able to run it on the [HPC Desktop](hpc_desktop.md), or install it yourself — see the [Software Overview](../index.md) and the [list of installed software](../applications/index.md).

## List of Available Apps

<!-- TODO the cards in child/ood_apps/ are incomplete. Per the 2026-04-29 upgrade
     announcement the portal also offers: AFNI, AnimalTA, CCP4, DeepLabCut, MATLAB,
     phy, WhisperX UI and XDSGUI. Cards for these need adding to child/ood_apps/.
     The legacy list below is likewise missing: Connectome Workbench, FSL,
     GLOBEClaritas, Open WebUI - Ollama, CCP4 and XDSGUI. -->

{% include  "child/ood_apps/*" %}

## Legacy Apps

!!! info
    Some applications have not yet moved to the current portal. They remain available on the legacy instance at [https://ondemand-legacy.otago.ac.nz](https://ondemand-legacy.otago.ac.nz), which you log in to the same way.

{% include  "child/ood_apps_legacy/*" %}

!!! related-pages "What's next?"
      - Unsure how to get into the portal? See the [Open OnDemand Overview](ondemand.md)
      - For graphical software without its own app, see the [HPC Desktop](hpc_desktop.md)
      - Looking for something else? See the [Software Overview](../index.md)
      - For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
