# DISCLAIMER: This script is not supported by Nutanix. Please contact
# Sandeep Cariapa (firstname.lastname@nutanix.com) if you have any questions.
import json
import time
import requests
from urllib.parse import quote
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Time period is one hour (3600 seconds).
period=3600

# AHV cluster details. We need these in order to log into the REST API.
src_cluster_ip = "555.666.777.888"
src_cluster_admin = "restapiuser"
src_cluster_pwd = "blahblahblah"

# ========== DO NOT CHANGE ANYTHING UNDER THIS LINE =====
class my_api():
    def __init__(self,ip,username,password):

        # Cluster IP, username, password.
        self.ip_addr = ip
        self.username = username
        self.password = password
        # Base URL at which v1 REST services are hosted in Prism Gateway.
        base_urlv1 = 'https://%s:9440/PrismGateway/services/rest/v1/'
        self.base_urlv1 = base_urlv1 % self.ip_addr
        self.sessionv1 = self.get_server_session(self.username, self.password)
        # Base URL at which v2 REST services are hosted in Prism Gateway.
        base_urlv2 = 'https://%s:9440/PrismGateway/services/rest/v2.0/'
        self.base_urlv2 = base_urlv2 % self.ip_addr
        self.sessionv2 = self.get_server_session(self.username, self.password)

    def get_server_session(self, username, password):

        # Creating REST client session for server connection, after globally
        # setting authorization, content type, and character set.
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

    # Get cluster information.
    def get_cluster_information(self):

        cluster_url = self.base_urlv2 + "cluster/"
        print("Getting cluster information for cluster %s." % self.ip_addr)
        try:
            server_response = self.sessionv2.get(cluster_url)
            return server_response.status_code ,json.loads(server_response.text)
        except Exception as ex:
            print(ex)
            return -1,cluster_url

    # Get all VMs in the cluster.
    def get_all_vm_info(self):

        cluster_url = self.base_urlv1 + "vms/"
        server_response = self.sessionv1.get(cluster_url)
        # print("Response code: %s" % server_response.status_code)
        return server_response.status_code ,json.loads(server_response.text)

    # Get resource stats.
    def get_resource_stats(self, vm_uuid, resource):

        if (resource == "cpu"):
            metric = "hypervisor_cpu_usage_ppm"
        elif (resource == "memory"):
            metric = "memory_usage_ppm"

        cur_time = int(time.time())
        start_time = cur_time - period
        # Now convert to usecs.
        cur_time = cur_time * 1000000
        start_time = start_time * 1000000

        # From: https://www.digitalformula.net/2018/api/vm-performance-stats-with-nutanix-rest-api/
        # https://10.133.16.50:9440/api/nutanix/v1/vms/3aa1699a-ec41-4037-aade-c73a9d14ed8c/stats/?metrics=hypervisor_cpu_usage_ppm&startTimeInUsecs=1524009660000000&endTimeInUsecs=1524096060000000&interval=30

        cluster_url = self.base_urlv1 + "vms/" + vm_uuid + "/stats/?metrics=" + metric + "&startTimeInUsecs="
        cluster_url += str(start_time) + "&" + "endTimeInUsecs=" + str(cur_time) + "&interval=30"
        # print ("Cluster_URL: ", cluster_url)
        server_response = self.sessionv1.get(cluster_url)
        # print("Response code: %s" % server_response.status_code)
        return server_response.status_code ,json.loads(server_response.text)
