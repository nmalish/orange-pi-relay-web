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
        
        # Set as output
        with open(f'{self.path}/direction', 'w') as f:
            f.write('out')
    
    def write(self, value):
        with open(f'{self.path}/value', 'w') as f:
            f.write(str(value))
    
    def cleanup(self):
        try:
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
