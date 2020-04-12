from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
import yaml
from netmiko import ConnectHandler


class CiscoSSH:
    def __init__(self, **device_dict):
        self.ssh = ConnectHandler(**device_dict)
        self.ssh.enable()

    def send_command(self, command):
        return self.ssh.send_command(command)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ssh.disconnect()


def connect_ssh(device_dict, command):
    with CiscoSSH(**device_dict) as session:
        result = session.send_command(command)
    return {device_dict["ip"]: result}


def threads_conn(function, devices, command, limit=2):
    all_results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command) for device in devices]
        for f in as_completed(future_ssh):
            all_results.append(f.result())
    return all_results


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    all_done = threads_conn(connect_ssh, devices, command="sh clock")
    pprint(all_done)