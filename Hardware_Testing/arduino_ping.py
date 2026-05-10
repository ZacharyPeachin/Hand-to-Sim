#!/usr/bin/env python3
"""
Arduino Serial Communication Script
This script communicates with an Arduino Uno R3 connected via USB serial port.
"""

import serial
import time
import sys


def find_arduino_port():
    """
    Attempt to find the Arduino's serial port.
    Checks common ports on Linux.
    """
    common_ports = [
        '/dev/ttyUSB0',
        '/dev/ttyUSB1',
        '/dev/ttyACM0',
        '/dev/ttyACM1',
    ]
    
    for port in common_ports:
        try:
            ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            ser.close()
            return port
        except Exception:
            continue
    
    return None


def ping_arduino(port=None, baud=9600, timeout=2):
    """
    Send a ping to the Arduino and receive the response.
    
    Args:
        port: Serial port (e.g., '/dev/ttyUSB0'). If None, tries to auto-detect.
        baud: Baud rate (default: 9600)
        timeout: Serial timeout in seconds (default: 2)
    
    Returns:
        True if successful, False otherwise
    """
    
    # Auto-detect port if not specified
    if port is None:
        print("Attempting to auto-detect Arduino port...")
        port = find_arduino_port()
        if port is None:
            print("Could not find Arduino. Please specify the port manually.")
            print("Common ports: /dev/ttyUSB0, /dev/ttyACM0")
            return False
        print(f"Found Arduino on {port}")
    
    try:
        # Open serial connection
        ser = serial.Serial(port, baud, timeout=timeout)
        print(f"Connected to {port} at {baud} baud")
        
        # Wait for Arduino to initialize
        time.sleep(2)
        
        # Clear any residual data
        ser.reset_input_buffer()
        
        # Read the startup message
        print("\nWaiting for Arduino response...")
        timeout_counter = 0
        startup_received = False
        
        while ser.in_waiting > 0 and timeout_counter < 10:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"  {line}")
                startup_received = True
            timeout_counter += 1
        
        if not startup_received:
            print("⚠ Warning: No startup message from Arduino")
            print("Checking if Arduino is responsive...")
        
        # Send ping
        print("\nSending 'ping' command...")
        ser.write(b'ping\n')
        
        # Wait for response
        time.sleep(0.5)
        
        # Read response
        responses_received = 0
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Response: {line}")
                responses_received += 1
        
        if responses_received > 0:
            print("\n✓ Serial connection confirmed!")
        else:
            print("\n✗ ERROR: No response from Arduino!")
            print("Troubleshooting:")
            print("  1. Check USB cable is plugged in")
            print("  2. Verify Arduino sketch is uploaded")
            print("  3. Try: arduino/basic_connectivity_sketch/basic_connectivity_sketch.ino")
            print("  4. Restart Arduino IDE and Arduino board")
        
        # Close connection
        ser.close()
        print("\nConnection closed successfully!")
        return responses_received > 0
        
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def interactive_mode(port=None, baud=9600):
    """
    Enter interactive mode to send commands to the Arduino.
    
    Args:
        port: Serial port (e.g., '/dev/ttyUSB0'). If None, tries to auto-detect.
        baud: Baud rate (default: 9600)
    """
    
    # Auto-detect port if not specified
    if port is None:
        print("Attempting to auto-detect Arduino port...")
        port = find_arduino_port()
        if port is None:
            print("Could not find Arduino. Please specify the port manually.")
            return
        print(f"Found Arduino on {port}")
    
    try:
        ser = serial.Serial(port, baud, timeout=2)
        print(f"Connected to {port} at {baud} baud")
        print("Type commands to send to Arduino (type 'exit' to quit):\n")
        
        # Wait for Arduino to initialize
        time.sleep(2)
        
        # Read and display initial message
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Arduino: {line}")
        
        # Interactive loop
        while True:
            try:
                cmd = input("Enter command: ").strip()
                
                if cmd.lower() == 'exit':
                    break
                
                if cmd:
                    ser.write((cmd + '\n').encode('utf-8'))
                    time.sleep(0.5)
                    
                    # Read all available responses
                    while ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        if line:
                            print(f"Arduino: {line}")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == 'interactive':
            interactive_mode(port)
        else:
            ping_arduino(port)
    else:
        # Try to auto-detect and ping
        if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
            interactive_mode()
        else:
            ping_arduino()
