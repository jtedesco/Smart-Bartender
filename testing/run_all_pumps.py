import json
import time
import RPi.GPIO as GPIO


 open(os.path.abspath('../config/pumps.json')) as f:
    pumps_config = json.load(f)
    pump_pins = [p['pin'] for p in pumps_config]


GPIO.setmode(GPIO.BCM)
for pin in pump_pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)


try:
    for pin in pump_pins:
        GPIO.output(pin, GPIO.LOW)
    while True:
        pass
except:
    pass
finally:
    for pin in pump_pins:
        GPIO.output(pin, GPIO.HIGH)
