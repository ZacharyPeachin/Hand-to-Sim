# Complete Hardware Testing Guide

## 📦 Your Hardware
- **Arduino**: Uno R3 (with USB connection)
- **Servos**: Adafruit P154 Continuous Rotation Servos
- **Controller**: Adafruit Servo Bonnet P3416
- **Power**: External 5V power supply (REQUIRED)

---

## ⚡ POWER SETUP (Critical!)

### Why You NEED External Power

```
Your Setup:
  USB (500mA max) ──→ Arduino only
  External PSU (2A+) ──→ Servo Bonnet ──→ Servos (700mA+ each)
```

**The Servo Bonnet's PCA9685 chip requires dedicated power for servo control.**

### Physical Connection

```
┌─────────────────────┐
│ 5V Power Supply     │
│ ┌─────────────────┐ │
│ │ +5V    GND      │ │
│ └────┬──────┬─────┘ │
└──────┼──────┼───────┘
       │      │
       │      ├─────────────┐
       │      │             │
       │   ┌──┴──┐     ┌────┴──┐
       │   │ GND │     │ GND   │
       │   │     │     │       │
    ┌──┴───┤ B   │ ┌───┤ A    │
    │      │ o   │ │   │      │
    │      │ a   │ │   │      │
    │      │ r   │ │   │      │
    │      │ d   │ │   │      │
    │      └─────┘ │   │ VCC  │
    │              │   │      │
    └──────────────┴───┤ SER  │
   External PSU        │ VO   │
   (5V, GND)           │ BON  │
                       │ NET  │
                       └──┬───┘
                          │
                 ┌────────┴────────┐
                 │   Servo Bonnet  │
                 │   Channels 0-15 │
                 │                 │
                 │ Ch0 Ch1 ... Ch15│
                 └────┬──┬────┬────┘
                      │  │    │
                  [Servo] [Servo] ...
```

### Connection Checklist

- [ ] External 5V power supply available
- [ ] Arduino connected to laptop via USB
- [ ] Servo Bonnet attached to Arduino (stacked on top)
- [ ] GND jumper wire from PSU → Arduino GND
- [ ] GND jumper wire from PSU → Servo Bonnet GND
- [ ] +5V wire from PSU → Servo Bonnet VCC
- [ ] Servo connectors plugged into Servo Bonnet channels
- [ ] **NO direct connection from PSU to Arduino**

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Install Arduino Library
1. Open Arduino IDE
2. Sketch → Include Library → Manage Libraries
3. Search: "Adafruit PWM Servo Driver"
4. Install (by Adafruit)

### Step 2: Upload Firmware
1. File → Open → `Hardware_Testing/arduino_sketch/adafruit_servo_bonnet_sketch.ino`
2. Tools → Board → Arduino Uno
3. Tools → Port → /dev/ttyUSB0 (or your port)
4. Sketch → Upload

### Step 3: Connect Hardware
1. Connect all GND wires first (PSU → Arduino → Servo Bonnet)
2. Connect +5V from PSU to Servo Bonnet VCC
3. Plug servos into Servo Bonnet channels
4. Turn ON external 5V power supply
5. Arduino should respond with startup message

### Step 4: Test
```bash
python3 Hardware_Testing/servo_test_bonnet.py /dev/ttyUSB0
```

Should see smooth servo rotation in both directions!

---

## 🎮 Controlling Servos

### Command Format
```
servo_speed channel speed
```

### Speed Reference
| Value | Motion | Use Case |
|-------|--------|----------|
| 255 | Full forward fast | Maximum speed forward |
| 200 | Forward fast | Fast forward |
| 128 | Forward medium | Medium speed forward |
| 64 | Forward slow | Slow forward |
| 0 | **STOP** | Hold position |
| -64 | Backward slow | Slow backward |
| -128 | Backward medium | Medium backward |
| -200 | Backward fast | Fast backward |
| -255 | Full backward fast | Maximum speed backward |

### Example Commands
```bash
# Channel 0, full forward
servo_speed 0 255

# Channel 0, slow forward
servo_speed 0 64

# Channel 0, stop
servo_speed 0 0

# Channel 0, full reverse
servo_speed 0 -255

# All channels stop
servo_stop_all
```

---

## 📝 File Organization

### Arduino Sketches (All in one place)
```
Hardware_Testing/arduino_sketch/
├── adafruit_servo_bonnet_sketch.ino    ← Use this for servos
├── motor_controller_sketch.ino         (For motor controllers)
└── arduino_sketch.ino                  (Basic test)
```

