#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import time
import os

app = Flask(__name__)

# GPIO Setup - change this to your GPIO number from 'gpio readall'
GPIO_PIN = 75

class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.path = f'/sys/class/gpio/gpio{pin}'
        self.state = False
        
    def setup(self):
        """Export and initialize GPIO"""
        if not os.path.exists(self.path):
            with open('/sys/class/gpio/export', 'w') as f:
                f.write(str(self.pin))
            time.sleep(0.2)
        
        # Start as input (OFF/floating)
        with open(f'{self.path}/direction', 'w') as f:
            f.write('in')
    
    def write(self, value):
        """Write value to GPIO"""
        if value:
            # ON: Set as output, pull to ground (0V)
            with open(f'{self.path}/direction', 'w') as f:
                f.write('out')
            with open(f'{self.path}/value', 'w') as f:
                f.write('0')
            self.state = True
        else:
            # OFF: Set as input (floating)
            with open(f'{self.path}/direction', 'w') as f:
                f.write('in')
            self.state = False
    
    def cleanup(self):
        """Clean up GPIO"""
        try:
            self.write(0)
            with open('/sys/class/gpio/unexport', 'w') as f:
                f.write(str(self.pin))
        except:
            pass

# Initialize relay
relay = GPIO(GPIO_PIN)
relay.setup()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/on')
def turn_on():
    """Turn relay ON"""
    relay.write(1)
    return jsonify({'success': True, 'state': 'on'})

@app.route('/off')
def turn_off():
    """Turn relay OFF"""
    relay.write(0)
    return jsonify({'success': True, 'state': 'off'})

@app.route('/pulse')
def pulse():
    """Pulse relay (ON for 0.5s, then OFF)"""
    relay.write(1)
    time.sleep(0.5)
    relay.write(0)
    return jsonify({'success': True, 'state': 'pulsed'})

@app.route('/status')
def status():
    """Get current status"""
    return jsonify({'state': 'on' if relay.state else 'off'})

if __name__ == '__main__':
    try:
        print(f"GPIO Pin: {GPIO_PIN}")
        print("Starting on http://10.10.10.117:8080")
        app.run(host='0.0.0.0', port=8080, debug=False)
    finally:
        relay.cleanup()