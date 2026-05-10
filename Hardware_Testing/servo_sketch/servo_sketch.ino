// Servo Testing Sketch
// Control servo motors via serial commands
// Requires: Servo library (included in Arduino IDE)
// Communication protocol: servo_angle pin angle

#include <Servo.h>

// Create servo object
Servo myServo;

// Default servo pin (can be any PWM pin)
const int DEFAULT_SERVO_PIN = 3;

// Servo angle limits
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

void setup() {
  Serial.begin(9600);
  
  // Initialize LED
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Attach servo to default pin
  myServo.attach(DEFAULT_SERVO_PIN);
  
  // Move to center position
  myServo.write(90);
  
  Serial.println("Servo Controller initialized!");
  Serial.print("Servo attached to pin: ");
  Serial.println(DEFAULT_SERVO_PIN);
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
    if (command.startsWith("servo_angle")) {
      handleServoAngle(command);
    }
    else {
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

void handleServoAngle(String command) {
  // Format: servo_angle pin angle
  // Example: servo_angle 3 90
  
  int firstSpace = command.indexOf(' ');
  int secondSpace = command.indexOf(' ', firstSpace + 1);
  
  int pin = command.substring(firstSpace + 1, secondSpace).toInt();
  int angle = command.substring(secondSpace + 1).toInt();
  
  // Constrain angle to valid range
  angle = constrain(angle, MIN_ANGLE, MAX_ANGLE);
  
  // Check if pin is valid (PWM pins: 3, 5, 6, 9, 10, 11)
  if (pin != 3 && pin != 5 && pin != 6 && pin != 9 && pin != 10 && pin != 11) {
    Serial.print("Invalid PWM pin: ");
    Serial.println(pin);
    return;
  }
  
  // Reattach servo if different pin
  if (pin != DEFAULT_SERVO_PIN) {
    myServo.detach();
    myServo.attach(pin);
    Serial.print("Servo reattached to pin: ");
    Serial.println(pin);
  }
  
  // Set servo angle
  myServo.write(angle);
  
  Serial.print("Servo angle set - Pin: ");
  Serial.print(pin);
  Serial.print(", Angle: ");
  Serial.println(angle);
}
