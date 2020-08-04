# Cisco DNA Center Command Runner guide

## Command Runner API

Command runner is the feature in Cisco DNA Center that allows you to execute commands on the devices managed by Cisco DNA Center.

At the moment, command runner supports read-only commands and not configuration ones.

These scripts will execute a set of commands on multiple devices using the Cisco DNA Center API.

## Functions

The [functions](./command-runner-functions.py) file uses python requests library to interact with the API.

## SDK

The [SDK](./command-runner-sdk.py) uses [Cisco DNA Center Python SDK](https://pypi.org/project/dnacentersdk/) to simplify the interaction with the API.

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).
