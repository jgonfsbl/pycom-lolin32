# This file is executed on every boot (including wake-boot from deepsleep)
# EA1HET @ 2019-01-01

import config
import network
import ubinascii as binascii
from time import sleep


print('\n[Booting]')
print('\nShutting down self-run AP')
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)    

print('\nConnecting to IoT network')
wlan_client = network.WLAN(network.STA_IF) 

for i in range(3):
    if not wlan_client.isconnected():
        wlan_client.active(True) 
        wlan_client.connect(config.essid, config.passphrase)
        sleep(5)
    else:
    	break
        
if wlan_client.isconnected(): 
    (ip, netmask, gateway, dns) = wlan_client.ifconfig()  
else:
    wlan_client.active(False)    
