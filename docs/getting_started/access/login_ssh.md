# Accessing the login node (ssh)
<!-- TODO See if overview is in line with content -->
!!! overview "On this Page"
    - How to Access the login node for 'lightweight' tasks
    - How to SSH through a terminal
    - How to SSH with OnDemand

Use of the login node should be limited to 'lightweight' tasks such as file browsing/copying/moving or submitting jobs into the SLURM scheduler.

You can access the Research Cluster login node remotely through the two below mechanisms.

## SSH through a terminal

To SSH to the login node from your local computer, first open a terminal/commandline and then use the `ssh` command with username being your Otago username and the address for the remote computer being `aoraki-login.otago.ac.nz` which will look like this: `ssh lasfi12p@aoraki-login.otago.ac.nz`

!!! terminal

    === "Staff Network"

        ```bash
        ssh <otago-username>@aoraki-login.otago.ac.nz
        ```

        ```output
        <otago-username>@aoraki-login.otago.ac.nz's password:
        ```

    === "Student Wifi/VPN"

        ```bash
        ssh <otago-username>@aoraki-login-stu.uod.otago.ac.nz
        ```

        ```output
        <otago-username>@aoraki-login-stu.uod.otago.ac.nz's password:
        ```
    !!! info

        If you are using **Student Wi-Fi or VPN**, you will need to use the alternate address **aoraki-login-stu**: ``ssh <otago-username>@aoraki-login-stu.uod.otago.ac.nz``


!!! info "First time connecting"

    The first time you `ssh` from a computer you will likely see output extremely similar to:
    
    !!! terminal
        ```output
        The authenticity of host 'aoraki-login.otago.ac.nz (X.X.X.X)' can't be established.
        ED25519 key fingerprint is SHA256:WXAGQmlR5C7rvCOiSSL8PtiuxytA368rjozXXO0NckE.
        This key is not known by any other names.
        Are you sure you want to continue connecting (yes/no/[fingerprint])?
        ```

        !!! Warning

            Double check the fingerprint matches one of the following:
            ```
            (RSA) SHA256:pzUx1abRS35sbM9n/3OqMpGiF9zegvlG4jQrr78cGFg
            (ECDSA) SHA256:g/BKtsqcMchX7l7YRqDJ98azAumTxzQT0hCCCgVIKxc
            (ED25519) SHA256:WXAGQmlR5C7rvCOiSSL8PtiuxytA368rjozXXO0NckE
            ```

    Type 'yes' and <kbd>Enter</kbd>, where you will then be prompted for your password (or need to re-`ssh`) depending on your `ssh` client.



!!! warning "Password not showing"

    When typing in your password when prompted there will be nothing outputed on the screen. Once you have typed your password press <kbd>Enter</kbd> to submit and continue. If you mistyped your password you will be prompted to re-enter it.

## SSH within OnDemand

To use the cluster shell access within OnDemand, first [connect to the **Otago OnDemand** web portal](/getting_started/access/ondemand_web#logging-in) and then from the top menu bar select the menu `Clusters` > `Aoraki Cluster Shell Access`.

You will then be prompted to input your password, similar to [SSH through the terminal](#ssh-through-a-terminal)

![Open OnDemand Shell](/assets/images/ood_shell.png){width="600px"}

<!-- TODO update screenshot -->


!!! related-pages "What's next?"
    Where to store your data and what your options are found on our [Storage Overview](../../storage/storage_options.md)
  <!-- TODO Are these pages the next step or relevant? -->

