# Modules import
import requests
from requests.auth import HTTPBasicAuth
import sys

# Disable SSL warnings. Not needed in production environments with valid certificates
import urllib3
urllib3.disable_warnings()

# Authentication
BASE_URL = 'https://<IP ADDRESS or FQDN>' # Example BASE_URL = 'https://sandboxdnac.cisco.com'
AUTH_URL = '/dna/system/api/v1/auth/token'
USERNAME = '<USERNAME>' # Example USERNAME = 'devnetuser'
PASSWORD = '<PASSWORD>' # Example PASSWORD = 'Cisco123!'

# URLs
DEVICES_COUNT_URL = '/dna/intent/api/v1/network-device/count'
DEVICES_URL = '/dna/intent/api/v1/network-device'
DEVICES_BY_ID_URL = '/dna/intent/api/v1/network-device/'

def print_devices_info(devices):
    # Print id, hostname and management IP
    for item in devices:
        print(item['id'], item['hostname'], item['managementIpAddress'])

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get count of devices
def get_devices_count(headers):
    response = requests.get(BASE_URL + DEVICES_COUNT_URL,
                            headers = headers,
                            verify=False)
    return response.json()['response']

# Get list of devices
def get_devices_list(headers, query_string_params):
    response = requests.get(BASE_URL + DEVICES_URL,
                            headers = headers,
                            params = query_string_params,
                            verify=False)
    return response.json()['response']

# Get information from one device
def get_devices_by_id(headers, device_id):
    response = requests.get(BASE_URL + DEVICES_BY_ID_URL + device_id, headers =  headers, verify=False)
    return response.json()['response']

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Print devices count
    devices_count = get_devices_count(headers)
    print('Printing device count ...')
    print('Device count is', devices_count)

    # print devices list
    print('\nPrinting device list ...')
    response = get_devices_list(headers, {})
    print_devices_info(response)

    # print devices list filtered by hostname
    print('\nPrinting device list filtered by hostname ...')
    query_string_params = {'hostname': 'CSR1Kv-01.devnet.local'}
    response = get_devices_list(headers, query_string_params)
    print_devices_info(response)

    # print devices list filtered by platform Id
    print('\nPrinting device list filtered by platform id...')
    query_string_params = {'platformId': 'C9500-40X'}
    response = get_devices_list(headers, query_string_params)
    print_devices_info(response)

    # print device information
    print('\nPrinting device info by device id...')
    device_id = response[0]['id']
    response = get_devices_by_id(headers, device_id)
    print(response)

if __name__ == "__main__":
    main()