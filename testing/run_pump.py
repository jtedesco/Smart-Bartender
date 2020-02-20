
import RPi.GPIO as GPIO

with open(os.path.abspath('../config/pumps.json')) as f:
    pump_config = json.load(f)

GPIO.setmode(GPIO.BCM)
for i, config in enumerate(pump_config):
    print('Setting up pump %d (%s), flowrate %.2f, pin %d, with %s' % (
        i, config['flowrate'], config['name'], config['flowrate'], config['pin'], config['value']))
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

for i, config in enumerate(pump_config):
pump_i = int(sys.argv[1])
assert(pump_i) < len(pump_config)
config = pump_config[pump_i]
print('Running pump %d (%s), flowrate %.2f, pin %d, with %s' % (
    pump_i, config['flowrate'], config['name'], config['flowrate'], config['pin'], config['value']))

ounce_time = 1 * config['flowrate']

try:
    GPIO.output(pin, GPIO.LOW)
    while True:
        pass
except:
    GPIO.output(pin, GPIO.HIGH)
