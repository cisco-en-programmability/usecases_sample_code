# Module import
import requests
from requests.auth import HTTPBasicAuth

# Disable SSL warnings. Not needed in production environments with valid certificates
import urllib3
urllib3.disable_warnings()

# Authentication
BASE_URL = 'https://<IP ADDRESS or FQDN>' # Example BASE_URL = 'https://sandboxdnac.cisco.com'
AUTH_URL = '/dna/system/api/v1/auth/token'
USERNAME = '<USERNAME>' # Example USERNAME = 'devnetuser'
PASSWORD = '<PASSWORD>' # Example PASSWORD = 'Cisco123!'

# URLs
DEVICE_REPLACEMENT_URL = '/dna/intent/api/v1/device-replacement'
DEVICE_REPLACEMENT_WORKFLOW_URL = '/dna/intent/api/v1/device-replacement/workflow'


# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Mark device for replacement
def mark_device_for_replacement(headers, device_info):
    response = requests.post(BASE_URL + DEVICE_REPLACEMENT_URL,
                             headers=headers, json=device_info,
                             verify=False)
    return response.json()

# Trigger device replacement workflow
def trigger_device_replacement_workflow(headers, device_info):
    response = requests.post(BASE_URL + DEVICE_REPLACEMENT_WORKFLOW_URL,
                             headers=headers, json=device_info,
                             verify=False)
    return response.json()

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Mark device for replacement
    faulty_serial_id = ''
    device_info = [
        {
            "faultyDeviceSerialNumber": faulty_serial_id
        }
    ]

    response = mark_device_for_replacement(headers, device_info)

    # Device replacement worklfow
    replacement_serial_id = ''
    device_info = [
        {
            "faultyDeviceSerialNumber": faulty_serial_id,
            "replacementDeviceSerialNumber": replacement_serial_id
        }
    ]

    response = trigger_device_replacement_workflow(headers, device_info)


if __name__ == "__main__":
    main()
