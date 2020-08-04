from dnacentersdk import api
import urllib3
urllib3.disable_warnings()

def print_devices_info(devices_info):
    for device in devices_info.response:
        print(device.id, device.hostname, 
              device.managementIpAddress)



dnac = api.DNACenterAPI(username="<USERNAME>", # Example username="devnetuser",
                        password="<PASSWORD>", # Example password="Cisco123!",
                        base_url="<IP ADDRESS or FQDN>", # Example base_url="https://sandboxdnac.cisco.com
                        version='1.3.3',
                        verify=False)

print('Printing authentication token...')
print(dnac.access_token)