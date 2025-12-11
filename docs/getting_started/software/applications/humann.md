# HUMAnN 3.0

While the requirements for the HUMAnN pipeline (MetaPhlAn etc.) could be satisfied using individual spack package loads, an Apptainer container packaging all required tools is available as a convenient alternative.

To enter an interactive shell in the container (with your home directory automatically mounted):

!!! terminal 
    
    ```bash
    humann3.sif /bin/bash
    humann_test
    ```

For usage, refer the tutorials at https://github.com/biobakery/biobakery/wiki/humann