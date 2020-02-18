import json
import os
import threading
import time

from flask import Flask
from flask import render_template

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
            print('Making %s for %d seconds...' %
                    (drink['name'], drink['duration']))
            time.sleep(drink['duration'])
            return ('', 200)

    return server


if __name__ == "__main__":
    with open(os.path.abspath('config/pumps.json')) as f:
        pumps_config = json.load(f)
    with open(os.path.abspath('config/drinks.json')) as f:
        drinks_config = json.load(f)
        for drink in drinks_config:
            drink['duration'] = max(drink['ingredients'].values())
            drink['ingredients'] = (
                    'Contains ' + ', '.join(drink['ingredients'].keys()))
            drink['id'] = drink['name'].lower().replace(' ', '_')

    # register drink making interrupts
    # register gpio to press right/enter
    create_server(drinks_config).run(debug=True)
