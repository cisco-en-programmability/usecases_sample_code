# Cisco DNA Center Health Monitoring guide

Cisco DNA Center Intent APIs provide an easy way for the developer to get an overview of the network health and drill down if needed.

The APIs seperate the information between wired and wireless clients, but also several health categories: good, fair, idle, amongst others..

## Functions

The [functions](./health-monitoring-functions.py) file uses python requests library to interact with the API.

## SDK

The [SDK](./health-monitoring-sdk.py) uses [Cisco DNA Center Python SDK](https://pypi.org/project/dnacentersdk/) to simplify the interaction with the API.

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).
