import time
import RPi.GPIO as GPIO

def test_pumps():
    # Per pin labels in https://pinout.xyz/pinout/pin11_gpio17
    GPIO.setmode(GPIO.BCM)
    PUMP_PINS = [17, 27, 22, 23, 24, 25, 12, 16]  # BCM pin numbers

    for i, pin in enumerate(PUMP_PINS):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    print("Testing pumps one at a time")
    for i, pin in enumerate(PUMP_PINS):
        GPIO.output(pin, GPIO.LOW)
        print("Testing pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)

    print("Testing pumps together...")
    for i, pin in enumerate(PUMP_PINS):
        print("Enabling pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
    for i, pin in enumerate(PUMP_PINS):
        print("Disabling pump %d, BCM pin %d" % (i+1, pin))
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)

test_pumps()

