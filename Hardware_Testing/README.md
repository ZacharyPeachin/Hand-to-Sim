# Hardware Testing

## Current Setup
- **Servo:** Adafruit P154 Continuous Rotation on Channel 0
- **Controller:** Adafruit Servo Bonnet P3416
- **Arduino:** Uno R3 (I2C: SDA/A4, SCL/A5)
- **Power:** 30V PSU + Buck Converter (5V output)

## Quick Test
```bash
python3 servo_test_bonnet.py /dev/ttyUSB0
```
Runs: **Forward 5s → Backward 5s → Stop**

## Arduino Sketches

Each sketch is in its own folder (open only ONE at a time in Arduino IDE):

### Servo Bonnet Controller
- **Folder:** `arduino/servo_bonnet_sketch/`
- **File:** `servo_bonnet_sketch.ino`
- **Commands:** `forward`, `backward`, `stop`, `speed N`, `test`
- **Angle:** 0° = backward, 90° = stop, 180° = forward

### Motor Controller
- **Folder:** `arduino/motor_controller_sketch/`
- **File:** `motor_controller_sketch.ino`
- **Commands:** `motor_speed`, `motor_direction`, `motor_stop`

### Basic Connectivity
- **Folder:** `arduino/basic_connectivity_sketch/`
- **File:** `basic_connectivity_sketch.ino`
- **Commands:** `ping`, `led_on`, `led_off`

## Python Test Scripts
- `servo_test_bonnet.py` - Servo directional test (5s forward/backward/stop)
- `motor_controller_test.py` - Motor controller test
- `arduino_ping.py` - Basic Arduino test

## Wiring
See `WIRING_GUIDE.md` for complete power/I2C setup

## File Structure
```
Hardware_Testing/
├── arduino/
│   ├── servo_bonnet_sketch/servo_bonnet_sketch.ino
│   ├── motor_controller_sketch/motor_controller_sketch.ino
│   └── basic_connectivity_sketch/basic_connectivity_sketch.ino
├── servo_test_bonnet.py
├── motor_controller_test.py
├── arduino_ping.py
├── README.md (this file)
└── WIRING_GUIDE.md
```
