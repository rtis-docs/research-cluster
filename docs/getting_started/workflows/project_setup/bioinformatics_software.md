## General Bioinformatics Tools
TODO convert to markdown

The following categories of bioinformatics tools are available through conda:

* Read aligners (e.g., bwa, bowtie2)
* Variant callers (e.g., freebayes, gatk, bcftools) 
* File format tools (e.g., samtools, vcftools)
* GWAS tools (e.g., plink, gemma)
* Visualization (e.g., igv, multiqc)
* RNA-seq / transcriptomics (e.g., kallisto, salmon)
* Assemblers (e.g., spades, megahit)

Finding Bioinformatics Tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  There are several ways to find bioinformatics tools in conda:

  1. Search online (recommended for discovery)
     * Use the Anaconda package search or browse specific channels:
       * Bioconda: https://anaconda.org/bioconda
       * Conda-Forge: https://anaconda.org/conda-forge
     * You can search for tools like:
       * plink
       * bcftools
       * samtools

  2. Command-line search
     From your terminal:

     .. code-block:: bash

         # Search all channels (if configured)
         conda search <package-name>

         # Example:
         conda search plink

         # If using Mamba (faster alternative to conda)
         mamba search plink

     To restrict search to a specific channel:

     .. code-block:: bash

         conda search -c bioconda plink

  3. Get full list (advanced)
     You can list everything in a channel, but it's very large:

     .. code-block:: bash

         # List all bioconda packages
         conda search --channel bioconda "*" | less

     Tip: pipe it through grep to find specific tools:

     .. code-block:: bash

         conda search -c bioconda "*" | grep vcftools