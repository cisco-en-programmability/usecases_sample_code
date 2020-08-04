# Modules import
import requests
from requests.auth import HTTPBasicAuth
import json
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
COMMAND_RUNNER_SEND_URL = '/dna/intent/api/v1/network-device-poller/cli/read-request'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
FILE_GET_BY_ID = '/dna/intent/api/v1/file/{file_id}'


# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get devices by platform ID
def get_devices_ids(headers, query_string_params):
    response = requests.get(BASE_URL + DEVICES_URL, headers=headers,
                            params=query_string_params, verify=False)
    devices = []
    for device in response.json()['response']:
        devices.append(device['id'])
    return devices

# Send commands to devices
def send_commands(headers, payload):
    response = requests.post(BASE_URL + COMMAND_RUNNER_SEND_URL, json=payload,
                            headers=headers, verify=False)
    return response.json()['response']

# Get Task result
def get_task(headers, task_id):
    response = requests.get(BASE_URL + TASK_BY_ID_URL.format(task_id=task_id), headers=headers, verify=False)
    return response

# Get file with command results
def get_file(headers, file_id):
    response = requests.get(BASE_URL + FILE_GET_BY_ID.format(file_id=file_id), headers=headers, verify=False)
    return response.json()

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    
    query_string_params = {'platformId': 'C9500-40X'}
    devices = get_devices_ids(headers, query_string_params)
    payload = {
    "commands": [
        "show version",
        "show ip int brief"
    ],
    "deviceUuids": devices,
    "timeout": 0
    }

    response = send_commands(headers, payload)

    # Wait to have a response back from the devices
    time.sleep(10)

    response = get_task(headers, response['taskId'])
    progress_json = json.loads(response.json()['response']['progress'])
    file_id = progress_json['fileId']

    # Get file
    response = get_file(headers, file_id)
    print(response[0]['commandResponses']['SUCCESS']['show ip int brief'])

if __name__ == "__main__":
    main()