### Python Test Scripts
```
Hardware_Testing/
├── servo_test_bonnet.py                ← Use this for testing
├── motor_controller_test.py            (For motor controllers)
└── arduino_ping.py                     (Basic connectivity)
```

### Documentation
```
/
├── SETUP_SUMMARY.md                    ← Quick reference
├── SERVO_BONNET_POWER_SETUP.md         ← Detailed power guide
└── Hardware_Testing/README.md          ← Complete reference
```

---

## 🧪 Running Tests

### Basic Servo Test
```bash
cd /home/zachary/Hand-to-Sim
python3 Hardware_Testing/servo_test_bonnet.py
```

Auto-detects Arduino port and runs test suite:
1. Speed range test (all speeds from -255 to 255)
2. Continuous rotation test (forward/backward)
3. Speed ramp test (gradual acceleration)

### Test With Specific Port
```bash
python3 Hardware_Testing/servo_test_bonnet.py /dev/ttyUSB0
```

### Motor Controller Test
```bash
python3 Hardware_Testing/motor_controller_test.py /dev/ttyUSB0
```

### Basic Ping Test
```bash
python3 Hardware_Testing/arduino_ping.py /dev/ttyUSB0
```

---

## 🔧 Troubleshooting

### Issue: Servo doesn't move
**Check:**
1. External power supply ON?
2. GND connections made?
3. Servo plugged into Servo Bonnet?
4. Arduino IDE shows successful upload?

**Fix:**
```bash
# Send test command in Arduino IDE Serial Monitor
test
```

### Issue: Servo jitters/vibrates
**Cause:** Insufficient power
**Fix:** Use higher current PSU (3A+) or remove servos

### Issue: Arduino resets repeatedly
**Cause:** Power glitch
**Fix:** 
1. Turn off PSU
2. Check all connections
3. Verify PSU voltage (should be 5.0V)

### Issue: Can't find Arduino port
```bash
# List all serial ports
ls /dev/tty*

# Try common ports:
# /dev/ttyUSB0
# /dev/ttyACM0
# /dev/ttyUSB1
# /dev/ttyACM1
```

### Issue: "Permission denied" on serial port
```bash
sudo usermod -a -G dialout $USER
# Then log out and log back in
```

---

## 📊 Power Supply Calculator

```
Number of Servos × Current per Servo = Total Current Needed
      N          ×      700mA        =    700N mA

Examples:
1 servo  × 700mA = 700mA  → Need 1A+ PSU ✓
2 servos × 700mA = 1.4A  → Need 2A+ PSU ✓
3 servos × 700mA = 2.1A  → Need 3A+ PSU ✓
4 servos × 700mA = 2.8A  → Need 3A+ PSU ✓
```

**Recommendation:** Get 3A+ PSU to safely handle multiple servos

---

## 🔌 Wiring Reference

### Servo Bonnet to Arduino
```
SDA (pin 20) ──→ SDA
SCL (pin 21) ──→ SCL
GND          ──→ GND
```

### Servo Bonnet to Power Supply
```
VCC (red)  ──→ +5V
GND (blk)  ──→ GND
```

### Arduino to Power Supply
```
GND (only) ──→ GND (common ground)
```

---

## ✅ Verification Checklist

- [ ] Arduino library installed (Adafruit PWM Servo Driver)
- [ ] Sketch uploaded successfully
- [ ] GND connections verified
- [ ] +5V connection verified (to Servo Bonnet, NOT Arduino)
- [ ] Servo connectors secured
- [ ] Power supply tested (should show 5.0V)
- [ ] Arduino responds to test command
- [ ] Servos move smoothly without jitter
- [ ] Speed control responsive

---

## 🎓 Learning Resources

- **Adafruit Servo Bonnet**: https://www.adafruit.com/product/3416
- **P154 Continuous Rotation Servo**: https://www.adafruit.com/product/154
- **PWMServoDriver Library**: https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library

---

## 📞 Emergency Stop

If anything goes wrong:
1. **Turn OFF the external power supply immediately**
2. Disconnect USB from Arduino
3. Wait 30 seconds
4. Inspect all connections for shorts
5. Verify power supply voltage with multimeter
6. Only reconnect when confident in your setup

---

## 🎉 You're All Set!

Your hardware testing suite is ready. Remember:
- **External power is NOT optional**
- Servos need stable 5V power
- Always check connections before powering on
- Start with a single servo to verify setup

Happy testing! 🚀
