import network
from time import sleep

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def scan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()

def do_connect(SSID, PSK, reconnects=5):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(reconnects=reconnects)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PSK)
        while not wlan.isconnected():
            sleep(0.1)
            pass
    print('network config:', wlan.ifconfig())
    return wlan.ifconfig()

def is_connected():
    return wlan.isconnected()
