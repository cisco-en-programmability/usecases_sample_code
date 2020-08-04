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
GLOBAL_IP_POOLS_URL='/dna/intent/api/v1/global-pool'

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get Global pools
def get_global_ip_pools(headers, query_params):
    response = requests.get(BASE_URL + GLOBAL_IP_POOLS_URL,
                            params=query_params,
                            headers=headers, verify=False)
    return response.json()['response']

# Create Global pools
def create_global_ip_pools(headers, pool_information):
    response = requests.post(BASE_URL + GLOBAL_IP_POOLS_URL,
                            json=pool_information,
                            headers=headers, verify=False)
    return response.json()

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    pool_information = {
        "settings": {
            "ippool": [
                {
                    "ipPoolName": "DNAC-Guide_Pool",
                    "type": "Generic",
                    "ipPoolCidr": "172.30.200.0/24",
                    "gateway": "172.30.200.1",
                    "dhcpServerIps": ["10.255.3.50"],
                    "dnsServerIps": ["10.255.3.50"],
                    "IpAddressSpace":"IPv4"
                }
            ]
        }
    }

    response = create_global_ip_pools(headers, pool_information)

    time.sleep(5)

    response = get_global_ip_pools(headers, {})
    for credential in response:
        print(credential['id'], credential['ipPoolName'], credential['ipPoolCidr'])

if __name__ == "__main__":
    main()
