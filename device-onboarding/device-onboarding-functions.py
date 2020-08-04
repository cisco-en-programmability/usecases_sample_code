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
SITE_PROFILE_ADD_SITE_URL = '/api/v1/siteprofile/{site_profile_id}/site/{site_id}'
SITE_PROFILE_URL = '/api/v1/siteprofile'
SITE_URL = '/dna/intent/api/v1/site'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'
TEMPLATE_PROJECT_URL = '/dna/intent/api/v1/template-programmer/project'
TEMPLATE_URL = '/dna/intent/api/v1/template-programmer/project/{project_id}/template'
TEMPLATE_VERSION_URL = '/dna/intent/api/v1/template-programmer/template/version'
ONBOARDING_PNP_IMPORT_URL = '/dna/intent/api/v1/onboarding/pnp-device/import'
ONBOARDING_CLAIM_DEVICE_URL = '/dna/intent/api/v1/onboarding/pnp-device/site-claim'

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

# Create site profile
def create_site_profile(headers, site_profile_info):
    response = requests.post(BASE_URL + SITE_PROFILE_URL,
                             headers=headers, json=site_profile_info,
                             verify=False)
    return response.json()['response']

# Assign Site to Site Profile
def assign_site_to_site_profile(headers, site_profile_id, site_id):
    response = requests.post(BASE_URL + 
                             SITE_PROFILE_ADD_SITE_URL.format(site_profile_id=site_profile_id,
                                                              site_id=site_id),
                             headers=headers, verify=False)
    return response.json()

# Import device to PnP process
def import_device_to_pnp(headers, pnp_import_info):
    response = requests.post(BASE_URL + ONBOARDING_PNP_IMPORT_URL,
                             headers=headers, json=pnp_import_info,
                             verify=False)
    return response.json()

# Import device to PnP process
def claim_device_to_site(headers, claim_info):
    response = requests.post(BASE_URL + ONBOARDING_PNP_IMPORT_URL,
                             headers=headers, json=claim_info,
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

    # # Get Device IP and Name using Serial Number
    device_serial = '919L3GOS8QC'
    device_name = 'CAT9k-DNAC-Guide'
    device_pid = 'C9500-40X'

    # Get Project information
    project_name = "Onboarding Configuration"
    response = get_configuration_template_project(headers)
    project_id = ''
    for project in response:
        if project['name'] == project_name:
            project_id = project['id']

    # Create Configuration Template
    template_info = {
        "name": "DNA Center Guide - Day0",
        "description": "Guide Configuration Template",
        "tags": [],
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
                "productSeries": "Cisco Catalyst 9500 Series Switches"
            }
        ],
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
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
        "comments": "DNAC Guide Day 0 Initial Version",
        "templateId": template_id
    }
    create_configuration_template_version(headers, template_version)

    # Create Configuration Template
    site_profile_info = {
        "name": "DNA Center Guide Profile",
        "namespace": "switching",
        "profileAttributes": [
            {
                "key": "day0.templates",
                "attribs": [
                    {
                        "key": "device.family",
                        "value": "Switches and Hubs",
                        "attribs": [
                            {
                                "key": "device.series",
                                "value": "Cisco Catalyst 9500 Series Switches",
                                "attribs": [
                                    {
                                        "key": "device.type",
                                        "attribs": [
                                            {
                                                "key": "template.id",
                                                "value": template_id,
                                            },
                                            {
                                                "key": "device.tag",
                                                "value": "",
                                                "attribs": [

                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    response = create_site_profile(headers, site_profile_info)

    task_id = response['taskId']

    time.sleep(3)
    response = get_task(headers, task_id)

    site_profile_id = response['data']

    response = assign_site_to_site_profile(headers, site_profile_id, site_id)

    # Add device to PnP process

    pnp_import_info = [
        {
            "deviceInfo": {
                "hostname": device_name,
		        "serialNumber": device_serial,
		        "pid": device_pid,
		        "sudiRequired": False,
		        "userSudiSerialNos": [],
		        "aaaCredentials": {
                    "username": "",
                 	"password": ""
		        }
            }
        }
    ]

    response = import_device_to_pnp(headers, pnp_import_info)

    device_id = response['successList'][0]['id']

    claim_info = {
        "siteId": site_id,
        "deviceId": device_id,
        "type": "Default",
        "configInfo": {
            "configId": template_id,
            "configParameters": {
                "permitACLName": "GUIDE-ALLOW-ACL",
                "denyACLName": "GUIDE - DENY - ACL"
            }
        }
    }

    claim_device_to_site(headers, claim_info)



if __name__ == "__main__":
    main()
