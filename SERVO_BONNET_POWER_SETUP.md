# Adafruit Servo Bonnet Power Supply Guide

## ⚠️ CRITICAL: External Power Required

Your Adafruit Servo Bonnet P3416 with P154 Continuous Rotation Servos **REQUIRES** an external 5V power supply. This is not optional.

## Why External Power?

- **USB Power Limitation**: USB provides max 500mA
- **Servo Current Draw**: Each servo draws up to 700mA under load
- **Bonnet Controller**: The PCA9685 chip draws additional current
- **Result Without External Power**: 
  - Servo jitter and erratic behavior
  - Overheating
  - Arduino resets
  - Servo failure

## Power Supply Specifications

**Required:**
- 5V DC output (±5%)
- 2A minimum (3A+ recommended for multiple servos)
- Good quality with stable output

**Options:**
1. **Lab Power Supply** (Recommended)
   - Set to 5V, 2-3A
   - Most stable and reliable
   
2. **USB Power Adapter**
   - 5V/2A rated adapter
   - Works well for testing
   
3. **Battery-Powered Option**
   - 5V power bank (marked as 2A or higher)
   - Good for portable testing

## Connection Steps

### 1. Disconnect Everything First
- Disconnect USB from Arduino
- Remove servo bonnet from Arduino
- Remove any servo connections

### 2. Connect Ground (GND) First
**This is the most important step!**
```
External PSU GND (black) ──→ Arduino GND pin
External PSU GND (black) ──→ Servo Bonnet GND pin
```

### 3. Connect Power
```
External PSU +5V (red) ──→ Servo Bonnet VCC pin
```

**DO NOT connect external PSU +5V to Arduino!**
USB will provide Arduino power.

### 4. Plug in USB
Connect Arduino to laptop via USB (data + Arduino power)

### 5. Connect External PSU
Turn on external power supply

### 6. Verify
- Arduino LED should light up
- No error messages on serial
- Servos should respond smoothly to commands

## Wiring Diagram

```
┌─────────────────────────────────────────────┐
│         External 5V Power Supply            │
│         ┌─────────────────────┐             │
│         │  +5V (red)  GND (blk)│             │
│         └────┬──────────┬──────┘             │
│              │          │                    │
│         ┌────▼──────────▼──────┐             │
│         │  Servo Bonnet P3416  │             │
│         │  VCC    GND          │             │
│         └────┬──────────┬──────┘             │
│              │          │                    │
│   ┌──────────┘          │                    │
│   │ ┌──────────────────────┐                 │
│   └─┤ Arduino Uno R3       │                 │
│     │ GND (share common)   │                 │
│     │                      │                 │
│     │ USB (to laptop) ────►│                 │
│     └──────────────────────┘                 │
│                                              │
│     Servo 0 ──→ Channel 0                    │
│     Servo 1 ──→ Channel 1                    │
│     ... (up to 16 servos)                    │
└─────────────────────────────────────────────┘
```

## Quick Checklist

- [ ] External 5V power supply available and tested
- [ ] GND wires connected first (before +5V)
- [ ] Arduino GND connected to power supply GND
- [ ] Servo Bonnet GND connected to power supply GND
- [ ] Servo Bonnet VCC connected to power supply +5V
- [ ] USB connected to Arduino (but NOT to Servo Bonnet)
- [ ] All servo connectors secure
- [ ] No loose wires or shorts visible

## Testing

Once connected, run:
```bash
python3 servo_test_bonnet.py /dev/ttyUSB0
```

You should see:
- Servos respond to commands immediately
- Smooth motion without jitter
- No Arduino resets or errors
- Servos holding position when stopped

## Troubleshooting

**Symptom: Servo jitter or erratic behavior**
- Check: Is external power supply ON?
- Check: Are GND wires connected?
- Check: Is power supply providing 5V?

**Symptom: Arduino resets repeatedly**
- Cause: Power supply under-current
- Fix: Use higher current PSU (3A+) or remove extra servos

**Symptom: Some servos work, others don't**
- Check: All servo connectors fully inserted
- Check: Power supply can handle all servos

**Symptom: Servo very slow to respond**
- Check: Power supply voltage (should be exactly 5V)
- Check: Power supply current sufficient

## Emergency Stop

If anything seems wrong:
1. Turn OFF external power supply immediately
2. Disconnect USB from Arduino
3. Check all connections for shorts
4. Wait 30 seconds before retrying

## Additional Notes

- Capacitors (100μF) across power supply lines help stabilize voltage
- Keep wires short and away from moving parts
- Label your cables for future reference
- Never hot-swap servo connections while powered
- Always have emergency stop easily accessible
