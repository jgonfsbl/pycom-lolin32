
""" Lopy4 con placa pysense actuando como nodo de LORAWAN en modo ABP.
    Envía los datos de los sensores integrados en la placa.
    Para el funcionamiento se deben incluir las siguiejtes librerías en el directorio
    /lib.
    - Pysense.py
    - SI7006A20.py
    - Pycoproc
    - SI7006A20
    - LTR329ALS01
    - MPL3115A2
"""

from network import LoRa
import socket
import binascii
import struct
import time
import config
import machine
from pysense import Pysense
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,PRESSURE
from LIS2HH12 import LIS2HH12


###### Bloque configuracion y conexión a LoRa ######
lora = LoRa(mode=LoRa.LORAWAN)  # Iniciamos LoRa en modo LORAWAN.

dev_addr = struct.unpack(">l", binascii.unhexlify(config.dev_addr))[0]
nwk_swkey = binascii.unhexlify(config.nwk_swkey)
app_swkey = binascii.unhexlify(config.app_swkey)

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))   # Comando de union a la red usando ABP

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

s.setblocking(False)
###### Fin bloque LoRa ######




###### Bloque lectura sensores y envio de datos por Lora ######
py = Pysense()
mp = MPL3115A2(py,mode=PRESSURE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)


while True:

    # Lectura de los sensores integrados en la placa Pysense
    temperatura = si.temperature()
    humedad = si.humidity()
    rocio = si.dew_point()
    presion = mp.pressure() / 100
    voltaje = py.read_battery_voltage()


    # Impresión de los datos a la consola REPL
    if config.REPL:
        print('La temperatura es: ' + str(temperatura) + 'C')
        print('Con una humedad de ' + str(humedad) + '%RH y punto de rocio ' + str(rocio) + 'C')
        print('La presion atmosferica es de ' + str(presion) + ' mBar')
        print('La bateria tiene un voltaje de: ' + str(voltaje) + 'V')


    # Conversion de los valores a Bytes
    temperatura = round(round(temperatura, 2) / 0.005)
    temperatura = struct.pack('!h', temperatura)
    humedad = round(round(humedad, 2) / 0.005)
    humedad = struct.pack('!H', humedad)
    rocio = round(round(rocio, 2) / 0.005)
    rocio = struct.pack('!h', rocio)
    presion = round(round(presion, 0))
    presion = struct.pack('!H', presion)
    voltaje = round(round(voltaje, 2) / 0.005)
    voltaje = struct.pack('!H', voltaje)


    # Envio de datos a TTN
    databytes = temperatura + humedad + rocio + presion + voltaje
    if config.REPL:
        print('Enviando datos a la red LoRa')
    s.send(databytes)
    time.sleep(config.tiempo)


###### Fin bloque envio de datos ######
