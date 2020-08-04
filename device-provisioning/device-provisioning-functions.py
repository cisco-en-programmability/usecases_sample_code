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
DEVICES_BY_SERIAL_URL = '/dna/intent/api/v1/network-device/serial-number/{serial_number}'
NETWORK_URL = '/dna/intent/api/v1/network/{site_id}'
SITE_DEVICE_URL = '/dna/intent/api/v1/site/{site_id}/device'
SITE_URL = '/dna/intent/api/v1/site'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
TEMPLATE_DEPLOY_URL = '/dna/intent/api/v1/template-programmer/template/deploy'
TEMPLATE_PROJECT_URL = '/dna/intent/api/v1/template-programmer/project'
TEMPLATE_URL = '/dna/intent/api/v1/template-programmer/project/{project_id}/template'
TEMPLATE_VERSION_URL = '/dna/intent/api/v1/template-programmer/template/version'

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Get list of sites
def get_sites(headers):
    response = requests.get(BASE_URL + SITE_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get device by serial
def get_device_by_serial(headers, serial_number):
    response = requests.get(BASE_URL + DEVICES_BY_SERIAL_URL.format(serial_number=serial_number),
                            headers=headers,
                            verify=False)
    return response.json()['response']

# Add devices to site
def add_devices_site(headers, site_id, devices):
    headers['__runsync'] = 'true'
    headers['__runsynctimeout'] = '30'
    response = requests.post(BASE_URL + SITE_DEVICE_URL.format(site_id=site_id),
                             headers=headers, json=devices,
                             verify=False)
    return response.json()

# Create template configuration project
def create_network(headers, site_id, network):
    response = requests.post(BASE_URL + NETWORK_URL.format(site_id=site_id),
                             headers=headers, json=network,
                             verify=False)
    return response.json()

# Get template configuration project
def get_configuration_template_project(headers):
    response = requests.get(BASE_URL + TEMPLATE_PROJECT_URL,
                             headers=headers,
                             verify=False)
    return response.json()

# Create template
def create_configuration_template(headers, project_id, template):
    response = requests.post(BASE_URL + TEMPLATE_URL.format(project_id=project_id),
                             headers=headers, json=template,
                             verify=False)
    return response.json()['response']

# Create configuration template version
def create_configuration_template_version(headers, template_version):
    response = requests.post(BASE_URL + TEMPLATE_VERSION_URL, 
                             headers=headers, json=template_version,
                             verify=False)
    return response.json()['response']

# Deploy template
def deploy_configuration_template(headers, deployment_info):
    response = requests.post(BASE_URL + TEMPLATE_DEPLOY_URL,
                             headers=headers, json=deployment_info,
                             verify=False)
    return response.json()

# Get Task result
def get_task(headers, task_id):
    response = requests.get(BASE_URL + TASK_BY_ID_URL.format(task_id=task_id),
                            headers=headers, verify=False)
    return response.json()['response']

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Get Site ID
    site_name = 'DNA Center Guide Building'
    response = get_sites(headers)
    for site in response:
        if site['name'] == site_name:
            site_id = site['id']

    print('Printing site name "{site_name}" site id {site_id}'.format(site_name=site_name,
                                                                      site_id=site_id))

    # Get Device IP and Name using Serial Number
    serial_number = '919L3GOS8QC'
    response = get_device_by_serial(headers, serial_number)
    device_ip = response['managementIpAddress']
    device_name = response['hostname']
    device_ips = [device_ip]

    print('\nPrinting device serial {serial_number} device IP {ip}'.format(serial_number=serial_number,
                                                                           ip=device_ip))
    # Create Site Network
    network = {
        "settings": {
            "dhcpServer": [
                "172.30.200.5"
            ],
            "dnsServer": {
                "domainName": "devnet.local",
                "primaryIpAddress": "172.30.200.6",
                "secondaryIpAddress": "172.30.200.7"
            },
            "syslogServer": {
                "ipAddresses": [
                    "10.255.0.1"
                ],
                "configureDnacIP": True
            }
        }
    }
    response = create_network(headers, site_id, network)

    site_devices = {
        'device': device_ips
    }

    # Assign device to site
    response = add_devices_site(headers, site_id, site_devices)
    print(response['result']['progress'])

    # Get Project information
    project_name = "Onboarding Configuration"
    response = get_configuration_template_project(headers)
    project_id = ''
    for project in response:
        if project['name'] == project_name:
            project_id = project['id']

    # Create Configuration Template
    template_info = {
        "name": "DNA Center Guide",
        "description": "Guide Configuration Template",
        "tags": [],
        "deviceTypes": [
            {
                "productFamily": "Routers",
                "productSeries": "Cisco 1000 Series Integrated Services Routers"
            }
        ],
        "softwareType": "IOS-IOS",
        "softwareVariant": "IOS",
        "templateContent": "ip access-list extended $permitACLName\npermit ip 10.0.0.0 0.255.255.25.0 any\npermit ip 172.16.0.0 0.15.255.255 any\npermit ip 192.168.0.0 0.0.255.255 any\n!\n\nip access-list extended $denyACLName\ndeny ip 10.0.0.0 0.255.255.25.0 any\ndeny ip 172.16.0.0 0.15.255.255 any\ndeny ip 192.168.0.0 0.0.255.255 any\n!\n",
        "rollbackTemplateContent": "",
        "templateParams": [
            {
                "parameterName": "permitACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 1,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            },
            {
                "parameterName": "denyACLName",
                "dataType": "STRING",
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 2,
                "selection": {
                    "selectionType": None,
                    "selectionValues": {},
                    "defaultSelectedValues": []
                },
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            }
        ],
        "rollbackTemplateParams": [],
        "composite": False,
        "containingTemplates": []
    }
    response = create_configuration_template(headers, project_id, template_info)
    task_id = response['taskId']

    time.sleep(3)
    response = get_task(headers, task_id)

    template_id = response['data']

    # Create Template version
    template_version = {
        "comments": "DNAC Guide Initial Version",
        "templateId": template_id
    }
    create_configuration_template_version(headers, template_version)

    # Deploy Template to device
    deployment_info = {
        "forcePushTemplate": False,
        "isComposite": False,
        "targetInfo": [
            {
                "hostName": device_name,
                "params": {
                    "permitACLName": "GUIDE-ALLOW-ACL",
                    "denyACLName": "GUIDE-DENY-ACL"
                },
                "type": "MANAGED_DEVICE_IP"
            }
        ],
        "templateId": template_id
    }
    response = deploy_configuration_template(headers, deployment_info)
    print(response)


if __name__ == "__main__":
    main()
