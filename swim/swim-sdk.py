from dnacentersdk import api
import urllib3
import time
import pprint
urllib3.disable_warnings()

pp = pprint.PrettyPrinter(indent=4)

dnac_url = "<IP/FQDN>"
dnac_username = "<USERNAME>"
dnac_password = "<PASSWORD>"
dnac_ssl_verify=False
dnac_version = "2.2.2.3"

dnacenter_client = api.DNACenterAPI(base_url=dnac_url, username=dnac_username, password=dnac_password,
    version=dnac_version, verify=dnac_ssl_verify)


def main():
    payload = {
        "sourceURL": "http://10.104.49.64/cat3k_caa_universalk9.16.12.03a.SPA.bin"
    }
    dnacenter_client.software_image_management_swim.import_software_image_via_url(payload=payload)

    time.sleep(30)

    software_images = dnacenter_client.software_image_management_swim.get_software_image_details(family='cat3k')

    devices = dnacenter_client.devices.get_device_list(hostname='CAT3K-03.devnet.local')

    image_distribution = [
        {
            'deviceUuid': devices.response[0].id,
            'imageUuid': devices.response[0].imageUuid,
            'distributeIfNeeded': True
        }
    ]

    dnacenter_client.software_image_management_swim.trigger_software_image_activation(payload=image_distribution)




if __name__ == "__main__":
    main()