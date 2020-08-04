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
SITE_TOPOLOGY_URL = '/dna/intent/api/v1/topology/site-topology'
PHYSICAL_TOPOLOGY_URL = '/dna/intent/api/v1/topology/physical-topology'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
L2_TOPOLOGY_URL = '/dna/intent/api/v1/topology/l2/{vlan_id}'

# Get nodes/links
def get_nodes_links(data):
    nodes = {}
    for node in data['nodes']:
        nodes[node['id']] = node['label']
   
    for link in data['links']:
        print('Source: {0}({1}) Target: {2}({3}) Status: {4}'.format(
            nodes[link['source']], link.get('startPortName', ''),
            nodes[link['target']], link.get('endPortName', ''),
            link['linkStatus']
        ))

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get site topology
def get_site_topology(headers):
    response = requests.get(BASE_URL + SITE_TOPOLOGY_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get physical topology
def get_physical_topology(headers):
    response = requests.get(BASE_URL + PHYSICAL_TOPOLOGY_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get L2 topology
def get_l2_topology(headers, vlan_id):
    response = requests.get(BASE_URL + L2_TOPOLOGY_URL.format(vlan_id=vlan_id),
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

    print('Printing site topology...')
    response = get_site_topology(headers)
    for site in response['sites']:
        print(site['name'], '-->' ,site['groupNameHierarchy'])

    print('\nPrinting physical topology...')
    response = get_physical_topology(headers)
    get_nodes_links(response)

    print('\nPrinting L2 topology...')
    response = get_l2_topology(headers, 3001)
    get_nodes_links(response)

if __name__ == "__main__":
    main()