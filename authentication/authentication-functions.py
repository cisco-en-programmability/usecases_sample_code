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

print('Printing authentication token...')
response = requests.post(BASE_URL + AUTH_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
print(response.json()['Token'])