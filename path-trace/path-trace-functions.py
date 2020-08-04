# Modules import
import requests
from requests.auth import HTTPBasicAuth
import sys
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
PATH_TRACE_URL = '/dna/intent/api/v1/flow-analysis'
PATH_TRACE_ID_URL = '/dna/intent/api/v1/flow-analysis/{flow_analysis_id}'

def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL, 
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get list of devices
def get_devices(headers, query_string_params):
    response = requests.get(BASE_URL + DEVICES_URL,
                            headers = headers,
                            params = query_string_params,
                            verify=False)
    return response.json()['response']

# Create path trace
def create_path_trace(headers, path_trace_payload):
    response = requests.post(BASE_URL + PATH_TRACE_URL, headers=headers, 
                             json=path_trace_payload, verify=False)
    return response.json()['response']

# Get path trace result
def get_path_trace_by_id(headers, flow_analysis_id):
    response = requests.get(BASE_URL + PATH_TRACE_ID_URL.format(flow_analysis_id=flow_analysis_id), 
                            headers=headers, verify=False)
    return response.json()['response']

# Get path trace summary
def get_path_traces_summary(headers, query_string_params):
    response = requests.get(BASE_URL + PATH_TRACE_URL, 
                            params=query_string_params, 
                            headers=headers, verify=False)
    return response.json()['response'] 
    

# Delete path trace
def delete_path_trace(headers, flow_analysis_id):
    response = requests.delete(BASE_URL + PATH_TRACE_ID_URL.format(flow_analysis_id=flow_analysis_id),
                               headers=headers, verify=False)
    return response


def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Get src device IP
    print('Printing source device IP ...')
    query_string_params = {'hostname': 'CSR1Kv-01.devnet.local'}
    response = get_devices(headers, query_string_params)
    src_ip_address = response[0]['managementIpAddress']
    print(src_ip_address)

    # print devices list
    print('\nPrinting destination device IP ...')
    query_string_params = {'hostname': 'CSR1Kv-09.devnet.local'}
    response = get_devices(headers, query_string_params)
    dst_ip_address = response[0]['managementIpAddress']
    print(dst_ip_address)

    # Generate a new path trace
    print('\nPrinting flow analysis id ...')
    path_trace_payload = {
        'sourceIP': src_ip_address,
        'destIP': dst_ip_address,
        'inclusions': [
            'INTERFACE-STATS',
            'DEVICE-STATS',
            'ACL-TRACE',
            'QOS-STATS'
        ],
        'protocol': 'icmp'
    }
    response = create_path_trace(headers, path_trace_payload)
    flow_analysis_id = response['flowAnalysisId']
    print(flow_analysis_id)

    # Waiting until the path trace is done
    time.sleep(10)

    # Get path trace result
    print('\nPrinting path trace result ...')
    response = get_path_trace_by_id(headers, flow_analysis_id)
    print(response)
    
    # Get path traces summary
    print('\nPrinting path trace summary...')
    query_string_params = {'destIP': dst_ip_address, 'limit': 2}
    response = get_path_traces_summary(headers,  query_string_params)
    print(response)

    # Delete path trace summary
    print('\nPrinting path trace delete status code ...')
    response = delete_path_trace(headers, flow_analysis_id)
    print(response.status_code)


if __name__ == "__main__":
    main()
