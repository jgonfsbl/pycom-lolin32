 
# This file is executed on every boot (including wake-boot from deepsleep)
# EA1HET @ 2019-01-01

import gc
import sys
from machine import Pin, deepsleep
from dht import DHT11
from time import sleep


gc.collect()

myreset=Pin(32, mode=Pin.OUT, value=1)
sensor = DHT11(Pin(4))
name = config.hostname + "-esp-%s" % binascii.hexlify(wlan_client.config("mac")[-3:]).decode("ascii")
macaddr = binascii.hexlify(wlan_client.config('mac'),':').decode('utf-8')

print('\n[System]')
print('Running Micropython on WEMOS.CC LoLin32 v1.0 Rev.1')
print('Free RAM    : %s bytes' % gc.mem_free())
print('Hostname    : {} ({})'.format(name, sys.platform))
print('Python      : %s' % sys.version)
print('WiFi MAC    :', macaddr)    

if wlan_client.isconnected():
    print('IP address  :', ip)
    print('Netmask     :', netmask)
    print('Gateway     :', gateway)
    print('DNS Server  :', dns)  
else:
    print('Networking  : Wi-Fi not connected')

sleep(5)

try:
    sensor.measure()
    print('\n[Barometer]')
    print('Temperature : %sº' % sensor.temperature())
    print('Humidity    : {}%'.format(sensor.humidity()))
    print('\nNow, going Deep Sleep...')  
    wlan_client.active(False) 
    sleep(2)
    deepsleep(60000)
except OSError as e:
    print(e)
    print('Sensor not available/operational.')
    print('Rebooting (5s)...\n')
    sleep(5)
    myreset(0)
    
