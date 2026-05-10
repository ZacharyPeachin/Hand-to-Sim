#!/usr/bin/env python3
"""
Directional Servo Controller Test
Tests single continuous rotation servo on Channel 0
Rotates forward 5s, backward 5s, then stops
"""

import serial
import time
import sys


class DirectionalServoTester:
    """Test directional servo on channel 0."""
    
    def __init__(self, port=None, baud=9600, timeout=2):
        """Initialize the servo tester."""
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
            print(f"Connected to servo controller on {self.port} at {self.baud} baud\n")
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
    
    def send_command(self, cmd, debug=False):
        """Send a command to the Arduino."""
        if not self.ser or not self.ser.is_open:
            print("Not connected")
            return None
        
        try:
            # Clear input buffer before sending
            self.ser.reset_input_buffer()
            
            # Send command
            command_bytes = (cmd + '\n').encode('utf-8')
            bytes_written = self.ser.write(command_bytes)
            
            if debug:
                print(f"  → Sent {bytes_written} bytes: '{cmd}'")
            
            # Wait for response
            time.sleep(0.5)
            
            # Read all available data
            response = ""
            bytes_read = 0
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore')
                response += line
                bytes_read += len(line)
            
            if debug:
                if bytes_read > 0:
                    print(f"  ← Received {bytes_read} bytes: '{response.strip()}'")
                else:
                    print(f"  ← No response received")
            
            return response.strip()
        except Exception as e:
            print(f"Command error: {e}")
            return None
    
    def forward(self):
        """Rotate servo forward."""
        response = self.send_command("forward", debug=True)
        if response:
            print(f"  ✓ {response}")
        else:
            print(f"  ✗ No response from Arduino")
        return response
    
    def backward(self):
        """Rotate servo backward."""
        response = self.send_command("backward", debug=True)
        if response:
            print(f"  ✓ {response}")
        else:
            print(f"  ✗ No response from Arduino")
        return response
    
    def stop(self):
        """Stop servo."""
        response = self.send_command("stop", debug=True)
        if response:
            print(f"  ✓ {response}")
        else:
            print(f"  ✗ No response from Arduino")
        return response
    
    def test_directions(self, forward_time=5, backward_time=5):
        """
        Test servo in both directions.
        
        Args:
            forward_time: Duration for forward rotation (seconds)
            backward_time: Duration for backward rotation (seconds)
        """
        print("=" * 50)
        print("DIRECTIONAL SERVO TEST")
        print("=" * 50)
        
        # Forward
        print(f"\nRotating FORWARD for {forward_time}s...")
        self.forward()
        time.sleep(forward_time)
        
        # Backward
        print(f"\nRotating BACKWARD for {backward_time}s...")
        self.backward()
        time.sleep(backward_time)
        
        # Stop
        print(f"\nStopping servo...")
        self.stop()
        
        print("\n" + "=" * 50)
        print("TEST COMPLETE")
        print("=" * 50)


def main():
    """Main test function."""
    port = sys.argv[1] if len(sys.argv) > 1 else None
    tester = DirectionalServoTester(port)
    
    if not tester.connect():
        return
    
    try:
        # Read initial messages from Arduino
        time.sleep(1)
        
        print("\n" + "="*60)
        print("SERIAL CONNECTION DIAGNOSTICS")
        print("="*60)
        print(f"Port: {tester.port}")
        print(f"Baud Rate: {tester.baud}")
        print("-"*60)
        
        # Clear buffer and read startup messages
        tester.ser.reset_input_buffer()
        time.sleep(0.5)
        
        print("Reading startup messages from Arduino...")
        startup_msg = ""
        if tester.ser.in_waiting > 0:
            startup_msg = tester.ser.read(tester.ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"✓ Received {len(startup_msg)} bytes")
            print(f"  Content:\n{startup_msg}")
            
            if "Servo Bonnet" in startup_msg or "Directional Controller" in startup_msg:
                print("✓ CONFIRMED: Servo Bonnet sketch detected!")
            else:
                print("⚠ WARNING: Unexpected response - may not be Servo Bonnet sketch")
        else:
            print("⚠ No startup message received")
        
        # Test echo with a simple command
        print("-"*60)
        print("Testing serial communication with 'stop' command...")
        response = tester.send_command("stop", debug=True)
        
        if response and len(response) > 0:
            print("✓ CONFIRMED: Serial communication is WORKING!")
        else:
            print("✗ ERROR: No response to 'stop' command - communication may be broken")
            print("Troubleshooting:")
            print("  1. Check USB cable is plugged in")
            print("  2. Verify correct COM port (currently: {})".format(tester.port))
            print("  3. Verify correct sketch is uploaded")
            print("  4. Try: arduino/servo_bonnet_sketch/servo_bonnet_sketch.ino")
            print("  5. Restart Arduino IDE and Arduino board")
            return
        
        print("="*60)
        print("✓ ALL DIAGNOSTICS PASSED - Ready for testing")
        print("="*60 + "\n")
        
        # Run the directional test
        tester.test_directions(forward_time=5, backward_time=5)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        tester.stop()
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
