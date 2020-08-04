# Modules import
import requests
from requests.auth import HTTPBasicAuth
import time

# Disable SSL warnings. Not needed in production environments with valid certificates
import urllib3
urllib3.disable_warnings()

# Authentication
BASE_URL = 'https://<IP ADDRESS or FQDN>' # Example BASE_URL = 'https://sandboxdnac.cisco.com'
AUTH_URL = '/dna/system/api/v1/auth/token'
USERNAME = '<USERNAME>' # Example USERNAME = 'devnetuser'
PASSWORD = '<PASSWORD>' # Example PASSWORD = 'Cisco123!'

# URLs
DEVICES_URL = '/dna/intent/api/v1/network-device'
SOFTWARE_IMAGE_URL='/dna/intent/api/v1/image/importation'
SOFTWARE_IMAGE_IMPORT_URL = '/dna/intent/api/v1/image/importation/source/url'
SOFTWARE_IMAGE_DISTRIBUTION_URL = '/dna/intent/api/v1/image/distribution'
SOFTWARE_IMAGE_ACTIVATION_URL = '/dna/intent/api/v1/image/activation/device'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Import software image
def import_image(headers, import_info):
    response = requests.post(BASE_URL + SOFTWARE_IMAGE_IMPORT_URL,
                            json=import_info,
                            headers=headers, verify=False)
    return response.json()['response']

# Get Software Images
def get_software_images(headers, query_params):
    response = requests.get(BASE_URL + SOFTWARE_IMAGE_URL,
                            params=query_params,
                            headers=headers, verify=False)
    return response.json()['response']

# Get devices
def get_devices(headers, query_params):
    response = requests.get(BASE_URL + DEVICES_URL,
                            params=query_params,
                            headers=headers, verify=False)
    return response.json()['response']

# Distribute image
def distribute_image(headers, distribution_info):
    response = requests.post(BASE_URL + SOFTWARE_IMAGE_DISTRIBUTION_URL,
                            json=distribution_info,
                            headers=headers, verify=False)
    return response.json()['response']

# Activate image
def activate_image(headers, activation_info):
    response = requests.post(BASE_URL + SOFTWARE_IMAGE_ACTIVATION_URL,
                            json=activation_info,
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

    # Import image
    import_info = {
        "sourceURL": "http://10.104.49.64/cat3k_caa_universalk9.16.12.03a.SPA.bin"
    }
    response = import_image(headers, import_info)

    time.sleep(30)

    # Get software images
    query_params ={
        'family': 'cat3k'
    }
    response = get_software_images(headers, query_params)
    image_id = response[0]['imageUuid']

    # Get device
    query_params = {
        'hostname': 'CAT3K-03.devnet.local'
    }

    response = get_devices(headers, query_params)
    device_id = response[0]['id']

    distribution_info = [
            {
        'deviceUuid': device_id,
        'imageUuid': image_id
        }
    ]

    response = distribute_image(headers, distribution_info)
    task_id = response['taskId']

    time.sleep(10)

    response = get_task(headers, task_id)
    print(response['data'])

    activate_info = [
            {
            'deviceUuid': device_id,
            'imageUuidList': [
                image_id
            ]
        }
    ]

    response = activate_image(headers, activate_info)
    task_id = response['taskId']

    time.sleep(10)

    response = get_task(headers, task_id)
    print(response['data'])

if __name__ == "__main__":
    main()