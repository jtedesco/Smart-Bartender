import json
import time
import RPi.GPIO as GPIO

def test_pumps(pump_pins):
    # Per pin labels in https://pinout.xyz/pinout/pin11_gpio17
    GPIO.setmode(GPIO.BCM)

    for i, pin in enumerate(pump_pins):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    print("Testing pumps one at a time")
    for i, pin in enumerate(pump_pins):
        GPIO.output(pin, GPIO.LOW)
        print("Testing pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)

    print("Testing pumps together...")
    for i, pin in enumerate(pump_pins):
        print("Enabling pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
    for i, pin in enumerate(pump_pins):
        print("Disabling pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)


with open(os.path.abspath('../config/pumps.json')) as f:
    pumps_config = json.load(f)


pump_pins = [p['pin'] for p in pumps_config]
test_pumps(pump_pins)

