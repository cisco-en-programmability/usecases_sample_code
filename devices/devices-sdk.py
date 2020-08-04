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

print('Printing device count ...')
devices_count = dnac.devices.get_device_count()
print('Device count is', devices_count.response)

print('\nPrinting device list ...')
devices = dnac.devices.get_device_list()
for device in devices.response:
    print(device.id, device.hostname, device.managementIpAddress)

print('\nPrinting device list filtered by hostname ...')
devices = dnac.devices.get_device_list(hostname='CSR1Kv-01.devnet.local')
print_devices_info(devices)

print('\nPrinting device list filtered by platform id...')
devices = dnac.devices.get_device_list(platformId='C9500-40X')
print_devices_info(devices)

print('\nPrinting device info by device id...')
device = dnac.devices.get_device_by_id(id=devices.response[0].id)
print(device.response.id, device.response.hostname)