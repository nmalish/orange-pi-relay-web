#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import time
import os

app = Flask(__name__)

# GPIO Setup - change this to your GPIO number
GPIO_PIN = 75

class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.path = f'/sys/class/gpio/gpio{pin}'
        
    def setup(self):
        # Export GPIO
        if not os.path.exists(self.path):
            try:
                with open('/sys/class/gpio/export', 'w') as f:
                    f.write(str(self.pin))
                time.sleep(0.1)
            except:
                pass
        
        # Set as output
        with open(f'{self.path}/direction', 'w') as f:
            f.write('out')
    
    def write(self, value):
        with open(f'{self.path}/value', 'w') as f:
            f.write(str(value))
    
    def cleanup(self):
        try:
            self.write(0)
            with open('/sys/class/gpio/unexport', 'w') as f:
                f.write(str(self.pin))
        except:
            pass

# Initialize GPIO
relay = GPIO(GPIO_PIN)
relay.setup()
relay.write(0)  # Start with relay OFF

# Store relay state
relay_state = False

@app.route('/')
def index():
    return render_template('index.html', state=relay_state)

@app.route('/toggle', methods=['POST'])
def toggle_relay():
    global relay_state
    relay_state = not relay_state
    relay.write(1 if relay_state else 0)
    return jsonify({
        'success': True,
        'state': relay_state,
        'message': 'Relay is now ' + ('ON' if relay_state else 'OFF')
    })

@app.route('/set', methods=['POST'])
def set_relay():
    global relay_state
    data = request.get_json()
    state = data.get('state', False)
    relay_state = state
    relay.write(1 if relay_state else 0)
    return jsonify({
        'success': True,
        'state': relay_state
    })

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'state': relay_state
    })

if __name__ == '__main__':
    try:
        print("Starting Relay Web Control on http://0.0.0.0:5000")
        print("Access from network: http://10.10.10.117:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        relay.cleanup()
