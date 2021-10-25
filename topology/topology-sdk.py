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

def main():
    site_topology = dnacenter_client.topology.get_site_topology()

    for site in site_topology.response.sites:
        print(f'{site.name} --> {site.groupNameHierarchy}')

    physical_topology = dnacenter_client.topology.get_physical_topology()

    get_nodes_links(physical_topology.response)

    l2_topology = dnacenter_client.topology.get_topology_details(vlan_id="1")
    get_nodes_links(l2_topology.response)



if __name__ == "__main__":
    main()