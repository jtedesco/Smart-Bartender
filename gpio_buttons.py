import os
import time
import uinput


# Fake out GPIO if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import RPi.GPIO as GPIO
else:
    print('Raspberry pi not detected, faking out GPIO')
    import fake_gpio as GPIO


def register_handlers(device):
    print('Registering GPIO handlers')

    GPIO.setmode(GPIO.BCM)

    LEFT_BTN = 13
    RIGHT_BTN = 26
    LEFT_PIN_BOUNCE = 300
    RIGHT_PIN_BOUNCE = 300

    GPIO.setup(LEFT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def left_button(ctx):
        device.emit_click(uinput.KEY_ENTER)

    def right_button(ctx):
        device.emit_click(uinput.KEY_RIGHT)

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


if __name__ == "__main__":
    try:
        time.sleep(1)
        with uinput.Device((uinput.KEY_ENTER, uinput.KEY_RIGHT)) as device:
            register_handlers(device)
            while True:
                pass
    finally:
        cleanup_handlers()
