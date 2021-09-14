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

area = {
        "type": "area",
        "site": {
            "area": {
                "name": "Altus",
                "parentName": "Global/Costa Rica"
            }
        }
    }

dnacenter_client.sites.create_site(payload=area)

building = {
        "type": "building",
        "site": {
            "building": {
                "name": "HQ",
                "parentName": "Global/Costa Rica/Altus",
                "latitude": 9.7489,
                "longitude": -83.7534
            }
        }
    }

dnacenter_client.sites.create_site(payload=building)

floor = {
        "type": "floor",
        "site": {
            "floor": {
                "name": "Floor4",
                "parentName": "Global/Costa Rica/Altus/HQ",
                "height": 100,
                "length": 100,
                "width": 20,
                "rfModel": "Drywall Office Only"
            }
        }
    }

dnacenter_client.sites.create_site(payload=floor)

sites = dnacenter_client.sites.get_site()
pp.pprint(sites)

