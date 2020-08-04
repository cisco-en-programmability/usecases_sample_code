from dnacentersdk import api
import urllib3

urllib3.disable_warnings()

dnac = api.DNACenterAPI(username="<USERNAME>", # Example username="devnetuser",
                        password="<PASSWORD>", # Example password="Cisco123!",
                        base_url="<IP ADDRESS or FQDN>", # Example base_url="https://sandboxdnac.cisco.com
                        version='1.3.3',
                        verify=False)

# Site health
print('Printing site health...')
site_health = dnac.sites.get_site_health()
for site in site_health.response:
    print('Site: {0}, Health: {1}'.format(site.siteName, site.networkHealthAverage))

# Network health
print('\nPrinting network health...')
network_health = dnac.topology.get_overall_network_health()
for network in network_health.response:
    print('Good: {0}, Bad: {1}, Health score: {2}'.format(
        network.goodCount, network.badCount,
        network.healthScore
    ))
for network in network_health.healthDistirubution:
    print('Category: {0} --> Good: {1}, Bad: {2}, Health score: {3}'.format(
        network.category, network.goodCount,
        network.badCount, network.healthScore
    ))

# Client health
print('\nPrinting client health...')
client_health = dnac.clients.get_overall_client_health()
for score in client_health.response[0]['scoreDetail']:
    print('Type: {0}, Count: {1}, Score: {2}'.format(
        score['scoreCategory']['value'],
        score['clientCount'], score['scoreValue']))
    try:
        for category in score['scoreList']:
            print('\tType: {0}, Count: {1}'.format(
                category['scoreCategory']['value'],
                category['clientCount']))
    except:
        pass