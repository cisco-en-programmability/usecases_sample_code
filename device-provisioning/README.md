# Cisco DNA Center Device Provisioning guide

## Device Provisioning API

Cisco DNA Center API can be used to provision configurations to the devices it manages. It supports network configurations that belong to the site the device is part of and also templates that can be deployed to devices, these templates support variables that can be replaced at the moment of deployment.

The script creates a Device Provision template and uses it to provision a device.

## Functions

The [functions](./device-provisioning-functions.py) file uses python requests library to interact with the API.

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).
