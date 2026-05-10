// Adafruit Continuous Rotation Servo Testing Sketch
// For: Adafruit P154 Continuous Rotation Servos with Servo Bonnet P3416
// 
// POWER REQUIREMENTS:
// - YES, you MUST use an external power supply!
// - The Servo Bonnet requires 5V external power (NOT just USB)
// - Connect GND from power supply to Arduino GND
// - Servo Bonnet draws more current than USB can provide
// - This prevents servo jitter and ensures proper operation
//
// PIN MAPPING (Servo Bonnet on Raspberry Pi or compatible I2C board)
// Uses I2C communication (SDA/SCL pins)
// For Arduino: Use SDA (A4) and SCL (A5) pins
//
// Servo Bonnet outputs: Channel 0-15 (16 servo channels)
// Continuous rotation servos use PWM:
// - 90 (1.5ms) = STOP
// - 0-89 = BACKWARD (increasing speed)
// - 91-180 = FORWARD (increasing speed)

#include <Wire.h>
#include "Adafruit_PWMServoDriver.h"

// Create PCA9685 object (default I2C address 0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo timing (in microseconds)
#define SERVOMIN  600   // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  2400  // This is the 'maximum' pulse length count (out of 4096)
#define SERVOMID  1500  // Center point (STOP for continuous rotation)

// PWM frequency
#define SERVO_FREQ 50 // 50 Hz

void setup() {
  Serial.begin(9600);
  delay(100);
  
  Serial.println("\n\n====================================");
  Serial.println("Adafruit Servo Bonnet Initialized");
  Serial.println("====================================");
  
  // Initialize I2C and PWM driver
  Wire.begin();
  pwm.begin();
  
  // Set PWM frequency to 50 Hz (standard servo frequency)
  pwm.setPWMFreq(SERVO_FREQ);
  
  // Initialize all servos to center (STOP)
  for (uint8_t i = 0; i < 16; i++) {
    pwm.setPWM(i, 0, microsecondsToTicks(SERVOMID));
    delay(50);
  }
  
  Serial.println("\nAll servos initialized to STOP position");
  Serial.println("External 5V power supply connected: YES (REQUIRED!)");
  Serial.println("\nCommands:");
  Serial.println("  servo_speed channel speed  (speed: -255 to 255, 0=stop)");
  Serial.println("  servo_stop channel");
  Serial.println("  servo_stop_all");
  Serial.println("====================================\n");
  
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    // Flash LED to show activity
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    
    // Parse and execute command
    if (command.startsWith("servo_speed")) {
      handleServoSpeed(command);
    }
    else if (command.startsWith("servo_stop_all")) {
      handleStopAll();
    }
    else if (command.startsWith("servo_stop")) {
      handleServoStop(command);
    }
    else if (command.startsWith("test")) {
      runQuickTest();
    }
    else {
      Serial.print("Unknown command: ");
      Serial.println(command);
      Serial.println("Use: servo_speed, servo_stop, servo_stop_all, or test");
    }
  }
}

void handleServoSpeed(String command) {
  // Format: servo_speed channel speed
  // channel: 0-15
  // speed: -255 (full reverse) to 255 (full forward), 0 = stop
  // Example: servo_speed 0 128  (channel 0, half forward speed)
  
  int firstSpace = command.indexOf(' ');
  int secondSpace = command.indexOf(' ', firstSpace + 1);
  
  uint8_t channel = command.substring(firstSpace + 1, secondSpace).toInt();
  int speed = command.substring(secondSpace + 1).toInt();
  
  // Validate channel
  if (channel > 15) {
    Serial.print("Invalid channel: ");
    Serial.println(channel);
    Serial.println("Valid channels: 0-15");
    return;
  }
  
  // Constrain speed
  speed = constrain(speed, -255, 255);
  
  // Convert speed to servo angle
  // For continuous rotation servos:
  // 90 = stop
  // < 90 = backward (90 - speed_range)
  // > 90 = forward (90 + speed_range)
  
  int servoValue;
  if (speed == 0) {
    servoValue = 90;  // Center = STOP
  }
  else if (speed > 0) {
    // Forward: map 1-255 to 91-180
    servoValue = 90 + (speed / 255.0) * 90;
  }
  else {
    // Backward: map -1 to -255 to 89-0
    servoValue = 90 + (speed / 255.0) * 90;  // This naturally goes backward
  }
  
  // Set servo
  uint16_t pulseLength = microsecondsToTicks(map(servoValue, 0, 180, SERVOMIN, SERVOMAX));
  pwm.setPWM(channel, 0, pulseLength);
  
  Serial.print("Channel ");
  Serial.print(channel);
  Serial.print(" speed: ");
  Serial.print(speed);
  Serial.print(" (servo value: ");
  Serial.print(servoValue);
  Serial.println(")");
}

void handleServoStop(String command) {
  // Format: servo_stop channel
  // Example: servo_stop 0
  
  int firstSpace = command.indexOf(' ');
  uint8_t channel = command.substring(firstSpace + 1).toInt();
  
  if (channel > 15) {
    Serial.print("Invalid channel: ");
    Serial.println(channel);
    return;
  }
  
  // Stop servo by setting to center (90 degrees = 1.5ms)
  pwm.setPWM(channel, 0, microsecondsToTicks(SERVOMID));
  
  Serial.print("Channel ");
  Serial.print(channel);
  Serial.println(" stopped");
}

void handleStopAll() {
  // Stop all servos
  for (uint8_t i = 0; i < 16; i++) {
    pwm.setPWM(i, 0, microsecondsToTicks(SERVOMID));
  }
  Serial.println("All servos stopped");
}

void runQuickTest() {
  // Quick test: cycle through all channels
  Serial.println("\n=== Quick Test: Cycling all channels ===");
  
  for (uint8_t i = 0; i < 16; i++) {
    Serial.print("Testing channel ");
    Serial.print(i);
    Serial.print("... FORWARD");
    
    // Move forward
    uint16_t pulseLength = microsecondsToTicks(map(135, 0, 180, SERVOMIN, SERVOMAX));
    pwm.setPWM(i, 0, pulseLength);
    delay(500);
    
    Serial.print(" -> BACKWARD");
    // Move backward
    pulseLength = microsecondsToTicks(map(45, 0, 180, SERVOMIN, SERVOMAX));
    pwm.setPWM(i, 0, pulseLength);
    delay(500);
    
    Serial.println(" -> STOP");
    // Stop
    pwm.setPWM(i, 0, microsecondsToTicks(SERVOMID));
    delay(200);
  }
  
  Serial.println("=== Test Complete ===\n");
}

// Helper function to convert microseconds to PWM ticks
uint16_t microsecondsToTicks(uint16_t microseconds) {
  // At 50Hz PWM frequency, period = 20ms = 20000 microseconds
  // PCA9685 has 4096 ticks per period
  return (microseconds / 20000.0) * 4096;
}
