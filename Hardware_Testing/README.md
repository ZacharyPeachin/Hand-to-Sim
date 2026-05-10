# Hardware Testing Suite

This directory contains testing scripts and Arduino sketches for various hardware components.

## 📋 Directory Structure

```
Hardware_Testing/
├── arduino_sketch/
│   ├── arduino_sketch.ino                    (Basic serial ping test)
│   ├── motor_controller_sketch.ino           (Motor controller test)
│   └── adafruit_servo_bonnet_sketch.ino      (Adafruit servo bonnet)
├── arduino_ping.py                           (Basic Arduino communication test)
├── motor_controller_test.py                  (Motor controller Python test)
├── servo_test_bonnet.py                      (Servo bonnet Python test)
└── README.md                                 (This file)
```

---

## ⚡ POWER REQUIREMENTS

### Adafruit Servo Bonnet P3416 + P154 Servos

**🔴 EXTERNAL 5V POWER SUPPLY IS REQUIRED! DO NOT SKIP THIS!**

**Why?**
- The Adafruit Servo Bonnet can control up to 16 servos simultaneously
- Each servo draws significant current (up to 700mA at full load)
- USB power (500mA max) is insufficient for even a single servo
- Without external power, servos will jitter, overheat, or fail

**How to Connect:**
1. Get a 5V power supply (recommended: 2A+ for multiple servos)
2. Connect power supply **GND (black)** to Arduino **GND**
3. Connect power supply **+5V (red)** to Servo Bonnet **+5V (VCC)**
4. **DO NOT connect power supply +5V directly to Arduino** (keep USB for data only)

**Power Supply Recommendations:**
- Standalone 5V power supply: 2-3A minimum
- 5V/2A USB power adapter (works for testing)
- Lab power supply set to 5V, 2A+

**Connection Diagram:**
```
[External PSU]         [Arduino + Servo Bonnet]
    +5V ──────────────→ Servo Bonnet VCC
    GND ───────┬───────→ Arduino GND
               └───────→ Servo Bonnet GND
    
    USB ──────────────→ Arduino (data only)
```

---

## 🔧 Hardware Setup

### Motor Controllers (L298N, TB6612FNG, etc.)

**Upload:**
```bash
# Upload motor_controller_sketch.ino to Arduino
```

**Test:**
```bash
python3 motor_controller_test.py /dev/ttyUSB0
```

**Serial Commands:**
- `motor_speed pin speed_value` - Set PWM speed (0-255)
- `motor_direction pin1 pin2 direction` - Set direction (forward/backward)
- `motor_stop pin1 [pin2]` - Stop motor

---

### Adafruit Servo Bonnet + Continuous Rotation Servos

**Requirements:**
- Arduino Uno R3
- Adafruit Servo Bonnet P3416
- Adafruit P154 Continuous Rotation Servo(s)
- **External 5V Power Supply (REQUIRED)**

**Arduino Library:**
1. Install Adafruit PWM Servo Driver library:
   - Sketch → Include Library → Manage Libraries
   - Search: "Adafruit PWM Servo Driver"
   - Install by Adafruit

**Upload:**
```bash
# Upload adafruit_servo_bonnet_sketch.ino to Arduino
```

**Test:**
```bash
python3 servo_test_bonnet.py /dev/ttyUSB0
```

**Serial Commands:**
- `servo_speed channel speed` - Set servo speed (-255 to 255)
  - Positive = forward rotation
  - Negative = backward rotation
  - 0 = stop
- `servo_stop channel` - Stop specific servo
- `servo_stop_all` - Stop all servos
- `test` - Run diagnostic test

**Servo Speed Reference:**
- **255**: Full forward speed
- **128**: Half forward speed
- **64**: Quarter forward speed
- **0**: Complete stop
- **-64**: Quarter reverse speed
- **-128**: Half reverse speed
- **-255**: Full reverse speed

**Channel Mapping:**
- Channels 0-15 correspond to the 16 outputs on the Servo Bonnet
- Connect P154 servo to desired channel (each channel can power 1 servo)

---

## 🧪 Testing Procedures

### Basic Connectivity Test

```bash
python3 arduino_ping.py /dev/ttyUSB0
```

### Motor Controller Test

```bash
python3 motor_controller_test.py /dev/ttyUSB0
```

**Tests included:**
- Speed ramp test (0% → 100% → 0%)
- Direction test (forward/backward)

### Servo Bonnet Test

```bash
python3 servo_test_bonnet.py /dev/ttyUSB0
```

**Tests included:**
- Speed range test
- Continuous rotation test
- Speed ramp test
- Multi-channel testing support

---

## 🔍 Troubleshooting

### Servo Jitter
- **Cause**: Insufficient power
- **Fix**: Ensure external 5V power supply is connected and GND is common

### Servo Won't Move
- **Cause**: Power supply not connected OR channel not configured
- **Fix**: 
  1. Check power supply connections
  2. Verify servo is connected to Servo Bonnet channel
  3. Run `test` command in Arduino sketch

### Serial Connection Failed
- **Cause**: Wrong port OR Arduino not detected
- **Fix**:
  1. List ports: `ls /dev/tty*`
  2. Common ports: `/dev/ttyUSB0`, `/dev/ttyACM0`
  3. Check permissions: `sudo usermod -a -G dialout $USER`

### Arduino IDE Upload Failed
- **Cause**: Board/port not selected or library missing
- **Fix**:
  1. Select Board: Tools → Board → Arduino Uno
  2. Select Port: Tools → Port → /dev/ttyUSB0
  3. Install Adafruit library (see setup above)

---

## 📊 Command Examples

### Motor Controller

```python
# Speed control
motor_speed 9 200          # Pin 9 at speed 200/255

# Direction control
motor_direction 8 9 forward    # Pins 8 & 9, forward direction
motor_direction 8 9 backward   # Pins 8 & 9, backward direction

# Stop
motor_stop 9               # Stop pin 9
motor_stop 8 9             # Stop pins 8 and 9
```

### Servo Bonnet

```python
# Speed control
servo_speed 0 255          # Channel 0, full forward
servo_speed 0 -128         # Channel 0, half reverse
servo_speed 0 0            # Channel 0, stop

# Stop
servo_stop 0               # Stop channel 0
servo_stop_all             # Stop all channels
```

---

## 📝 Notes

- All sketches communicate at **9600 baud**
- Python scripts auto-detect Arduino if port not specified
- Always stop servos before disconnecting power
- For production use, consider adding capacitors to power supply (recommended: 100μF per servo)

---

## 🔗 Useful Links

- [Adafruit Servo Bonnet P3416](https://www.adafruit.com/product/3416)
- [Adafruit P154 Continuous Rotation Servo](https://www.adafruit.com/product/154)
- [Adafruit PWM Servo Driver Library](https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library)
- [Arduino Uno R3](https://store.arduino.cc/arduino-uno-rev3)
