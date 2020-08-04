# Cisco DNA Center Credentials guide

## Credentials API

Cisco DNA Center Credentials API allows you to manage the credentials used for discovery and management of network devices.

Both command runner API and Discover APIs use the credentials to communicate with the devices.

It supports different kind of credentials: SNMP (2/3), NETCONF, CLI (Telnet/SSH) and HTTP.

This script creates different types of credentials.

## Functions

The [functions](./credentials-functions.py) file uses python requests library to interact with the API.

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).
