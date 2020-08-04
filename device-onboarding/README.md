# Cisco DNA Center Device Onboarding guide

## Device Onboarding API

Cisco DNA Center API can be used to provision configurations to the devices it manages. It supports network configurations that belong to the site the device is part of and also templates that can be deployed to devices, these templates support variables that can be replaced at the moment of deployment.

Templates can be used for _Day Zero Provisioning_, in order to send configuration for devices that are being onboarded to the network and Cisco DNA Center

This script creates a template for _Day Zero Provisioning_ and uses it to onboard a device.

## Functions

The [functions](./device-onboarding-functions.py) file uses python requests library to interact with the API.

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).
