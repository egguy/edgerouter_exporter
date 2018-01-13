# encoding: utf-8

import json
import sys
import time

from netmiko import ConnectHandler
from paramiko import SSHException
from prometheus_client import start_http_server, Gauge


def parse_dhcp_stats(input: str) -> dict:
    """Parse the return of the show dhcp statistics

    :param input:
    :return:
    """
    found_pool = False
    found_dash = False

    stats = {}

    for line in input.split("\n"):
        line = line.strip().replace("\x1b[m", "")

        if not line:
            continue

        if not found_pool and line.startswith("pool"):
            found_pool = True
            continue
        elif found_pool and found_dash is False and line.startswith("----"):
            found_dash = True
            continue
        elif found_pool and found_dash:
            dhcp_stats = line.split()
            if len(dhcp_stats) != 4:
                continue
            stats[dhcp_stats[0]] = {
                "size": int(dhcp_stats[1]),
                "used": int(dhcp_stats[2]),
                "avail": int(dhcp_stats[3])
            }
    return stats


if __name__ == '__main__':
    config = json.load(open('config.json'))

    free_leases = Gauge('dhcp_stats_available', 'DHCP Usage: free leases', ['network'])
    used_leases = Gauge('dhcp_stats_used', 'DHCP Usage: used lease', ['network'])

    start_http_server(9097)

    try:
        c = ConnectHandler(**config)
    except SSHException:
        print("There's a problem connecting to the switch.")
        sys.exit()

    while True:
        command_result = c.send_command('show dhcp statistics')
        result = parse_dhcp_stats(command_result)
        for network, data in result.items():
            free_leases.labels(network=network).set(data['avail'])
            used_leases.labels(network=network).set(data['used'])
        time.sleep(30)