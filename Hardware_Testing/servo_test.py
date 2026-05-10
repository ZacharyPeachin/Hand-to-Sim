#!/usr/bin/env python3
"""
Adafruit Servo Bonnet Testing Script
Tests Adafruit P154 Continuous Rotation Servos via Servo Bonnet P3416
Supports 16 servo channels with continuous rotation control.
"""

import serial
import time
import sys


class ServoTester:
    """Test servo motors (continuous rotation) connected via Adafruit Servo Bonnet."""
    
    def __init__(self, port=None, baud=9600, timeout=2):
        """
        Initialize the servo tester.
        
        Args:
            port: Serial port (e.g., '/dev/ttyUSB0')
            baud: Baud rate (default: 9600)
            timeout: Serial timeout in seconds
            
        Note: Ensure external 5V power supply is connected to Servo Bonnet!
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
            print(f"Connected to servo controller on {self.port} at {self.baud} baud")
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
    
    def set_servo_speed(self, channel, speed):
        """
        Set continuous rotation servo to a specific speed.
        
        Args:
            channel: Servo channel (0-15)
            speed: Speed in range -255 (full reverse) to 255 (full forward)
                  0 = stop
        """
        if channel < 0 or channel > 15:
            print(f"Invalid channel: {channel}. Must be between 0-15.")
            return False
        
        if speed < -255 or speed > 255:
            print(f"Invalid speed: {speed}. Must be between -255 and 255.")
            return False
        
        cmd = f"servo_speed {channel} {speed}"
        response = self.send_command(cmd)
        if response:
            direction = "FORWARD" if speed > 0 else "BACKWARD" if speed < 0 else "STOP"
            print(f"Channel {channel} speed set to {speed} ({direction}): {response}")
        return response
    
    def sweep_servo(self, servo_pin, start=0, end=180, step=10, duration=0.1):
        """
        Sweep servo through a range of angles.
        
        Args:
            servo_pin: Arduino pin number
            start: Starting angle
            end: Ending angle
            step: Angle increment
            duration: Duration at each angle (seconds)
        """
        print(f"\nSweeping servo on pin {servo_pin} from {start}° to {end}°...\n")
        
        current_angle = start
        while (current_angle <= end and step > 0) or (current_angle >= end and step < 0):
            print(f"Angle: {current_angle}°")
            self.set_servo_angle(servo_pin, current_angle)
            time.sleep(duration)
            current_angle += step
        
        print("Sweep complete!\n")
    
    def test_servo_limits(self, servo_pin, min_angle=0, max_angle=180, hold_time=1):
        """
        Test servo limits by moving to min and max angles.
        
        Args:
            servo_pin: Arduino pin number
            min_angle: Minimum angle to test
            max_angle: Maximum angle to test
            hold_time: Time to hold at each limit (seconds)
        """
        print(f"\nTesting servo limits on pin {servo_pin}...")
        print(f"Min: {min_angle}°, Max: {max_angle}°\n")
        
        print(f"Moving to minimum angle ({min_angle}°)...")
        self.set_servo_angle(servo_pin, min_angle)
        time.sleep(hold_time)
        
        print(f"Moving to maximum angle ({max_angle}°)...")
        self.set_servo_angle(servo_pin, max_angle)
        time.sleep(hold_time)
        
        print(f"Returning to center (90°)...")
        self.set_servo_angle(servo_pin, 90)
        time.sleep(hold_time)
        
        print("Limit test complete!\n")
    
    def test_multiple_servos(self, servo_pins):
        """
        Test multiple servos in sequence.
        
        Args:
            servo_pins: List of servo pin numbers
        """
        print(f"\nTesting multiple servos on pins: {servo_pins}\n")
        
        for pin in servo_pins:
            print(f"--- Testing servo on pin {pin} ---")
            self.test_servo_limits(pin, hold_time=0.5)
        
        print("All servo tests complete!\n")
    
    def test_servo_smoothness(self, servo_pin, iterations=3):
        """
        Test servo smoothness by repeatedly sweeping.
        
        Args:
            servo_pin: Arduino pin number
            iterations: Number of full sweeps to perform
        """
        print(f"\nTesting servo smoothness on pin {servo_pin} ({iterations} iterations)...\n")
        
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}")
            self.sweep_servo(servo_pin, start=0, end=180, step=30, duration=0.05)
            time.sleep(0.5)
        
        print("Smoothness test complete!\n")


def main():
    """Main test function."""
    print("Servo Testing Suite\n")
    
    port = sys.argv[1] if len(sys.argv) > 1 else None
    tester = ServoTester(port)
    
    if not tester.connect():
        return
    
    try:
        # Example: Test single servo on pin 3
        print("=== Single Servo Sweep Test ===")
        tester.sweep_servo(servo_pin=3, start=0, end=180, step=15, duration=0.1)
        
        # Example: Test servo limits
        print("=== Servo Limits Test ===")
        tester.test_servo_limits(servo_pin=3)
        
        # Example: Test servo smoothness
        print("=== Servo Smoothness Test ===")
        tester.test_servo_smoothness(servo_pin=3, iterations=2)
        
        print("\nAll tests completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
