# Pequeño ejemplo de parpadeo del Led en Lolin32.
# El led está conectado al pin 22. El led se enciende con un nivel bajo en ese
# pin.

import time
import machine

# Tiempos de led encendido y apagado (En segundos).
TiempoOff = 1
TiempoOn = 2

LedPin = machine.Pin(22, machine.Pin.OUT)

while True:
    LedPin(1)
    time.sleep(TiempoOff)
    LedPin(0)
    time.sleep(TiempoOn)
