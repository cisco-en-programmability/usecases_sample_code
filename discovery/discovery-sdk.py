from dnacentersdk import api
import urllib3
import time
import pprint
urllib3.disable_warnings()

pp = pprint.PrettyPrinter(indent=4)

dnac_url = "https://<IP/FQDN>"
dnac_username = "<USERNAME>"
dnac_password = "<PASSWORD>"
dnac_ssl_verify=False
dnac_version = "2.2.2.3"

dnacenter_client = api.DNACenterAPI(base_url=dnac_url, username=dnac_username, password=dnac_password,
    version=dnac_version, verify=dnac_ssl_verify)


def main():

    sites = dnacenter_client.sites.get_site(name='Global')
    print(f'\n"Global" Site ID is: {sites.response[0].id}')

    print('\nGetting Global CLI credentials to do discovery')
    credentials = dnacenter_client.discovery.get_global_credentials(credential_sub_type="CLI")
    credentials_ids = [credential.id for credential in credentials.response]

    print('\nCreating discovery...')
    discovery_task_id = dnacenter_client.discovery.start_discovery(name="Discovery-Guide",
        discoveryType="Range", ipAddressList="10.255.3.11-10.255.3.19",
        protocolOrder="ssh", timeout=5, retry=3, globalCredentialIdList=credentials_ids)

    print('\nWaiting 10 seconds for discovery to be created...')
    time.sleep(10)
    print(f'\nTask is: {discovery_task_id.response.taskId}')

    discovery_task = dnacenter_client.task.get_task_by_id(task_id=discovery_task_id.response.taskId) 
    time.sleep(30)
    print(f'\nDiscovery ID is: {discovery_task.response.progress}')

    discovery = dnacenter_client.discovery.get_discovered_network_devices_by_discovery_id(id=discovery_task.response.progress)

    device_ips = [device.managementIpAddress for device in discovery.response]

    site_devices = {
        "device": device_ips
    }

    dnacenter_client.sites.assign_device_to_site(site_id=sites.response[0].id, device=site_devices)

if __name__ =="__main__":
    main()