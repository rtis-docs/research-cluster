---
tags:
  - OnDemand
---

# Available Apps

!!! overview "On this Page"
    - Which portal to use, and why there are two
    - Every application you can launch, what it is for, and what it needs
    - The applications that need a licence before they will start
    - What to do when the software you need has no app

These are the applications you can launch from the **Interactive Apps** menu in
[Open OnDemand](ondemand.md). Each runs as a Slurm job on a compute node: you fill in a short
form for cores, memory, wall time and any options specific to that app, press **Launch**, then
click **Connect** once the job starts.

Because it is a normal Slurm job it has to queue, and it holds the resources you asked for
until you delete the session or the wall time runs out. [Open OnDemand Overview](ondemand.md)
covers how that works and the limits that apply to OnDemand jobs.

## Which Portal?

There are two portals, and you log in to both the same way.

Table: The two OnDemand portals

| Portal | Address | What is on it |
|---|---|---|
| **Current** | [ondemand.otago.ac.nz](https://ondemand.otago.ac.nz) | Open OnDemand 4.1, and most applications. Start here. |
| **Legacy** | [ondemand-legacy.otago.ac.nz](https://ondemand-legacy.otago.ac.nz) | Applications that have not yet moved across. |

The legacy instance exists only because a set of applications had not been ported when the
portal was upgraded in [April 2026](../../../general/announcements/2026-04-29-maintenance.md).
It is shrinking over time, so check the current portal first.

## Apps on the Current Portal

Table: Available from Interactive Apps at ondemand.otago.ac.nz

| App | What it is for | Notes |
|---|---|---|
| **[Otago HPC Desktop](hpc_desktop.md)** | A full Linux desktop on a compute node, for anything without its own app | |
| **[RStudio Server](../applications/r_rstudio.md)** | R and RStudio in the browser | |
| **JupyterLab** | Notebooks for Python, R and Julia | [Several environments](#jupyterlab) |
| **[WhisperX UI](../applications/whisper.md)** | Speech-to-text transcription and translation | Faster with a GPU |
| **[AFNI](../applications/afni.md)** | Analysis and display of functional MRI data | |
| **Blender** | 3D modelling, animation and rendering | **Needs a GPU** |
| **[DeepLabCut](../applications/deeplabcut.md)** | Markerless pose estimation from video | Faster with a GPU |
| **ESA SNAP** | Earth observation imagery, including Sentinel data | |
| **Fiji** | Scientific image analysis — an ImageJ distribution with plugins bundled | |
| **FlexPDE** | Finite element solver for partial differential equations | [Licence](#flexpde) |
| **Kilosort** | Spike sorting for multi-channel electrophysiology recordings | Faster with a GPU |
| **[MATLAB](../applications/matlab.md)** | Numerical computing and simulation | Licensed |
| **NetLogo** | Agent-based modelling of natural and social phenomena | |
| **Phenix** | Macromolecular structure determination from X-ray and cryo-EM data | |
| **phy** | Manual curation of spike sorting results | |
| **VSCodium** | Code editor in the browser — a freely-licensed build of VS Code | |
| **[XDSGUI](../applications/xdsguI.md)** | Processing and phasing X-ray, neutron and electron diffraction data | Also on legacy |

## Apps on the Legacy Portal

Table: Available from Interactive Apps at ondemand-legacy.otago.ac.nz

| App | What it is for | Notes |
|---|---|---|
| **[CCP4](../applications/ccp4.md)** | Macromolecular structure determination by X-ray crystallography | |
| **ChimeraX** | Molecular structure visualisation | **Needs a GPU** |
| **CLC Genomics Workbench** | Sequence analysis for genomics, epigenomics and metagenomics | [Licence](#clc-genomics-workbench) |
| **[Connectome Workbench](../applications/connectome_workbench.md)** | Visualising Human Connectome Project data | |
| **EcoAssist** | Classifying camera trap images | Faster with a GPU |
| **EPI2ME Desktop** | Oxford Nanopore's GUI for Nextflow bioinformatics pipelines | [Setup notes](#epi2me-desktop) |
| **[FSL](../applications/fsl.md)** | Analysis of FMRI, MRI and diffusion brain imaging data | |
| **[GLOBEClaritas](../applications/claritas.md)** | 2D and 3D land and marine seismic data processing | Licensed |
| **GRASS GIS** | Geospatial analysis, modelling and visualisation | |
| **ilastik** | Interactive image classification and segmentation using machine learning | |
| **MELTS** | Thermodynamic modelling of phase equilibria in magmatic systems | [Model versions](#melts) |
| **[Open WebUI – Ollama](../applications/ollama.md)** | Browser front end for running large language models locally | Faster with a GPU |
| **QGIS** | Desktop geographic information system | |
| **RELION** | Cryo-electron microscopy structure determination | Faster with a GPU |
| **SAGA GIS** | Geospatial analysis, with a large library of terrain and raster tools | |
| **SaTScan** | Spatial, temporal and space-time cluster detection | |
| **Specify** | Biological collections management | |
| **Stata** | Statistics, data management and econometrics | [Licence](#stata) |
| **UGENE** | Visualising, aligning, assembling and annotating DNA and protein sequences | [Launch options](#ugene) |
| **[XDSGUI](../applications/xdsguI.md)** | Processing and phasing X-ray, neutron and electron diffraction data | Also on the current portal |

## Apps That Need More Than a Launch Form

Most apps need nothing beyond filling in the form. These are the exceptions.

### JupyterLab

JupyterLab comes in a number of domain-focused and application-specific variants, selected on
the launch form. Each is a container, so the software stack is immutable — which makes your
environment consistent from one session to the next and easier to reproduce later.

The environments are based on the [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io)
images maintained by the Jupyter team. If you need a customised environment, email the
eResearch Support team at **{{ support_email }}**.

### FlexPDE

**FlexPDE Lite** is the evaluation configuration. It is free to use, but limits the number of
simultaneous equations and mesh cells.

**FlexPDE Professional** can be activated over the internet with an appropriate serial number.
Activation is machine-based, so unless you select the same node each time you will need to
deactivate and reactivate on subsequent runs.

### CLC Genomics Workbench

QIAGEN [CLC Genomics Workbench](https://digitalinsights.qiagen.com/products-overview/discovery-insights-portfolio/analysis-and-visualization/qiagen-clc-genomics-workbench/)
is a sequence analysis platform for genomics, epigenomics and metagenomics.

!!! warning "Licensed software"
    The cluster has a small number of floating licences available for trial purposes,
    facilitated by Dr Sunali Mehta (<mailto:sunali.mehta@otago.ac.nz>) in the Pathology
    department. Please make sure you are authorised before consuming a licence.

Tick the **3D hardware-accelerated rendering** option and request a GPU if you are using the
3D viewers.

### MELTS

MELTS models thermodynamic phase equilibria in magmatic systems
([melts.ofm-research.org](https://melts.ofm-research.org)). The launcher lets you pick the
version and model:

  * **rhyolite-MELTS 1.0.2** — original version with corrections. Old H<sub>2</sub>O model, no mixed fluids.
  * **rhyolite-MELTS 1.1.0** — mixed fluid version that preserves the ternary minimum. Old H<sub>2</sub>O model.
  * **rhyolite-MELTS 1.2.0** — mixed fluid version, best for mafic and alkalic melts. New H<sub>2</sub>O model.
  * **pMELTS 5.6.1** — original version with corrections. Old H<sub>2</sub>O model, no mixed fluids.

### UGENE

[UGENE](https://ugene.net) integrates dozens of well-known biological tools and algorithms for
genomics, evolutionary biology and virology. Two launch options are worth knowing about:

  * **Hardware-accelerated 3D** improves the 3D viewer.
  * **OpenCL** improves the performance of a few algorithms, including Smith-Waterman and the
    UGENE Genome Aligner.

### EPI2ME Desktop

Oxford Nanopore's [EPI2ME Desktop](https://labs.epi2me.io/about/) gives you a graphical
interface for running bioinformatics pipelines.

!!! note "Importing other workflows"
    As well as the ONT workflows prepopulated in the **Available Workflows** tab, EPI2ME
    Desktop can import generic **Nextflow** workflows, including the 100+ curated pipelines of
    [nf-core](https://nf-co.re/pipelines). Under **Workflows**, click **Import workflow** and
    paste the workflow's git repository URL — for example `https://github.com/nf-core/<wf>`.

How it behaves on the cluster:

  * Individual pipeline tasks are sent to Slurm and **scheduled as separate jobs**, with their
    own resources — taken from the workflow defaults, or from what you set in the
    **Nextflow configuration** tab.
  * For pipelines needing GPU compute there is no need to run EPI2ME itself on a GPU. The
    launch form does not offer the option; tasks that need a GPU are scheduled onto
    GPU-capable nodes automatically.
  * There is no need to change the **Profile** setting under **Nextflow configuration**. This
    instance defaults to the `singularity` profile, which uses Apptainer.

Launching the app for the first time creates a global Nextflow configuration at
`~/.nextflow/config` to make that work. If the file already exists, you may need to add the
following yourself:

!!! terminal

    ```bash
    process {
      executor = 'slurm'
      time = 6.h
      withLabel: 'gpu' {
        queue = 'aoraki_gpu'
      }
    }
    ```

!!! warning
    EPI2ME Desktop is not designed with HPC clusters in mind, so integrating it with the
    scheduler has taken a number of workarounds. Testing has been promising, but the added
    complexity — and the application's limited Nextflow configurability — *may* produce
    problems that are hard to troubleshoot.

    Consider running the workflows from the command line with
    [Nextflow](../../running/workflows/nextflow.md) instead.

### Stata

Stata will not start until a valid licence file is installed for your account. That needs
authorisation details from the University's software procurement office.

**Requesting a licence**

1. Go to [https://www.otago.ac.nz/its/services/software/stata](https://www.otago.ac.nz/its/services/software/stata).
2. Click the **Software Order Form** link.
3. Enter **Stata** in the *Product* field.
4. ITS Software Procurement will email you a PDF containing your **serial number**, **code**
   and **authorisation**.
5. Forward that PDF to the eResearch Support team at **{{ support_email }}**.

We then generate the licence file, install it for your account, and confirm when Stata is ready
to use.

If you already hold a University Stata licence you can reuse it for the cluster — just forward
the PDF. Licences are managed centrally to comply with the University's licensing terms.

## Licensed Applications

Some applications need licensing sorted out before they will run. If you are planning work
around one of these, start the licence process early:

Table: Applications with licensing requirements

| App | What is needed |
|---|---|
| **Stata** | A licence file generated for your account — see [Stata](#stata) above |
| **CLC Genomics Workbench** | Authorisation to use one of a small number of floating licences |
| **FlexPDE Professional** | A serial number, activated per node. FlexPDE Lite needs nothing, but is limited |
| **MATLAB** | Covered by the University licence |
| **GLOBEClaritas** | Covered by the University licence |

If you are unsure whether your licence covers cluster use, ask the eResearch Support team at
**{{ support_email }}** before you start.

## If the App You Need Is Not Here

Three things to try, in order:

1. **Run it on the [HPC Desktop](hpc_desktop.md).** Plenty of graphical software runs happily
   in a desktop session without needing an app of its own.
2. **Load it as a module.** Some of these applications are also available on the command line,
   including AFNI, FSL, Connectome Workbench, GLOBEClaritas, MATLAB, EPI2ME and R. Run
   `module spider <name>` to check, or see [Software Applications](../applications/index.md)
   for the full list.
3. **Ask us to install it.** See
   [How Do I Ask for Software to Be Installed?](../../../general/faq/software.md#how-do-i-ask-for-software-to-be-installed)
   for what makes that request easy to act on.

!!! related-pages "What's next?"
      - Unsure how to get into the portal? See the [Open OnDemand Overview](ondemand.md)
      - For graphical software without its own app, see the [HPC Desktop](hpc_desktop.md)
      - Looking for something else? See the [Software Overview](../index.md)
      - For how to run a job on the cluster go to [Running Jobs](../../running/running_jobs_overview.md)
