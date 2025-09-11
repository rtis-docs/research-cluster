<!-- FIXME convert from rst to md -->

CRYSTAL23 
----------

Overview
^^^^^^^^
This guide describes how to run **CRYSTAL23 v1.0.1** on the cluster using Slurm.
The installation is built with **ifort 2021.4**, **Open MPI 4.1.6** (TCP over Ethernet),
and **Intel oneMKL 2024.2**, exposed via the module ``crystal/23.1.0.1``.

.. important::

   This Open MPI build is **not Slurm-PMI enabled**. Use ``mpirun`` to launch MPI ranks.
   You can still use ``srun``/**salloc** to obtain an allocation or an interactive shell,
   then invoke ``mpirun`` inside that allocation.

Environment
^^^^^^^^^^
Load the CRYSTAL23 module before running:

.. code-block:: bash

   module load crystal/23.1.0.1
   which Pcrystal   # -> /opt/crystal/23/1.0.1/bin/Pcrystal

The module also sets Open MPI to use **TCP over Ethernet** by default
(``OMPI_MCA_btl=self,tcp`` and ``OMPI_MCA_oob=tcp``), so you do not need to add
InfiniBand-related flags.

Input/Output Conventions
^^^^^^^^^^^^^^^^^^^^^^^^
* CRYSTAL reads its input deck from **stdin** and writes results to **stdout**.
* Always use shell redirection:

  .. code-block:: bash

     mpirun -np <RANKS> Pcrystal < INPUT > OUTPUT

* Keep OpenMP threads to one (MPI-first code):

  .. code-block:: bash

     export OMP_NUM_THREADS=1

Interactive Runs (via srun allocation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Obtain a node allocation with ``srun --pty`` (or ``salloc``), then call ``mpirun``:

.. code-block:: bash

   # 1 node, 8 MPI ranks example (edit partition/time as needed)
   srun --pty -N 1 --ntasks-per-node=8 -t 00:30:00 -p <partition> bash -l

   # inside the interactive shell:
   module load crystal/23.1.0.1
   export OMP_NUM_THREADS=1

   # CPU binding and mapping: adjust to your node size
   mpirun --bind-to core --map-by ppr:8:node -np 8 \
          Pcrystal < INPUT > OUTPUT

Batch Runs (sbatch)
^^^^^^^^^^^^^^^^^^^
Save the following to ``crystal23.sbatch`` and submit with ``sbatch crystal23.sbatch``.

.. code-block:: bash

   #!/bin/bash
   #SBATCH -J crystal23
   #SBATCH --ntasks-per-node=16        # MPI ranks per node (edit)
   #SBATCH -t 02:00:00                 # wall time (edit)
   #SBATCH -p <partition>              # partition/queue (edit)
   #SBATCH -o crystal23.%j.out
   #SBATCH -e crystal23.%j.err

   set -euo pipefail

   module load crystal/23.1.0.1
   export OMP_NUM_THREADS=1

   # Work in the submission directory
   cd "${SLURM_SUBMIT_DIR:-$PWD}"

   # Check input deck is present
   test -s INPUT || { echo "Missing INPUT deck"; exit 2; }

   # Launch ranks with mpirun (Open MPI not built with Slurm PMI)
   mpirun --bind-to core --map-by ppr:${SLURM_NTASKS_PER_NODE}:node \
          -np ${SLURM_NTASKS} Pcrystal < INPUT > OUTPUT

   echo "CRYSTAL23 finished. See OUTPUT and slurm logs."

Resource Selection & Binding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Choose ranks-per-node (``--ntasks-per-node``) to match physical cores you want to use.
* Use ``--bind-to core`` and a sensible mapping (e.g., ``ppr:<ranks-per-node>:node``) for
  predictable performance.
* Keep ``OMP_NUM_THREADS=1`` unless you explicitly want hybrid MPI+OpenMP.

Troubleshooting
^^^^^^^^^^^^^^^
**“END OF DATA IN INPUT DECK” and MPI_ABORT**  
You ran without a valid stdin redirection or your ``INPUT`` file is empty/malformed.
Run as: ``mpirun -np N Pcrystal < INPUT > OUTPUT``.

**OpenFabrics / openib warnings**  
Harmless on Ethernet-only systems. The module already forces TCP transports.

**Attempting to start ranks with srun**  
This build isn’t Slurm-PMI enabled. Use ``srun``/**salloc** to get the allocation,
then launch with ``mpirun`` inside that allocation.

Provenance
^^^^^^^^^^
* CRYSTAL23 v1.0.1 (``Pcrystal``)
* ifort 2021.4, Open MPI 4.1.6 (TCP), Intel oneMKL 2024.2
* Module: ``crystal/23.1.0.1``