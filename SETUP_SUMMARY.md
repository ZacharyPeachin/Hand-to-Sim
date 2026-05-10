# Hardware Testing Suite - Organization Summary

## ✅ What Has Been Reorganized

All Arduino sketches are now centralized in the `arduino_sketch` folder:

```
Hardware_Testing/
├── arduino_sketch/                          ← All sketches here
│   ├── arduino_sketch.ino                   (Basic connectivity test)
│   ├── motor_controller_sketch.ino          (Motor controller support)
│   └── adafruit_servo_bonnet_sketch.ino     (Servo bonnet I2C control)
│
├── arduino_ping.py                          (Python: Basic test)
├── motor_controller_test.py                 (Python: Motor control)
├── servo_test_bonnet.py                     (Python: Servo bonnet)
└── README.md                                (Complete documentation)

SERVO_BONNET_POWER_SETUP.md                  (Power guide at root)
```

---

## 🔌 About Your Adafruit Servo Setup

You have:
- **Adafruit P154 Continuous Rotation Servos**
- **Adafruit Servo Bonnet P3416** (I2C-based PWM controller)

### External Power Supply: YES, REQUIRED

Your Servo Bonnet communicates with Arduino via I2C (SDA/SCL pins), but **requires a separate 5V power supply** for servo control.

**Why?**
- Continuous rotation servos draw 700mA+ under load
- USB (500mA max) cannot power even one servo
- Power supply powers the servos only, not the Arduino

**Setup:**
1. Connect external 5V PSU GND to Arduino GND (common ground)
2. Connect external 5V PSU +5V to Servo Bonnet VCC
3. Connect USB to Arduino (Arduino power + data)
4. Connect servos to Servo Bonnet channels (0-15)

See: `SERVO_BONNET_POWER_SETUP.md` for detailed wiring

---

## 🚀 Quick Start

### 1. Upload Arduino Sketch
```bash
# In Arduino IDE:
# - File > Open > Hardware_Testing/arduino_sketch/adafruit_servo_bonnet_sketch.ino
# - Tools > Board > Arduino Uno
# - Tools > Port > /dev/ttyUSB0 (or your port)
# - Upload
```

### 2. Connect Power
```
External 5V PSU:
  ├─ GND → Arduino GND
  ├─ GND → Servo Bonnet GND
  └─ +5V → Servo Bonnet VCC

USB:
  └─ → Arduino (USB port)

Servos:
  └─ → Servo Bonnet Channels (0-15)
```

### 3. Test Servos
```bash
cd /home/zachary/Hand-to-Sim
python3 Hardware_Testing/servo_test_bonnet.py /dev/ttyUSB0
```

---

## 📋 Hardware Files

### Motor Controller
- **Sketch**: `arduino_sketch/motor_controller_sketch.ino`
- **Test**: `motor_controller_test.py`
- **Supports**: L298N, TB6612FNG, etc.

### Servo Bonnet (Your Setup)
- **Sketch**: `arduino_sketch/adafruit_servo_bonnet_sketch.ino`
- **Test**: `servo_test_bonnet.py`
- **Servos**: Adafruit P154 Continuous Rotation
- **Channels**: 16 (0-15)
- **Power**: External 5V required

### Basic Connectivity
- **Sketch**: `arduino_sketch/arduino_sketch.ino`
- **Test**: `arduino_ping.py`

---

## ⚡ Power Supply Reference

**Minimum Specs:**
- 5V DC output
- 2A continuous
- Stable, regulated output

**Recommended Purchases:**
- Lab bench power supply (5V, 3A+)
- Quality USB-C 5V/2A power adapter
- 5V power bank (marked 2A+)

**NOT Recommended:**
- USB hubs (low current)
- Phone chargers < 2A
- Unregulated supplies

---

## 🔧 Servo Control Commands

```bash
# Start a servo
servo_speed 0 255          # Channel 0, full forward

# Slow down
servo_speed 0 128          # Channel 0, half speed

# Stop
servo_speed 0 0            # Channel 0, stop

# Reverse
servo_speed 0 -255         # Channel 0, full reverse

# Stop all
servo_stop_all             # Stop all channels
```

---

## 📂 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Arduino Sketches | `Hardware_Testing/arduino_sketch/` | Upload to Arduino |
| Python Tests | `Hardware_Testing/*.py` | Run on laptop |
| Documentation | `README.md` | Full details |
| Power Guide | `SERVO_BONNET_POWER_SETUP.md` | Power setup |

---

## ✨ You're Ready!

1. ✅ All sketches organized in `arduino_sketch/`
2. ✅ Adafruit servo bonnet sketch created (with I2C support)
3. ✅ Python test script for servo bonnet ready
4. ✅ Power requirements documented
5. ✅ Motor controller support included
6. ✅ Auto-detection of Arduino port

**Next step:** Get your external 5V power supply and follow the power setup guide!

---

## 📞 Troubleshooting

See `Hardware_Testing/README.md` for:
- Connection diagrams
- Troubleshooting guides
- Command references
- Testing procedures
