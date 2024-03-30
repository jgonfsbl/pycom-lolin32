import config
import time
from network import WLAN
from network import Server


# Conexion a la WiFi
wlan = WLAN(mode=WLAN.STA)  # Modo adaptador wifi
wlan.connect(config.wifi_ssid, auth=(None, config.wifi_pass))   # Orden y parámetros de conexión a la red wifi
if config.REPL:
    while not wlan.isconnected():
        print('No conectado a WiFi')
        time.sleep(5)
    if wlan.isconnected():
        print('Conectado a WiFi: ' + config.wifi_ssid)

# Servicio telnet
server = Server(login=(config.user, config.password), timeout=60)
server.timeout(300) # change the timeout
