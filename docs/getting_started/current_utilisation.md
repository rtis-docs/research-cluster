# Current Utilisation

!!! overview "On this Page"
    - How much of the cluster's CPU capacity is allocated, over the last week
    - How hard each GPU node has been working, node by node
    - Where to look instead if you want queue waiting times and what is free right now

This page shows current resource utilisation across the Otago Aoraki Cluster.

!!! note

    This data is only visible if you are on the University of Otago network or connected via VPN.

If what you actually want to know is *how long will my job wait* or *what is free right now*,
[Queue and Availability](queue_and_availability.md) answers those directly. This page is the
raw hardware view.

## CPU Allocation Over the Last 7 Days

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="CPU allocation across the cluster over the last 7 days" src="https://research-monitoring.otago.ac.nz/d-solo/bX7jn6dZk/slurm-dashboard?orgId=1&from=now-7d&to=now&refresh=30s&theme=light&panelId=10&hideLogo=true"></iframe>

## GPU Utilisation Over the Last 7 Days

These graphs show how hard each GPU has been *working*, which is not the same as whether it
was **allocated**. A GPU held by a job that is loading data or waiting on the filesystem sits
near zero here while still being unavailable to everyone else. For allocation, see
[Queue and Availability](queue_and_availability.md).

### aoraki11 — 2x A100 80GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki11" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r11.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki12 — 2x A100 80GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki12" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r12.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki16 — 4x H100 80GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki16" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r16.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki30 — 4x H100 96GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki30" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r30.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki18 — 3x L40 48GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki18" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r18.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki19 — 3x L40 48GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki19" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r19.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki27 — 2x A100 40GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki27" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r27.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki28 — 2x A100 40GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki28" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r28.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki29 — 7x L4 24GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki29" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r29.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki44 — 8x H200 144GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki44" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r44.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki45 — 8x RTX6000 98GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki45" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r45.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

### aoraki46 — 8x RTX6000 98GB

<iframe class="grafana-panel grafana-panel--compact" loading="lazy" title="GPU utilisation on aoraki46" src="https://research-monitoring.otago.ac.nz/d-solo/Oxed_c6Wz/nvidia-dcgm-exporter?orgId=1&var-instance=rtis-hpc-r46.uod.otago.ac.nz%3A9400&var-gpu=All&from=now-7d&to=now&refresh=30s&theme=light&panelId=6&hideLogo=true"></iframe>

!!! related-pages "What's next?"
    - [Queue and Availability](queue_and_availability.md) for waiting times and what is free
    - [Running Jobs Overview](running/running_jobs_overview.md)
    - [Writing Slurm Job Scripts](running/batch/slurm_quickstart.md)
    - [Job Efficiency](running/efficiency.md)
