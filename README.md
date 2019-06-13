# perfmon

If there are any questions regarding the REST API, a good place to start is the REST API explorer (accessed via Prism Element), or from browsing https://developer.nutanix.com/api-reference/. The scripts in this repo utilize v1 and v2 of the REST API.

REST API v1 docs are available at: https://portal.nutanix.com/#/page/docs/details?targetId=API-Ref-AOS-v58:API-Ref-AOS-v58

Here is a description of the files in this repo:

HOWTO.txt describes how to set up a dev environment so one can get started.

clusterconfig.py contains variables and common functions used in the code. It is a Python module. You will need to update the variables above the line in order to get the programs to work. In particular please create a separate admin user on your cluster called "restapiuser", so the real admin password is not passed around.

getvm_stats.py takes the name of a VM and spews out CPU and Memory usage percentages over a particular period of time. The period and the sampling interval are in clusterconfig.py.
