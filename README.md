# Smart Bartender

Raspberry Pi-based smart bartender using a simple Python server & HDMI display. This project was forked from a HackerShack project but rewritten from the ground up. This version uses peristaltic pumps controlled by a Raspberry Pi, two Gpio buttons for controls, and a small HDMI display pointed to a local Python server that dispenses drinks.

## Configuration Files

JSON configs are used for both the pump attributes (e.g. ingredient names, flow rates) and the drinks themselves. On startup, the server filters the drink list to only include drinks with all ingredients available in the pump configs.

### pumps.json

The pump configuration persists information about pumps and the liquids that they are assigned to. An pump entry looks like this:

```
"pump_1": {
    "flowrate": 20,
		"name": "Pump 1",
		"pin": 17, 
		"value": "gin"
	}
```

Flowrate indicates the time (in seconds) that it takes for this pump to pull 1oz of liquid through the tube. This can be adjusted to adjust pump timings for faster or slower pumps (or for adjustments like pumps with carbonated ingredients, which may pull less liquid volume per second than non-carbonated liquids).

Each pump key needs to be unique. It is comprised of `name`, `pin`, and `value`. `name` is the display name shown to the user on the pump configuration menu, `pin` is the GPIO pin attached to the relay for that particular pump, and `value` is the current selected drink. `value` doesn't need to be set initially, but it will be changed once you select an option from the configuration menu.

### drinks.json

The drinks configuration maps pump `value` entries to `ingredients` to configure the time required per pump. All ingredient values are in units of ounces and will be scaled using the flowrate pump config to determine the specific timing.

The `name` will both be the name displayed, and unless `image` is provided, the background image for the menu item on the server. `garnish` displays an optional message for a few seconds after the drink is completed.

```
{
  "name": "Sazerac",
  "ingredients": {
    "absinthe": 0.25,
    "simple syrup": 0.5,
    "rye whisky": 1.5
  },
  "garnish": "Add three drops of Peychaud's bitters and lemon peel"
}
```

## Running Outside RaspberryPI

The Python server uses a set of stub libraries for gpio and automatically switches to these libraries instead of the real gprio libraries when running off of a Raspberry PI. This allows development of the drink server on devices other than the Raspberry Pi.

## Testing Utilities

The `testing` directory contains several utilities for testing components of the Raspberry Pi:

1. `calibrate_pumps.py`: Runs a given pump for a fixed time. Useful for determining the flowrate of individual pumps to pour one ounce of liquid.

1. `run_all_pumps.py`: Runs all pumps at once. Useful for rinsing or washing the pump tubes

1. `run_pump.py`: Runs a single pump until the script is quit

1. `test_buttons.py`: Attaches a listener to print debug when gpio buttons are pressed

1. `test_pumps.py`: Tests both the pump wiring and total amperage draw by individually starting each pump, then starting them all at once in sequence.

## Running the Code

First, make sure to download this repository on your raspberry pi. Once you do, navigate to the downloaded folder in the terminal:

```
cd ~/path/to/directory
```

and install the dependencies

```
sudo pip install -r requirements.txt
```

You can start the bartender by running

```
sudo python server.py
```

### Autostart.sh

The commands described below are consolidated into `autostart.sh`. Adding this shell script to auto-run should be sufficient to accomplish both steps below.

### Running the Server at Startup

You can configure the bartender to run at startup by starting the program from the `rc.local` file. First, make sure to get the path to the repository directory by running

```
pwd
```

from the repository folder. Copy this to your clipboard.

Next, type

```
sudo vim /etc/rc.local
```

to open the rc.local file. Next, press `i` to edit. Before the last line, add the following two lines:

```
cd your/pwd/path/here
sudo python server.py &
```

`your/pwd/path/here` should be replaced with the path you copied above. `sudo python server.py &` starts the bartender program in the background. Finally, press `esc` then `ZZ` to save and exit. 

If that doesn't work, you can consult this [guide](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) for more options.

### Running the Browser at Startup

Once the server launches at startup, you can show the server's landing page automatically at startup by adding the following command to auto-run after the server launches (with some delay):

```
sleep 5 && chromium-browser --kiosk --disable-session-crashed-bubble http://localhost:5000  && unclutter -idle 0.1 -root &
```

This command launches Chromium full-screen and hides the cursor.
