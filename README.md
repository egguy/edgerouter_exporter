# edgerouter_exporter
Export stats for the edgerouter

create an configuration file named *config.json* like this:

```
{
  "device_type": "vyatta_vyos",
  "ip": "172.16.255.1",
  "username": "ubnt",
  "password": "ubnt"
}

```

Run the exporter with `python exporter.py`. The stats are available on the port 9097
