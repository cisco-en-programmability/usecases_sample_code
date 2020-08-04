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
SDA_FABRIC_URL = '/dna/intent/api/v1/business/sda/fabric'
SITE_URL = '/dna/intent/api/v1/site'
SITE_FABRIC_URL = '/dna/intent/api/v1/business/sda/fabric-site'
FABRIC_CONTROL_PLANE_URL = '/dna/intent/api/v1/business/sda/control-plane-device'
FABRIC_BORDER_URL = '/dna/intent/api/v1/business/sda/border-device'
FABRIC_EDGE_URL = '/dna/intent/api/v1/business/sda/edge-device'
SDA_AUTHENTICATION_PROFILE_URL = '/dna/intent/api/v1/business/sda/authentication-profile'
VIRTUAL_NETWORK_URL = '/dna/intent/api/v1/business/sda/virtual-network'
VIRTUAL_NETWORK_IPPOOL_URL = '/dna/intent/api/v1/business/sda/virtual-network/ippool'
SDA_PORT_ASSIGNMENT_URL = '/dna/intent/api/v1/business/sda/hostonboarding/user-device'
SDA_AP_ASSIGNMENT_URL = '/dna/intent/api/v1/business/sda/hostonboarding/access-point'

def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL, 
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get list of devices
def get_sda_fabric(headers, query_string_params):
    response = requests.get(BASE_URL + SDA_FABRIC_URL,
                            headers = headers, params = query_string_params,
                            verify=False)
    return response.json()

# Create sda fabric
def create_sda_fabric(headers, sda_fabric_info):
    response = requests.post(BASE_URL + SDA_FABRIC_URL, headers=headers, 
                             json=sda_fabric_info, verify=False)
    return response.json()

# Get list of sites
def get_sites(headers, site_params):
    response = requests.get(BASE_URL + SITE_URL, headers=headers,
                            params=site_params, verify=False)
    return response.json()['response']

# Add site to SDA fabric
def add_site_to_sda_fabric(headers, site_fabric_info):
    response = requests.post(BASE_URL + SITE_FABRIC_URL, headers=headers, 
                             json=site_fabric_info, verify=False)
    return response.json()

# Add Control Plane device
def add_control_plane_device(headers, device_info):
    response = requests.post(BASE_URL + FABRIC_CONTROL_PLANE_URL, headers=headers, 
                             json=device_info, verify=False)
    return response.json()

# Add Border device
def add_border_device(headers, device_info):
    response = requests.post(BASE_URL + FABRIC_BORDER_URL, headers=headers, 
                             json=device_info, verify=False)
    return response.json()

# Add Edge device
def add_edge_device(headers, device_info):
    response = requests.post(BASE_URL + FABRIC_EDGE_URL, headers=headers, 
                             json=device_info, verify=False)
    return response.json()

# Add default authentication profile in SDA Fabric
def add_authentication_profile(headers, authentication_profile):
    response = requests.post(BASE_URL + SDA_AUTHENTICATION_PROFILE_URL, headers=headers, 
                             json=authentication_profile, verify=False)
    return response.json()

# Add virtual network in the SDA Fabric
def add_virtual_network(headers, virtual_network):
    response = requests.post(BASE_URL + VIRTUAL_NETWORK_URL, headers=headers, 
                             json=virtual_network, verify=False)
    return response.json()

# Add Virtual Network IP Pool
def add_virtual_network_ip_pool(headers, ip_pool):
    response = requests.post(BASE_URL + VIRTUAL_NETWORK_IPPOOL_URL, headers=headers, 
                             json=ip_pool, verify=False)
    return response.json()

# Add user device port assignment
def add_user_device_port_assignment(headers, port_assignment):
    response = requests.post(BASE_URL + SDA_PORT_ASSIGNMENT_URL, headers=headers, 
                             json=port_assignment, verify=False)
    return response.json()

