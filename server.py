import json
import os
import threading
import time

# Fake out uinput if not on a raspberry pi
if 'raspberrypi' in os.uname():
    import uinput
else:
    print('Raspberry pi not detected, faking out uinput')
    import fake_uinput as uinput

from flask import Flask
from flask import render_template

import gpio_wrapper


def create_server(drinks_config):

    server = Flask(__name__)
    drink_lock = threading.Lock()

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

            # TODO: pour in parallel
            timed_pour(pin, time)

            print('Making %s for %d seconds...' %
                    (drink['name'], drink['duration']))

            time.sleep(drink['duration'])

            return ('', 200)

    return server


if __name__ == "__main__":
    with open(os.path.abspath('config/pumps.json')) as f:
        pumps_config = json.load(f)
    ingredients_available = set(p['value'] for p in pumps_config)
    with open(os.path.abspath('config/drinks.json')) as f:
        drinks_config = json.load(f)
        for drink in drinks_config:
            ingredients_needed = set(drink['ingredients'].keys())
            missing_ingredients = ingredients_needed - set(ingredients_available)
            if missing_ingredients:
                print('Not loading "%s", missing %s' % (
                    drink['name'], ','.join(missing_ingredients)))
            else:
                print('Loading "%s" config...' % drink['name'])
                drink['duration'] = max(drink['ingredients'].values())
                drink['ingredients'] = (
                        'Contains ' + ', '.join(drink['ingredients'].keys()))
                drink['id'] = drink['name'].lower().replace(' ', '_')

    # TODO: add a sampling mode

    # register drink making interrupts
    try:
        time.sleep(1)
        with uinput.Device((uinput.KEY_ENTER, uinput.KEY_RIGHT)) as device:
            gpio_wrapper.register_handlers(device)
            create_server(drinks_config).run(debug=True)
    finally:
        gpio_wrapper.cleanup_handlers()
