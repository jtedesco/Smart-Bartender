import json
import os
import sys
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

with open(os.path.abspath('../config/pumps.json')) as f:
    pump_config = json.load(f)

GPIO.setmode(GPIO.BCM)
for i, config in enumerate(pump_config):
    GPIO.setup(config['pin'], GPIO.OUT, initial=GPIO.HIGH)

pump_i = int(sys.argv[1]) - 1
assert(pump_i) < len(pump_config)
config = pump_config[pump_i]
print('Running %s, flowrate %.2f, pin %d, with %s' % (
    config['name'], config['flowrate'], config['pin'], config['value']))

pin = config['pin']
try:
    GPIO.output(pin, GPIO.LOW)
    while True:
        pass
except:
    pass
finally:
    GPIO.output(pin, GPIO.HIGH)
