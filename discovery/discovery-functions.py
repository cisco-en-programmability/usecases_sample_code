# Modules import
import requests
from requests.auth import HTTPBasicAuth
import time
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
CREDENTIALS_URL = '/dna/intent/api/v1/global-credential/cli'
DISCOVERY_URL = '/dna/intent/api/v1/discovery'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
SITE_URL = '/dna/intent/api/v1/site'
DISCOVERY_DEVICES_URL = '/dna/intent/api/v1/discovery/{discovery_id}/network-device'
SITE_DEVICE_URL = '/dna/system/api/v1/site/{site_id}/device'

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Create site
def create_site(headers, site):
    headers['__runsync'] = 'true'
    headers['__runsynctimeout'] = '30'
    response = requests.post(BASE_URL + SITE_URL,
                             headers=headers, json=site,
                             verify=False)
    return response.json()

# Add devices to site
def add_devices_site(headers, site_id, devices):
    headers['__runsync'] = 'true'
    headers['__runsynctimeout'] = '30'
    response = requests.post(BASE_URL + SITE_DEVICE_URL.format(site_id=site_id),
                             headers=headers, json=devices,
                             verify=False)
    return response.json()


def create_credentials(headers, credentials):
    response = requests.post(BASE_URL + CREDENTIALS_URL, headers=headers,
                            json=credentials, verify=False)
    return response.json()['response']

def create_discovery(headers, discovery):
    response = requests.post(BASE_URL + DISCOVERY_URL, headers=headers,
                            json=discovery, verify=False)
    return response.json()['response']

# Get devices from discovery
def get_discovery_devices(headers, discovery_id):
    response = requests.get(BASE_URL + DISCOVERY_DEVICES_URL.format(discovery_id=discovery_id),
                            headers=headers, verify=False)
    return response.json()['response']

# Get Task result
def get_task(headers, task_id):
    response = requests.get(BASE_URL + TASK_BY_ID_URL.format(task_id=task_id),
                            headers=headers, verify=False)
    return response.json()['response']

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    site_area = {
        "type": "area",
        "site": {
            "area": {
                "name": "DNA Center Guide",
                "parentName": "Global"
            }
        }
    }

    print('Printing area ID...')
    response = create_site(headers, site_area)
    area_id = response['siteId']
    print(area_id)

    site_building = {
        "type": "building",
        "site": {
            "building": {
                "name": "DNA Center Guide Building",
                "parentName": "Global/DNA Center Guide",
                "latitude": "37.409424",
                "longitude": "-121.928868"
            }
        }
    }

    print('\nPrinting building ID...')
    response = create_site(headers, site_building)
    building_id = response['siteId']
    print(building_id)

    credentials = [
        {
            'description': 'DNA Center Guide Credentials',
            'enablePassword': 'C!scow02',
            'password': 'C!scow02',
            'username': 'devnet',
            'credentialType': 'GLOBAL'
        }
    ]
    response = create_credentials(headers, credentials)
    task_id = response['taskId']

    time.sleep(5)

    print('\nPrinting credential id...')
    response = get_task(headers, task_id)
    credential_id = response['progress']
    print(credential_id)

    discovery = {
        "name": "Discovery-Guide",
        "discoveryType": "Range",
        "ipAddressList": "10.255.3.11-10.255.3.19",
        "protocolOrder": "ssh",
        "timeOut": 5,
        "retryCount": 3,
        "isAutoCdp": False,
        "globalCredentialIdList": [
            credential_id
        ]
    }
    response = create_discovery(headers, discovery)
    task_id = response['taskId']

    print('\nWaiting 10 seconds for discovery to be created...')
    time.sleep(10)

    print('\nPrinting discovery id')
    response = get_task(headers, task_id)
    discovery_id = response['progress']
    print(discovery_id)

    print('\nWaiting 30 seconds for discovery to end...')
    time.sleep(30)
    response = get_discovery_devices(headers, discovery_id)
    device_ips = []
    for device in response:
        device_ips.append({'ip': device['managementIpAddress']})

    site_devices = {
        'device': device_ips
    }   

    print('\nPrinting device inclusion in site...')
    response = add_devices_site(headers, building_id, site_devices)
    print(response['result']['progress'])


if __name__ == "__main__":
    main()