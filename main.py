import secrets.wifi #SSID, PSK
print(secrets.wifi.SSID, secrets.wifi.PSK)
import main.network as nw

# Print wifi scan in json
import json
print(json.dumps(nw.scan()))

# Connect to wifi, default to reconnect 5 times
nw.do_connect(secrets.wifi.SSID, secrets.wifi.PSK)
