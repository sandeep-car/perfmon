#!/usr/local/bin/python3.7
#
# DISCLAIMER: This script is not supported by Nutanix. Please contact
# Sandeep Cariapa (firstname.lastname@nutanix.com) if you have any questions.
# Last updated: 6/13/2019
# This script uses Python 3.7.
# NOTE:
# 1. You need a Python library called "requests" which is available from
# the url: http://docs.python-requests.org/en/latest/user/install/#install
# For reference look at:
# https://github.com/nutanix/Connection-viaREST/blob/master/nutanix-rest-api-v2-script.py
# https://github.com/nelsonad77/acropolis-api-examples

import sys
import requests
import clusterconfig as C
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Print usage messages.
def PrintUsage():

    print ("<Usage>: <{}> <VM Name>".format(sys.argv[0]))
    print ("Will output CPU/Memory usage over the last %d minutes, sampled over an interval of 30 seconds." % (C.period/60))
    return

if __name__ == "__main__":
    try:
        if (len(sys.argv) != 2):
            PrintUsage()
            sys.exit(1)

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        mycluster = C.my_api(C.src_cluster_ip,C.src_cluster_admin,C.src_cluster_pwd)
        status, cluster = mycluster.get_cluster_information()
        if (status != 200):
            print("Cannot connect to ",cluster)
            print("Did you remember to update the config file?")
            sys.exit(1)

        vm_name = sys.argv[1]
        # 1. Get the UUID of the VM.
        status, all_vms = mycluster.get_all_vm_info()
        all_vms_list = all_vms["entities"]
        found = False
        # Get VM info for each VM.
        for vm_dict in all_vms_list:
            if (vm_dict["vmName"] == vm_name):
                vm_uuid = vm_dict["uuid"]
                print ("VM NAME: ", vm_name, "VM UUID: ", vm_uuid)
                found = True
                break

        if (found == False):
            print ("Cound not find", vm_name)
            print ("Did you spel it right?")
            sys.exit(1)

        # 2. Get CPU stats.
        status, resp = mycluster.get_resource_stats(vm_uuid,"cpu")
        stats = resp['statsSpecificResponses'][0]
        if (stats['successful'] != True):
            print (">> CPU Stat call to", C.src_cluster_ip, "failed. Aborting... <<")
            sys.exit(1)
        cpu_stats = stats['values']
        i=0
        cpu_min = sys.maxsize
        cpu_max=0
        running_total=0
        for cpu in cpu_stats:
            if (cpu < cpu_min):
                cpu_min = int(cpu)
            if (cpu > cpu_max):
                cpu_max = int(cpu)
            running_total += int(cpu)
            i=i+1
            # print ("CPU: %d cpu_max: %d cpu_min: %d running_total: %d Index: %d" % (cpu,cpu_max,cpu_min,running_total,i))

        print ("Percentage utilization: CPU_MAX: %5.2f CPU_MIN: %5.2f CPU_AVG %5.2f" % (cpu_max/10000,cpu_min/10000,(running_total/10000)/i))

        # 3. Get Memory stats. This code block is remarkably similar to the code block above.
        status, resp = mycluster.get_resource_stats(vm_uuid,"memory")
        stats = resp['statsSpecificResponses'][0]
        if (stats['successful'] != True):
            print (">> Memory Stat call to", C.src_cluster_ip, "failed. Aborting... <<")
            sys.exit(1)
        mem_stats = stats['values']
        i=0
        mem_min = sys.maxsize
        mem_max=0
        running_total=0
        for mem in mem_stats:
            if (mem < mem_min):
                mem_min = int(mem)
            if (mem > mem_max):
                mem_max = int(mem)
            running_total += int(mem)
            i=i+1
            # print ("MEM: %d mem_max: %d mem_min: %d running_total: %d Index: %d" % (mem,mem_max,mem_min,running_total,i))

        print ("Percentage utilization: MEM_MAX: %5.2f MEM_MIN: %5.2f MEM_AVG %5.2f" % (mem_max/10000,mem_min/10000,(running_total/10000)/i))
        sys.exit(0)

    except Exception as ex:
        print(ex)
        sys.exit(1)
