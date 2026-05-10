#!/usr/bin/env python3
"""
Adafruit Servo Bonnet Testing Script
Tests Adafruit P154 Continuous Rotation Servos via Servo Bonnet P3416
Supports 16 servo channels with continuous rotation control.

IMPORTANT: External 5V Power Supply Required!
- Connect 5V and GND from external power supply to Servo Bonnet
- This is REQUIRED for proper servo operation
- USB power alone is insufficient
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
    
    def stop_servo(self, channel):
        """
        Stop a servo.
        
        Args:
            channel: Servo channel (0-15)
        """
        cmd = f"servo_stop {channel}"
        response = self.send_command(cmd)
        if response:
            print(f"Channel {channel} stopped: {response}")
        return response
    
    def stop_all_servos(self):
        """Stop all servos on the bonnet."""
        cmd = "servo_stop_all"
        response = self.send_command(cmd)
        if response:
            print(f"All servos stopped: {response}")
        return response
    
    def test_servo_speed_range(self, channel, hold_time=1):
        """
        Test servo at various speeds.
        
        Args:
            channel: Servo channel (0-15)
            hold_time: Time to hold at each speed (seconds)
        """
        print(f"\nTesting servo speed range on channel {channel}...")
        print(f"Hold time at each speed: {hold_time}s\n")
        
        test_speeds = [255, 128, 64, 0, -64, -128, -255]
        
        for speed in test_speeds:
            print(f"Setting speed to {speed}...")
            self.set_servo_speed(channel, speed)
            time.sleep(hold_time)
        
        print("Speed range test complete!\n")
    
    def test_continuous_rotation(self, channel, duration=2):
        """
        Test continuous rotation in both directions.
        
        Args:
            channel: Servo channel (0-15)
            duration: Duration for each direction (seconds)
        """
        print(f"\nTesting continuous rotation on channel {channel}...")
        
        print(f"Rotating FORWARD at full speed for {duration}s...")
        self.set_servo_speed(channel, 255)
        time.sleep(duration)
        
        print(f"Rotating BACKWARD at full speed for {duration}s...")
        self.set_servo_speed(channel, -255)
        time.sleep(duration)
        
        print("Stopping...")
        self.set_servo_speed(channel, 0)
        time.sleep(0.5)
        
        print("Continuous rotation test complete!\n")
    
    def test_multiple_channels(self, channels, duration=1):
        """
        Test multiple servo channels.
        
        Args:
            channels: List of channel numbers (0-15)
            duration: Duration for each channel test (seconds)
        """
        print(f"\nTesting multiple channels: {channels}\n")
        
        for channel in channels:
            print(f"--- Testing channel {channel} ---")
            self.test_servo_speed_range(channel, hold_time=0.5)
        
        print("All channel tests complete!\n")
    
    def test_speed_ramp(self, channel, min_speed=-255, max_speed=255, step=50, duration=0.2):
        """
        Test smooth speed ramp.
        
        Args:
            channel: Servo channel (0-15)
            min_speed: Minimum speed to test
            max_speed: Maximum speed to test
            step: Speed increment
            duration: Duration at each speed (seconds)
        """
        print(f"\nSpeed ramp test on channel {channel}...")
        print(f"Range: {min_speed} to {max_speed}, Step: {step}\n")
        
        current_speed = min_speed
        while current_speed <= max_speed:
            self.set_servo_speed(channel, current_speed)
            time.sleep(duration)
            current_speed += step
        
        print("Stopping...")
        self.set_servo_speed(channel, 0)
        print("Speed ramp test complete!\n")


def main():
    """Main test function."""
    print("\n" + "="*50)
    print("Adafruit Servo Bonnet Testing Suite")
    print("="*50)
    print("\nIMPORTANT: External 5V power supply required!")
    print("Connect GND from power supply to Arduino GND")
    print("="*50 + "\n")
    
    port = sys.argv[1] if len(sys.argv) > 1 else None
    tester = ServoTester(port)
    
    if not tester.connect():
        return
    
    try:
        # Example: Test single servo channel
        print("=== Single Channel Speed Range Test ===")
        tester.test_servo_speed_range(channel=0, hold_time=0.5)
        
        # Example: Test continuous rotation
        print("=== Continuous Rotation Test ===")
        tester.test_continuous_rotation(channel=0, duration=1)
        
        # Example: Test speed ramp
        print("=== Speed Ramp Test ===")
        tester.test_speed_ramp(channel=0, min_speed=-200, max_speed=200, step=50, duration=0.3)
        
        print("\nAll tests completed!")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        tester.stop_all_servos()
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
