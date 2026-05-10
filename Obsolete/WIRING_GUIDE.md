# Complete Wiring Guide - Arduino + Servo Bonnet + Multiple Servos

## Your Hardware Summary
- Arduino Uno R3
- Adafruit Servo Bonnet P3416
- Multiple Adafruit P154 Continuous Rotation Servos (3-pin female connectors)
- External 30V power supply
- Buck converter (to step down to 5V for servos)
- Elegoo kit components

---

## ⚡ Power Supply Setup (IMPORTANT)

### Buck Converter Configuration
Since your power supply goes to 30V, use the buck converter:

1. **Buck Converter Input:**
   - V_in+ (positive) → PSU positive terminal
   - V_in- (negative) → PSU negative terminal

2. **Buck Converter Output (adjust to exactly 5.0V):**
   - V_out+ (positive) → Servo Bonnet VCC
   - V_out- (negative) → Common ground point

3. **Common Ground (CRITICAL):**
   - Buck V_out- → Arduino GND
   - Buck V_out- → Servo Bonnet GND
   - **All grounds must be connected together**

**Why the buck converter?** Your PSU is 30V but servos need 5V. The buck converter safely steps it down.

---

## 🔌 Wiring Diagram

```
┌─────────────────────────────────────────────────────────┐
│           External 30V Power Supply                      │
│         (+ terminal)  (- terminal/GND)                   │
│                │              │                          │
│                └──────┬──────┘                           │
│                       │                                   │
│              ┌────────▼────────┐                         │
│              │  Buck Converter │                         │
│              │   (set to 5V)   │                         │
│              │ V_in  V_out     │                         │
│              │  +  -  +  -     │                         │
│              └─┬─┬──┬─┬────────┘                         │
│                │ │  │ │                                  │
│         ┌──────┘ │  │ └─────┐                           │
│         │        │  │       │                            │
│    ┌────▼────────▼──▼───────▼────┐                      │
│    │    Servo Bonnet P3416        │                      │
│    │  VCC    GND    SDA    SCL    │                      │
│    │   ↑      ↑      │      │     │                      │
│    │   │      │      └──────┼─────┼──→ To Arduino       │
│    │   │      │             │     │    SDA (A4)         │
│    │   │      │             └─────┼──→ To Arduino       │
│    │   │      │                   │    SCL (A5)         │
│    │   └──────┴───────────────────┤                      │
│    │  Channels 0-15               │                      │
│    │  Ch0  Ch1  Ch2 ... Ch15      │                      │
│    └───┬────┬────┬───────┬────────┘                      │
│        │    │    │       │                               │
│     ┌──▼─┐┌──▼─┐┌──▼─┐ ┌──▼─┐                          │
│     │Srv1││Srv2││Srv3│ │Srv4│  (can have up to 16)     │
│     └────┘└────┘└────┘ └────┘                           │
│                                                          │
│    Arduino Uno R3                                        │
│    ┌──────────────────────────┐                         │
│    │ GND    SDA    SCL        │                         │
│    │  ↑      ↑      ↑         │                         │
│    │  │      │      │         │                         │
│    │  └──────┴──────┴─────────┤ (I2C communication)    │
│    │  USB (to laptop)         │                         │
│    └──────────────────────────┘                         │
│                                                          │
│ Common Ground Point (star connection):                   │
│   ├─ Arduino GND                                         │
│   ├─ Servo Bonnet GND                                    │
│   ├─ Buck Converter V_out- (-)                           │
│   └─ PSU negative terminal                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Step-by-Step Wiring

### Step 1: Power Supply to Buck Converter
- PSU positive (red) → Buck V_in+
- PSU negative (black) → Buck V_in-

### Step 2: Buck Converter to Servo Bonnet
- Buck V_out+ (red) → Servo Bonnet VCC (usually top-left pin labeled VCC)
- Buck V_out- (black) → Servo Bonnet GND

### Step 3: Servo Bonnet to Arduino (I2C Communication)
- Servo Bonnet SDA → Arduino A4 (SDA)
- Servo Bonnet SCL → Arduino A5 (SCL)
- Servo Bonnet GND → Arduino GND (common ground)

### Step 4: Arduino Power
- USB cable to laptop (provides 5V power to Arduino)

### Step 5: Servos to Servo Bonnet
For each servo you want to use:
- Servo 3-pin connector → Servo Bonnet channel (0-15)
  - Signal (yellow/orange) → Signal pin (middle)
  - Power (red) → Power pin (top)
  - Ground (black) → Ground pin (bottom)

**Note:** Channel 0 is on the left, channels go up to 15 on the right

### Step 6: Common Ground Connection
Connect all grounds together at one point:
- Arduino GND
- Servo Bonnet GND
- Buck Converter V_out- (negative output)
- PSU negative terminal

Use a breadboard or solder them together to ensure solid connection.

---

## 🎯 Servo Bonnet Channel Map

```
Left side (looking at bonnet):        Right side:
Ch15 Ch14 Ch13 Ch12 Ch11 Ch10        Ch09 Ch08 Ch07 Ch06 Ch05 Ch04 Ch03 Ch02 Ch01 Ch00
```

Connect your servos to any channels (0-15). The test script will let you specify which channel each servo is on.

---

## ⚙️ Arduino Pin Reference

You'll need these connections:
- **A4 (SDA)** - I2C data line (to Servo Bonnet)
- **A5 (SCL)** - I2C clock line (to Servo Bonnet)
- **GND** - Ground (common ground point)
- **USB** - Power + data to/from laptop

---

## 🧪 Testing Your Setup

### 1. Upload the sketch:
```
Hardware_Testing/arduino_sketch/adafruit_servo_bonnet_sketch.ino
```

### 2. Run the Python test:
```bash
python3 Hardware_Testing/servo_test_bonnet.py /dev/ttyUSB0
```

### 3. Test commands:
```
servo_speed 0 255      # Channel 0 full forward
servo_speed 0 -255     # Channel 0 full backward
servo_speed 0 0        # Channel 0 stop
servo_stop_all         # All stop
```

---

## ⚠️ Troubleshooting Checklist

- [ ] Buck converter set to exactly 5.0V (use multimeter)
- [ ] All ground wires connected together (common ground point)
- [ ] Arduino GND connected to Servo Bonnet GND
- [ ] Servo Bonnet VCC (red) only comes from buck converter
- [ ] Arduino powered only by USB
- [ ] I2C wires (SDA/SCL) are secure
- [ ] Servo connectors fully inserted into bonnet
- [ ] No loose wires touching each other

---

## 💡 Tips

- Use the soldering iron to create a solid common ground point if using breadboard is unreliable
- Keep servo wires short and away from moving parts
- Label each servo connector with its channel number
- Test with one servo first before adding more
- If servos jitter, check your ground connections (99% of servo problems are ground issues)

---

## 📊 Power Budget

Your setup can handle:
- 16 servos × 700mA each = 11.2A max
- Your PSU provides "plenty of amps" through the buck converter
- You're good to go!
