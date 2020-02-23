import gpio_wrapper
import json
import os
import sys
import threading
import time

from flask import Flask
from flask import render_template
from gpio_wrapper import GPIO

# Fake out uinput if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import uinput
else:
    print('Raspberry pi not detected, faking out uinput')
    import fake_uinput as uinput


def timed_pour(pin, seconds):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(pin, GPIO.HIGH)


def create_server(drinks_config, pumps_config, sampling_mode=False):

    server = Flask(__name__)
    drink_lock = threading.Lock()
    sampling_mode = sampling_mode
    pumps_by_ingredient = {p['value']: (p['pin'], p['flowrate']) for p in pumps_config}

    @server.route("/")
    def index():
        return render_template('index.html', drinks_config=drinks_config)

    @server.route("/make_drink/<drink_id>", methods=['POST'])
    def make_drink(drink_id=None):

        if drink_lock.locked():
            message = "We're already making a drink, this should never happen!"
            print(message)
            return (message, 400)

        if not drink_id:
            message = "Asked to make a drink, but no drink id was provided!"
            print(message)
            return (message, 400)

        with drink_lock:
            drink = next(d for d in drinks_config if d['id'] == drink_id)

            print('Making %s for %d seconds...' %
                    (drink['name'], drink['duration']))

            threads = []
            for ingredient, duration in drink['ingredients'].items():
                pin, flowrate = pumps_by_ingredient[ingredient]
                duration = duration * flowrate * (0.25 if sampling_mode else 1)
                thread = threading.Thread(target=timed_pour, args=(pin, duration))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

            return ('', 200)

    return server


if __name__ == "__main__":

    # Add a mode for small quantitty drink tasting
    sampling_mode = False
    if any('sampl' in a for a in sys.argv):
        sampling_mode = True
        print('Running server in sampling mode, all drinks will be made at 1/4 size.')

    with open(os.path.abspath('config/pumps.json')) as f:
        pumps_config = json.load(f)
    ingredients_available = set(p['value'] for p in pumps_config)
    with open(os.path.abspath('config/drinks.json')) as f:
        drinks_config = json.load(f)
        updated_drinks = []
        for drink in drinks_config:
            ingredients_needed = set(drink['ingredients'].keys())
            missing_ingredients = ingredients_needed - set(ingredients_available)
            if missing_ingredients:
                print('Not loading "%s", missing %s' % (
                    drink['name'], ','.join(missing_ingredients)))
            else:
                print('Loading "%s" config...' % drink['name'])
                drink['duration'] = (
                        max(drink['ingredients'].values())
                        * (0.25 if sampling_mode else 1))
                drink['ingredients_list'] = (
                        'Contains ' + ', '.join(drink['ingredients'].keys()))
                drink['id'] = drink['name'].lower().replace(' ', '_')
                updated_drinks.append(drink)

    # register drink making interrupts
    try:
        time.sleep(1)
        with uinput.Device((uinput.KEY_ENTER, uinput.KEY_RIGHT)) as device:
            gpio_wrapper.register_handlers(device)
            create_server(updated_drinks, pumps_config, sampling_mode).run(debug=True)
    finally:
        gpio_wrapper.cleanup_handlers()
