from dnacentersdk import api
import urllib3
import time
import pprint
urllib3.disable_warnings()

pp = pprint.PrettyPrinter(indent=4)

dnac_url = "https://<IP/FQDN>"
dnac_username = "<username>"
dnac_password = "<password>"
dnac_ssl_verify=False
dnac_version = "2.2.2.3"

dnacenter_client = api.DNACenterAPI(base_url=dnac_url, username=dnac_username, password=dnac_password,
    version=dnac_version, verify=dnac_ssl_verify)

#SNMP v3 Credentials
snmpv3_credentials =  [
        {
        "authType": "SHA",
        "authPassword": "DNAC-2020",
        "snmpMode": "AUTHPRIV",
        "username": "dnac-guide",
        "privacyType": "AES128",
        "privacyPassword": "DNAC-PRIV-2020",
        "comments": "DNAC Guide",
        "description": "DNAC Guide"
        },
        {
        "snmpMode": "NOAUTHNOPRIV",
        "username": "dnac-guide-2",
        "comments": "DNAC Guide (2)",
        "description": "DNAC Guide 2"
        }
    ]

dnacenter_client.discovery.create_snmpv3_credentials(payload=snmpv3_credentials)
time.sleep(3)

credentials = dnacenter_client.discovery.get_global_credentials(credential_sub_type='SNMPV3')
pp.pprint(credentials)

# HTTP Credentials
credentials = [
    {
        "description": "DNAC Guide",
        "comments": "DNAC Guide",
        "password": "HTTP-cr3d$",
        "port": 443,
        "secure": True,
        "username": "dna-http-user"
    }
]

dnacenter_client.discovery.create_http_write_credentials(payload=credentials)
time.sleep(3)

credentials = dnacenter_client.discovery.get_global_credentials(credential_sub_type='HTTP_WRITE')
pp.pprint(credentials)

# CLI Credentials
credentials = [
    {
        "description": "DNAC Guide",
        "comments": "DNAC Guide",
        "enablePassword": "Cisco123!",
        "password": "Cisco123!",
        "username": "dnac"
    }
]
dnacenter_client.discovery.create_cli_credentials(payload=credentials)
time.sleep(3)

credentials = dnacenter_client.discovery.get_global_credentials(credential_sub_type='CLI')
pp.pprint(credentials)

