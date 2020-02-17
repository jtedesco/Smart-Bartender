import json
import os

from flask import Flask
from flask import render_template

def create_server(drinks_config):

    server = Flask(__name__)

    @server.route("/")
    def index():
        return render_template('index.html', drinks_config=drinks_config)

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
