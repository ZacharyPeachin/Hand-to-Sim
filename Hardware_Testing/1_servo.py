#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import time
import sys

BAUD = 9600
TIMEOUT = 2

def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    candidates = [p for p in ports if any(k in p.description.lower()
                  for k in ['arduino', 'ch340', 'ttyacm', 'ttyusb', 'uart'])]
    if candidates:
        return candidates[0].device
    if ports:
        return ports[0].device
    return None

def connect(port=None):
    if port is None:
        port = find_arduino()
    if port is None:
        print("[ERROR] No serial ports found.")
        sys.exit(1)

    print(f"[DEBUG] Connecting to {port} at {BAUD} baud...")
    try:
        ser = serial.Serial(port, BAUD, timeout=TIMEOUT)
    except serial.SerialException as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("[DEBUG] Waiting for Arduino boot...")
    time.sleep(2)
    ser.reset_input_buffer()

    deadline = time.time() + 2
    while time.time() < deadline:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                print(f"  ARDUINO: {line}")
    return ser

def send_command(ser, cmd):
    ser.write((cmd + '\n').encode())
    ser.flush()
    deadline = time.time() + 1.0
    got = False
    while time.time() < deadline:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                print(f"  ARDUINO: {line}")
                got = True
        else:
            if got:
                break
            time.sleep(0.05)

def calibrate(ser):
    """Step through pulses to find true stop point."""
    print()
    print("=== CALIBRATION MODE ===")
    print("Servo will step toward stop.")
    print("Press ENTER each step. Type 'done' when servo stops.")
    print("Type 'q' to exit calibration.")
    print()
    send_command(ser, 's')  # start at current stop
    time.sleep(1)

    while True:
        cmd = input("Step [ENTER=decrease -/ENTER=increase +/done/q]: ").strip().lower()
        if cmd == 'q':
            break
        elif cmd == 'done':
            send_command(ser, 'p')
            print("Note the CURRENT pulse value above — update STOP in the Arduino sketch.")
            break
        elif cmd == '+':
            send_command(ser, '+')
        else:
            send_command(ser, '-')

def main():
    print("==============================")
    print("  Servo Serial Controller")
    print("==============================")

    port = sys.argv[1] if len(sys.argv) > 1 else None
    ser = connect(port)

    print()
    print("Commands: f=forward  r=reverse  s=stop")
    print("          +=faster   -=slower   p=pulse info")
    print("          c=calibrate stop point  q=quit")
    print("==============================")

    try:
        while True:
            try:
                cmd = input("\n> ").strip().lower()
            except EOFError:
                break

            if not cmd:
                continue

            if cmd == 'q':
                send_command(ser, 's')
                break
            elif cmd == 'c':
                calibrate(ser)
            elif cmd[0] in ['f', 'r', 's', '+', '-', 'p']:
                send_command(ser, cmd[0])
            else:
                print(f"Unknown: '{cmd}'")

    except KeyboardInterrupt:
        print("\nStopping...")
        try:
            send_command(ser, 's')
        except Exception:
            pass
    finally:
        ser.close()
        print("Done.")

if __name__ == '__main__':
    main()