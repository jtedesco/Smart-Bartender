import os
import threading
import time

# Prevent accidental "make drink" pushes by holding a global lock
# when a button press is registered
_gpio_lock = threading.Lock()
_last_pressed = time.time()
_BOUNCE_MS = 500

# Fake out uinput if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import uinput
else:
    print('Raspberry pi not detected, faking out uinput')
    import fake_uinput as uinput

# Fake out GPIO if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
else:
    print('Raspberry pi not detected, faking out GPIO')
    import fake_gpio as GPIO


def register_handlers(device):
    print('Registering GPIO handlers')

    LEFT_BTN = 26
    RIGHT_BTN = 13

    GPIO.setup(LEFT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def left_button(ctx):
        global _gpio_lock
        global _last_pressed
        with _gpio_lock:
            if (time.time() < _last_pressed + (_BOUNCE_MS / 1000.0)):
                print('Duplicate left press suppressed')
                return
            device.emit_click(uinput.KEY_RIGHT)
            _last_pressed = time.time()

    def right_button(ctx):
        global _gpio_lock
        global _last_pressed
        with _gpio_lock:
            if (time.time() < _last_pressed + (_BOUNCE_MS / 1000.0)):
                print('Duplicate right press suppressed')
                return
            device.emit_click(uinput.KEY_ENTER)
            _last_pressed = time.time()

    GPIO.add_event_detect(
            LEFT_BTN,
            GPIO.FALLING,
            callback=left_button,
            bouncetime=_BOUNCE_MS)
    GPIO.add_event_detect(
            RIGHT_BTN,
            GPIO.FALLING,
            callback=right_button,
            bouncetime=_BOUNCE_MS)


def cleanup_handlers():
    print('Cleaning up GPIO registration')
    GPIO.cleanup()


def init_outputs(pumps_config):
    for config in pumps_config:
        GPIO.setup(config['pin'], GPIO.OUT, initial=GPIO.HIGH)


if __name__ == "__main__":
    try:
        time.sleep(1)
        with uinput.Device((uinput.KEY_ENTER, uinput.KEY_RIGHT)) as device:
            register_handlers(device)
            while True:
                pass
    finally:
        cleanup_handlers()
