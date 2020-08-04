from dnacentersdk import api
import urllib3
import time
import json
urllib3.disable_warnings()

dnac = api.DNACenterAPI(username="<USERNAME>", # Example username="devnetuser",
                        password="<PASSWORD>", # Example password="Cisco123!",
                        base_url="<IP ADDRESS or FQDN>", # Example base_url="https://sandboxdnac.cisco.com
                        version='1.3.3',
                        verify=False)

devices = dnac.devices.get_device_list(platform_id='C9500-40X')
device_ids = []
for device in devices.response:
    device_ids.append(device.id)

print(device_ids)
commands = ['show version', "show ip interface brief"]
command_runner = dnac.command_runner.run_read_only_commands_on_devices(commands=commands,
                                                                       deviceUuids=device_ids,
                                                                       timeout=0)

time.sleep(20)

task = dnac.task.get_task_by_id(command_runner.response.taskId)
progress_json = json.loads(task.response.progress)
print(progress_json)
file_id = progress_json['fileId']
print(file_id)

file_info = dnac.file.download_a_file_by_fileid(file_id=file_id)
print(file_info)