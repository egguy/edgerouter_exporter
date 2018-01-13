from exporter import parse_dhcp_stats


def test_parse_dhcp_stats():
    result = parse_dhcp_stats('\x1b=\npool                           pool size  # leased   # avail\x1b[m\n----                           ---------  --------   -------\x1b[m\nVLAN_255                              21         0        21\x1b[m\n')
    excepted = {
        "VLAN_255": {
            "size": 21,
            "used": 0,
            "avail": 21
        }

    }
    print(result)

    assert result == excepted