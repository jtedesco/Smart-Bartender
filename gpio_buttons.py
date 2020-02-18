import os

# Fake out GPIO if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import RPi.GPIO as GPIO
else:
    print('Raspberry pi not detected, faking out GPIO')
    import fake_gpio as GPIO


def left_button(ctx):
    # TODO register to next and enter as keyboard presses
    print('Pushed left button')


def right_button(ctx):
    print('Pushed right button')


def register_handlers():
    print('Registering GPIO handlers')

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


def cleanup_handlers():
    print('Cleaning up GPIO registration')
    GPIO.cleanup()
