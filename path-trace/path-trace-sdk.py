from dnacentersdk import api
import urllib3
import time
import pprint
urllib3.disable_warnings()

pp = pprint.PrettyPrinter(indent=4)

dnac_url = "https://<IP/FQDN>"
dnac_username = "<username>"
dnac_password = "<password>"
dnac_ssl_verify=False
dnac_version = "2.2.2.3"

dnacenter_client = api.DNACenterAPI(base_url=dnac_url, username=dnac_username, password=dnac_password,
    version=dnac_version, verify=dnac_ssl_verify)


network_devices = dnacenter_client.devices.get_device_list(hostname='ISR-4K--Branch-SFO') # CHANGE ME
network_devices_2 = dnacenter_client.devices.get_device_list(hostname='C9K-Branch-SFO.clus-demo.com') #CHANGE ME


path_trace = dnacenter_client.path_trace.initiate_a_new_pathtrace(destIP=network_devices_2.response[0].managementIpAddress,
                                                     sourceIP=network_devices.response[0].managementIpAddress,
                                                     inclusions=['INTERFACE-STATS', 'DEVICE-STATS', 'ACL-TRACE', 'QOS-STATS'], 
                                                     protocol='icmp')

time.sleep(60)
flow_analysis = dnacenter_client.path_trace.retrieves_previous_pathtrace(flow_analysis_id=path_trace.response.flowAnalysisId)
pp.pprint(flow_analysis)
