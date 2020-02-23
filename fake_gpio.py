BCM = 0
PUD_UP = 0
IN = 0
OUT = 0
FALLING = 0

def _fake(*args, **kwargs):
    pass

setup = _fake
add_event_detect = _fake
setmode = _fake
cleanup = _fake

HIGH = 100
LOW = 99

def output(pin, val):
    mode = 'on' if val == LOW else 'off'
    print('Set pin %d to %s' % (pin, mode))
