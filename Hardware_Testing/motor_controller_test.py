#!/usr/bin/env python3
"""
Motor Controller Testing Script
Tests motor controllers connected to Arduino via PWM pins.
Supports various motor controller types (L298N, TB6612FNG, etc.)
"""

import serial
import time
import sys


class MotorControllerTester:
    """Test motor controllers connected to Arduino."""
    
    def __init__(self, port=None, baud=9600, timeout=2):
        """
        Initialize the motor controller tester.
        
        Args:
            port: Serial port (e.g., '/dev/ttyUSB0')
            baud: Baud rate (default: 9600)
            timeout: Serial timeout in seconds
        """
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = None
    
    def connect(self):
        """Connect to the Arduino."""
        if self.port is None:
            self.port = self._find_arduino_port()
            if self.port is None:
                print("Could not find Arduino port")
                return False
        
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"Connected to motor controller on {self.port} at {self.baud} baud")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the Arduino."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected")
    
    def _find_arduino_port(self):
        """Auto-detect Arduino port."""
        common_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
        for port in common_ports:
            try:
                ser = serial.Serial(port, 9600, timeout=1)
                time.sleep(1)
                ser.close()
                return port
            except Exception:
                continue
        return None
    
    def send_command(self, cmd):
        """Send a command to the Arduino."""
        if not self.ser or not self.ser.is_open:
            print("Not connected")
            return None
        
        try:
            self.ser.write((cmd + '\n').encode('utf-8'))
            time.sleep(0.3)
            
            response = ""
            while self.ser.in_waiting > 0:
                response += self.ser.readline().decode('utf-8', errors='ignore')
            
            return response.strip()
        except Exception as e:
            print(f"Command error: {e}")
            return None
    
    def test_motor_speed(self, motor_pin, speed_percent):
        """
        Test motor at specified speed.
        
        Args:
            motor_pin: Arduino pin number
            speed_percent: Speed 0-100%
        """
        speed_value = int((speed_percent / 100.0) * 255)
        cmd = f"motor_speed {motor_pin} {speed_value}"
        response = self.send_command(cmd)
        if response:
            print(f"Motor on pin {motor_pin} at {speed_percent}%: {response}")
        return response
    
    def test_motor_direction(self, pin1, pin2, direction):
        """
        Test motor direction with two control pins.
        
        Args:
            pin1: First control pin
            pin2: Second control pin
            direction: 'forward' or 'backward'
        """
        cmd = f"motor_direction {pin1} {pin2} {direction}"
        response = self.send_command(cmd)
        if response:
            print(f"Motor direction ({pin1}, {pin2}) set to {direction}: {response}")
        return response
    
    def test_motor_stop(self, pin1, pin2=None):
        """
        Stop motor.
        
        Args:
            pin1: First control pin
            pin2: Second control pin (optional)
        """
        if pin2:
            cmd = f"motor_stop {pin1} {pin2}"
        else:
            cmd = f"motor_stop {pin1}"
        response = self.send_command(cmd)
        if response:
            print(f"Motor stopped: {response}")
        return response
    
    def run_speed_ramp_test(self, motor_pin, start=0, end=100, step=10, duration=1):
        """
        Test motor with speed ramp.
        
        Args:
            motor_pin: Arduino pin number
            start: Starting speed percentage
            end: Ending speed percentage
            step: Speed increment percentage
            duration: Duration at each speed (seconds)
        """
        print(f"\nRunning speed ramp test on pin {motor_pin}...")
        print(f"Range: {start}% to {end}%, Step: {step}%\n")
        
        current_speed = start
        while (current_speed <= end and step > 0) or (current_speed >= end and step < 0):
            print(f"Setting speed to {current_speed}%")
            self.test_motor_speed(motor_pin, current_speed)
            time.sleep(duration)
            current_speed += step
        
        print("Stopping motor...")
        self.test_motor_stop(motor_pin)
        print("Speed ramp test complete!\n")
    
    def run_direction_test(self, pin1, pin2, duration=3):
        """
        Test motor in both directions.
        
        Args:
            pin1: First control pin
            pin2: Second control pin
            duration: Duration for each direction (seconds)
        """
        print(f"\nRunning direction test on pins {pin1} and {pin2}...")
        
        print("Testing FORWARD direction...")
        self.test_motor_direction(pin1, pin2, 'forward')
        time.sleep(duration)
        
        print("Testing BACKWARD direction...")
        self.test_motor_direction(pin1, pin2, 'backward')
        time.sleep(duration)
        
        print("Stopping motor...")
        self.test_motor_stop(pin1, pin2)
        print("Direction test complete!\n")


def main():
    """Main test function."""
    print("Motor Controller Testing Suite\n")
    
    port = sys.argv[1] if len(sys.argv) > 1 else None
    tester = MotorControllerTester(port)
    
    if not tester.connect():
        return
    
    try:
        # Check serial connection
        print("Checking serial connection...")
        time.sleep(1)
        
        if tester.ser.in_waiting > 0:
            startup_msg = tester.ser.read(tester.ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"Arduino startup: {startup_msg}")
            
            if "Motor Controller" in startup_msg:
                print("✓ Serial connection confirmed - Motor Controller detected!")
            else:
                print("⚠ Warning: Unexpected Arduino response. Check if correct sketch is uploaded.")
        else:
            print("⚠ Warning: No response from Arduino. Checking if sketch is running...")
            # Try sending a test command
            tester.send_command("motor_stop 9")
            time.sleep(0.5)
            if tester.ser.in_waiting > 0:
                response = tester.ser.read(tester.ser.in_waiting).decode('utf-8', errors='ignore')
                print(f"Arduino responded: {response}")
                print("✓ Serial connection confirmed!")
            else:
                print("✗ ERROR: No response from Arduino!")
                print("Troubleshooting:")
                print("  1. Check USB cable is plugged in")
                print("  2. Verify correct sketch is uploaded")
                print("  3. Try: arduino/motor_controller_sketch/motor_controller_sketch.ino")
                print("  4. Restart Arduino IDE and Arduino board")
                return
        
        # Example: Test motor on pin 9 with speed ramp
        print("\n=== Speed Ramp Test ===")
        tester.run_speed_ramp_test(motor_pin=9, start=0, end=100, step=20, duration=1)
        
        # Example: Test motor on pins 8 and 9 for direction
        print("=== Direction Test ===")
        tester.run_direction_test(pin1=8, pin2=9, duration=2)
        
        print("\nAll tests completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
