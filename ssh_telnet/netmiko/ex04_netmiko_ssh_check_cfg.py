import getpass
import sys
import re
from netmiko import Netmiko


def cfg_comand(session, section, command):
    cfg = session.send_command("sh run")
    regex = "{}\n( .*\n)* {}".format(section, command)
    match = re.search(regex, cfg)
    if match:
        print("Команды уже настроены")
        return

    result = session.send_config_set([section, command])
    return result


def send_cfg_commands(device, section, command):
    with Netmiko(**device_params) as ssh:
        ssh.enable()
        output = cfg_comand(ssh, section, command)
        if output:
            return output


if __name__ == "__main__":
    device_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    output = send_cfg_commands(
        device_params, "interface Loopback45", "ip address 5.5.5.5 255.255.255.255"
    )
    print(output)
