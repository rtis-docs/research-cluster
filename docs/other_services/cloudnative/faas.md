# Function-as-a-Service (FaaS)

**Serverless computing** is a cloud-based paradigm that enables developers to write code without worrying about infrastructure management, thereby reducing barriers and potentially increasing efficiency and scalability. The most common serverless paradigm, Function-as-a-Service (FaaS), popularized by Amazon Lambda, Google Functions, and Azure Functions, allows users to register programming functions with a cloud service and then invoke those functions with arbitrary input arguments. The cloud provider transparently provisions the virtual infrastructure (typically a container), executes the function, and returns results.

## Globus Compute

[Globus Compute](https://www.globus.org/compute) (formerly funcX) implements a unique federated FaaS model that is primarily aimed at scientific computing scenarios. Unlike cloud FaaS platforms, Globus Compute’s federated model is based on a hybrid architecture with **endpoints on arbitrary remote compute resources**. These endpoints are responsible for managing the local computing infrastructure, including provisioning resources via different interfaces (e.g. batch schedulers such as Slurm, Kubernetes, or local processes).

Task execution is similar to other FaaS platforms.
 
 - First, users register **Python functions** with a Globus Compute endpoint by passing a serialized function body. 
 - Globus Compute service stores the serialized function body in the database and assigns a unique UUID for subsequent use. 
 - Users may then invoke the function by supplying the function UUID, target endpoint UUID, and optionally any input arguments.

### Research Cluster endpoint

Currently in testing
