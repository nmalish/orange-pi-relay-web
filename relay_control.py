#!/usr/bin/env python3
import time
import os

# GPIO number - change this to match your pin
# Check with: gpio readall
GPIO_PIN = 75 

class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.path = f'/sys/class/gpio/gpio{pin}'
        
    def setup(self):
        # Export GPIO
        if not os.path.exists(self.path):
            with open('/sys/class/gpio/export', 'w') as f:
                f.write(str(self.pin))
            time.sleep(0.1)
        
        # Start with pin floating (input mode)
        with open(f'{self.path}/direction', 'w') as f:
            f.write('in')
    
    def write(self, value):
        if value:
            # ON: Set as output and pull to ground (0V)
            with open(f'{self.path}/direction', 'w') as f:
                f.write('out')
            with open(f'{self.path}/value', 'w') as f:
                f.write('0')
        else:
            # OFF: Set as input (floating/high impedance)
            with open(f'{self.path}/direction', 'w') as f:
                f.write('in')
    
    def cleanup(self):
        try:
            # Set to floating state before cleanup
            self.write(0)
            with open('/sys/class/gpio/unexport', 'w') as f:
                f.write(str(self.pin))
        except:
            pass

# Create GPIO object
relay = GPIO(GPIO_PIN)
relay.setup()

print("Relay Control - Press Ctrl+C to exit")

try:
    while True:
        print("Relay ON")
        relay.write(1)
        time.sleep(2)
        
        print("Relay OFF")
        relay.write(0)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nCleaning up...")
    relay.write(0)
    relay.cleanup()
    print("Done!")
