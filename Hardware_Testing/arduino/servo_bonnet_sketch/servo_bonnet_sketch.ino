// Adafruit Continuous Rotation Servo Controller
// For: Adafruit P154 Continuous Rotation Servos with Servo Bonnet P3416
// 
// SETUP:
// - Channel 0 servo connected to Servo Bonnet
// - External 5V power supply via buck converter
// - I2C: Arduino A4 (SDA), A5 (SCL)
// - Serial: 9600 baud
//
// Servo Control (Channel 0):
// - 0 degrees = BACKWARD
// - 90 degrees = STOP
// - 180 degrees = FORWARD

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
  Serial.println("Servo Bonnet Directional Controller");
  Serial.println("Channel 0 Connected");
  Serial.println("====================================");
  
  // Initialize I2C and PWM driver
  Wire.begin();
  pwm.begin();
  
  // Set PWM frequency to 50 Hz (standard servo frequency)
  pwm.setPWMFreq(SERVO_FREQ);
  
  // Initialize servo to STOP
  pwm.setPWM(0, 0, SERVOMID);
  
  Serial.println("\nServo initialized to STOP");
  Serial.println("\nCommands:");
  Serial.println("  forward   - Rotate forward (180 degrees)");
  Serial.println("  backward  - Rotate backward (0 degrees)");
  Serial.println("  stop      - Stop servo (90 degrees)");
  Serial.println("  speed N   - Set speed 0-90 (0=slow, 90=full)");
  Serial.println("====================================\n");
  
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toLowerCase();
    
    // Flash LED to show activity
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    
    // Parse and execute command
    if (command == "forward") {
      handleForward();
    }
    else if (command == "backward") {
      handleBackward();
    }
    else if (command == "stop") {
      handleStop();
    }
    else if (command.startsWith("speed")) {
      handleSpeed(command);
    }
    else if (command == "test") {
      runQuickTest();
    }
    else {
      Serial.print("Unknown command: ");
      Serial.println(command);
      Serial.println("Use: forward, backward, stop, speed N, or test");
    }
  }
}

void handleForward() {
  // Rotate forward (180 degrees)
  uint16_t pulseLength = map(180, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulseLength);
  Serial.println("Servo: FORWARD");
}

void handleBackward() {
  // Rotate backward (0 degrees)
  uint16_t pulseLength = map(0, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulseLength);
  Serial.println("Servo: BACKWARD");
}

void handleStop() {
  // Stop servo (90 degrees)
  pwm.setPWM(0, 0, SERVOMID);
  Serial.println("Servo: STOP");
}

void handleSpeed(String command) {
  // Format: speed N
  // N: 0-90, where 0 = slow, 90 = full forward
  
  int firstSpace = command.indexOf(' ');
  int speedPercent = command.substring(firstSpace + 1).toInt();
  
  if (speedPercent < 0 || speedPercent > 90) {
    Serial.println("Invalid speed: 0-90");
    return;
  }
  
  // Map speed to servo angle: 90 (stop) + speedPercent = forward direction
  int servoAngle = 90 + speedPercent;
  uint16_t pulseLength = map(servoAngle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulseLength);
  
  Serial.print("Servo speed: ");
  Serial.println(speedPercent);
}

void runQuickTest() {
  // Quick test: forward, backward, stop
  Serial.println("\n=== Quick Test ===");
  
  Serial.println("Testing FORWARD...");
  uint16_t pulseLength = map(180, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulseLength);
  delay(2000);
  
  Serial.println("Testing BACKWARD...");
  pulseLength = map(0, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulseLength);
  delay(2000);
  
  Serial.println("Stopping...");
  pwm.setPWM(0, 0, SERVOMID);
  
  Serial.println("=== Test Complete ===\n");
}

// Helper function to convert microseconds to PWM ticks
// NOTE: The Adafruit PWM driver setPWM() function expects the tick value directly
// The map() function already converts to the correct range (SERVOMIN-SERVOMAX)
uint16_t microsecondsToTicks(uint16_t microseconds) {
  // This function is kept for reference but is no longer used
  // At 50Hz PWM frequency, period = 20ms = 20000 microseconds
  // PCA9685 has 4096 ticks per period
  return (microseconds / 20000.0) * 4096;
}
