import time
import RPi.GPIO as GPIO


def left_button(ctx):
    print('Pushed left button')


def right_button(ctx):
    print('Pushed right button')


def test_buttons():
    GPIO.setmode(GPIO.BCM)

    LEFT_BTN = 13
    RIGHT_BTN = 26
    LEFT_PIN_BOUNCE = 300
    RIGHT_PIN_BOUNCE = 300

    GPIO.setup(LEFT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
            LEFT_BTN,
            GPIO.FALLING,
            callback=left_button,
            bouncetime=LEFT_PIN_BOUNCE)
    GPIO.add_event_detect(
            RIGHT_BTN,
            GPIO.FALLING,
            callback=right_button,
            bouncetime=RIGHT_PIN_BOUNCE)

    while True:
        pass

try:
    test_buttons()
except KeyboardInterrupt:
    print('Cleaning up GPIO')
    GPIO.cleanup()
