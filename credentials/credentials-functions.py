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
CLI_CREDENTIALS_URL='/dna/intent/api/v1/global-credential/cli'
CREDENTIALS_BY_ID_URL='/dna/intent/api/v1/global-credential/{credential_id}'
CREDENTIALS_URL='/dna/intent/api/v1/global-credential'
HTTP_WRITE_CREDENTIALS_URL='/dna/intent/api/v1/global-credential/http-write'
SNMP_V3_CREDENTIALS_URL='/dna/intent/api/v1/global-credential/snmpv3'

# Get Authentication token
def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    return token

# Print credentials
def print_credentials(credentials):
    for credential in credentials:
        print('Username: {0} Description: {1}'.format(
              credential['username'], 
              credential['description']))

# Create SNMP v3 credentials
def create_snmpv3_credentials(headers, credentials):
    response = requests.post(BASE_URL + SNMP_V3_CREDENTIALS_URL,
                            json = credentials,
                            headers=headers, verify=False)
    return response.json()['response']

# Create CLI credentials
def create_cli_credentials(headers, credentials):
    response = requests.post(BASE_URL + CLI_CREDENTIALS_URL,
                            json = credentials,
                            headers=headers, verify=False)
    return response.json()['response']

# Create HTTP write credentials
def create_http_write_credentials(headers, credentials):
    response = requests.post(BASE_URL + HTTP_WRITE_CREDENTIALS_URL,
                            json = credentials,
                            headers=headers, verify=False)
    return response.json()['response']

# Get credentials
def get_credentials(headers, params):
    response = requests.get(BASE_URL + CREDENTIALS_URL,
                            params=params,
                            headers=headers, verify=False)
    return response.json()['response']

def main():
    # obtain the Cisco DNA Center Auth Token
    token = get_dnac_jwt_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # Create SNMPv3 credentials
    credentials =  [
        {
        "authType": "SHA",
        "authPassword": "DNAC-2020",
        "snmpMode": "AUTHPRIV",
        "username": "dnac-guide",
        "privacyType": "AES128",
        "privacyPassword": "DNAC-PRIV-2020"
        },
        {
        "snmpMode": "NOAUTHNOPRIV",
        "username": "dnac-guide-2"
        }
    ]
    create_snmpv3_credentials(headers, credentials)
    time.sleep(3)

    # Get SNMP credentials
    print('Printing SNMP credentials...')
    query_string_params = {
        'credentialSubType': 'SNMPV3'
    }
    response = get_credentials(headers, query_string_params)
    print_credentials(response)

    # HTTP Write credentials
    credentials = [
        {
            "comments": "DNA Center HTTP credentials",
            "description": "HTTP Creds",
            "password": "HTTP-cr3d$",
            "port": "443",
            "secure": "true",
            "username": "dna-http-user"
        }
    ]
    create_http_write_credentials(headers, credentials)

    time.sleep(3)

    # Get HTTP Write credentials
    print('\nPrinting HTTP Write credentials...')
    query_string_params = {
        'credentialSubType': 'HTTP_WRITE'
    }
    response = get_credentials(headers, query_string_params)
    print_credentials(response)

    # CLI Credentials
    credentials = [
        {
            "comments": "CLI Credentials for the guide",
            "description": "Guide creds",
            "enablePassword": "Cisco123!",
            "password": "Cisco123!",
            "username": "dnac"
        }
    ]
 
    create_cli_credentials(headers, credentials)
    time.sleep(3)

    # Get CLI credentials
    print('\nPrinting CLI credentials...')
    query_string_params = {
        'credentialSubType': 'CLI'
    }
    response = get_credentials(headers, query_string_params)
    print_credentials(response)
 
if __name__ == "__main__":
    main()