# Add port assignment
def add_ap_port_assignment(headers, port_assignment):
    response = requests.post(BASE_URL + SDA_PORT_ASSIGNMENT_URL, headers=headers, 
                             json=port_assignment, verify=False)
    return response.json()



def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Create SDA Fabric
    sda_fabric_info = {
        "fabricName": "DNAC_Guide_Fabric"
    }
    response = create_sda_fabric(headers, sda_fabric_info)

    site_fabric_info = {
        "fabricName": "DNAC_Guide_Fabric",
        "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building"
    }

    response = add_site_to_sda_fabric(headers, site_fabric_info)

    authentication_profile = [
        {
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building",
            "authenticateTemplateName": "No Authentication"
        }
    ]

    response = add_authentication_profile(headers, authentication_profile)

    virtual_network_info = {
        "virtualNetworkName": "INFRA_VN",
        "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building"
    }

    response = add_virtual_network(headers, virtual_network_info)

    ip_pool_info = [
        {
            "virtualNetworkName": "INFRA_VN",
            "ipPoolName": "data_ip_pool1",
            "trafficType": "DATA",
            "authenticationPolicyName": "No Authentication",
            "scalableGroupName": "",
            "isL2FloodingEnabled": True,
            "isThisCriticalPool": True,
            "poolType": "AP"
        }
    ]

    response = add_virtual_network_ip_pool(headers, ip_pool_info)

    ip_pool_info = [
        {
            "virtualNetworkName": "INFRA_VN",
            "ipPoolName": "voice_ip_pool1",
            "trafficType": "VOICE",
            "authenticationPolicyName": "No Authentication",
            "scalableGroupName": "",
            "isL2FloodingEnabled": True,
            "isThisCriticalPool": True,
            "poolType": "Extended"
        }
    ]

    response = add_virtual_network_ip_pool(headers, ip_pool_info)

    device_info = [
        {
            "deviceManagementIpAddress": "10.195.192.96",
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building"
        }
    ]

    response = add_control_plane_device(headers, device_info)
    print(response)

    device_info = [
        {
            "deviceManagementIpAddress": "10.195.192.95",
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building",
            "externalDomainRoutingProtocolName": "BGP",
            "externalConnectivityIpPoolName": "sda_1",
            "internalAutonomouSystemNumber": "65002",
            "borderSessionType": "EXTERNAL",
            "connectedToInternet": False,
            "externalConnectivitySettings": [
                {
                    "interfaceName": "FortyGigabitEthernet1/1/1",
                    "externalAutonomouSystemNumber": "65003",
                    "l3Handoff": [
                        {
                            "virtualNetwork": {
                                "virtualNetworkName": "INFRA_VN"
                            }
                        }
                    ]
                }
            ]
        }
    ]
    response = add_border_device(headers, device_info)
    
    device_info = [
        {
            "deviceManagementIpAddress": "10.195.192.95",
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building"
        }
    ]

    response = add_edge_device(headers, device_info)

    port_assignment_info = [
        {
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building",
            "deviceManagementIpAddress": "10.195.192.95",
            "interfaceName": "GigabitEthernet1/0/1",
            "dataIpAddressPoolName": "data_ip_pool1",
            "voiceIpAddressPoolName": "voice_ip_pool1",
            "scalableGroupName": "testGroupName",
            "authenticateTemplateName": "No Authentication"
        }
    ]

    response = add_user_device_port_assignment(headers, port_assignment_info)

    port_assignment_info = [
        {
            "siteNameHierarchy": "Global/DNA_Center_Guide/DNA_Center_Guide_Building",
            "deviceManagementIpAddress": "10.195.192.95",
            "interfaceName": "GigabitEthernet1/0/1",
            "addressPoolName": "data_ip_pool1",
            "authenticateTemplateName": "No Authentication"
        }
    ]
    response = add_ap_port_assignment(headers, port_assignment_info)

if __name__ == "__main__":
    main()
