# Reasonable Usage

TODO


Remember the Aoraki cluster is a shared resource and as such the following guidelines will help ensure resources are available to everyone

- Try to limit how many jobs you have in the queue and any given time, we suggest less than 1000
    - Limit how many array jobs are running simultaneously by using `%N` with your `--array` parameter, e.g. `--array=1-500%20` to limit to 20 simultaneous jobs   