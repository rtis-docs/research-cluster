## ShinyProxy - R Shiny app and containerised application hosting


### Shiny app hosting

eResearch Solutions manages a ShinyProxy platform; [ShinyProxy](https://www.shinyproxy.io/) is a free & open source project that allows for the deployment of data science apps on demand, such as (but not limited to) R Shiny apps at scale, without the restrictions of e.g. the free-tier Posit/Shiny Server.

* single sign-on authentication using UO credentials, or general public access
* granular access controls (i.e. which group of users can start which apps)
* no artificial limits on concurrent usage
* highly-available and scalable, as app instances are run on one of the [eResearch Kubernetes clusters](../cloudnative/index.md).

Email {{ support_email }} if you have an R Shiny app that you would like to make available.

!!! note

    ShinyProxy can also be used to host other data science apps such as Dash, Streamlit, etc., as well as other containerised, interactive applications that need to be started on demand -web apps, Jupyter notebooks, but also native Linux desktop apps, (some) Windows applications, or even entire lightweight Linux desktop environments-.
    This may also make it an ideal platform to host a controlled, ephemeral environment for use in teaching, workshops or training.
    
    For research workloads, see [eResearch HPC Cluster](../../index.md)`.


### Shiny app development

ShinyProxy expects Shiny apps to be packaged (containerised) a certain way. App developers can provide us with the Shiny app code and we can take care of the deployment, or alternatively we can assist you in setting up a code repository and/or deployment pipeline suitable for deploying your app to ShinyProxy. 

If needed, the eResearch Software Engineering team can [assist](../../general/support.md)  you with the actual app development.



