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
SITE_URL = '/dna/intent/api/v1/site'
SITE_COUNT_URL = '/dna/intent/api/v1/site/count'
MEMBERSHIP_SITE_URL = '/dna/intent/api/v1/membership/{site_id}'
SITE_HEALTH_URL = '/dna/intent/api/v1/site-health'

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

# Get list of site's devices
def get_site_devices(headers, site_id):
    response = requests.get(BASE_URL + MEMBERSHIP_SITE_URL.format(site_id=site_id),
                            headers=headers, verify=False)
    return response.json()['site']['response']

# Get list of sites
def get_sites(headers):
    response = requests.get(BASE_URL + SITE_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get sites count
def get_site_count(headers):
    response = requests.get(BASE_URL + SITE_COUNT_URL,
                            headers=headers, verify=False)
    return response.json()['response']

# Get site's health
def get_site_health(headers, site_id):
    response = requests.get(BASE_URL + SITE_HEALTH_URL.format(site_id=site_id),
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

    print('\nPrinting site count...')
    response = get_site_count(headers)
    print(response)

    print('\nPrinting sites')
    response = get_sites(headers)
    print(response)

    print('\nPrinting site\'s devices')
    site_id = response[1]['id']
    response = get_site_devices(headers, site_id)
    print(len(response))

    print('\nPrinting site\'s health')
    response = get_site_health(headers, site_id)
    site_name = response[0]['siteName']
    site_health = response[0]['healthyNetworkDevicePercentage']
    print('Name: {site_name}, Average health: {site_health}'
          .format(site_name=site_name, site_health=site_health))




if __name__ == "__main__":
    main()