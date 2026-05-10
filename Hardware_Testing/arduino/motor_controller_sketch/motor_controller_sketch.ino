// Motor Controller Testing Sketch
// Supports L298N, TB6612FNG, and similar motor controllers
// Communication protocol: motor_speed pin speed_value
//                        motor_direction pin1 pin2 direction
//                        motor_stop pin1 [pin2]

const int MAX_SPEED = 255;
const int MIN_SPEED = 0;

void setup() {
  Serial.begin(9600);
  
  // Initialize all possible motor control pins as OUTPUT
  // Adjust pin numbers based on your motor controller connections
  for (int i = 2; i <= 13; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Motor Controller initialized!");
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
    if (command.startsWith("motor_speed")) {
      handleMotorSpeed(command);
    } 
    else if (command.startsWith("motor_direction")) {
      handleMotorDirection(command);
    } 
    else if (command.startsWith("motor_stop")) {
      handleMotorStop(command);
    }
    else {
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

void handleMotorSpeed(String command) {
  // Format: motor_speed pin speed_value
  // Example: motor_speed 9 128
  
  int firstSpace = command.indexOf(' ');
  int secondSpace = command.indexOf(' ', firstSpace + 1);
  
  int pin = command.substring(firstSpace + 1, secondSpace).toInt();
  int speed = command.substring(secondSpace + 1).toInt();
  
  // Constrain speed to valid range
  speed = constrain(speed, MIN_SPEED, MAX_SPEED);
  
  // Check if pin is valid
  if (pin < 2 || pin > 13) {
    Serial.print("Invalid pin: ");
    Serial.println(pin);
    return;
  }
  
  // Set PWM
  analogWrite(pin, speed);
  
  Serial.print("Motor speed set - Pin: ");
  Serial.print(pin);
  Serial.print(", Speed: ");
  Serial.println(speed);
}

void handleMotorDirection(String command) {
  // Format: motor_direction pin1 pin2 direction
  // Example: motor_direction 8 9 forward
  
  int firstSpace = command.indexOf(' ');
  int secondSpace = command.indexOf(' ', firstSpace + 1);
  int thirdSpace = command.indexOf(' ', secondSpace + 1);
  
  int pin1 = command.substring(firstSpace + 1, secondSpace).toInt();
  int pin2 = command.substring(secondSpace + 1, thirdSpace).toInt();
  String direction = command.substring(thirdSpace + 1);
  direction.toLowerCase();
  
  // Validate pins
  if (pin1 < 2 || pin1 > 13 || pin2 < 2 || pin2 > 13) {
    Serial.print("Invalid pins: ");
    Serial.print(pin1);
    Serial.print(", ");
    Serial.println(pin2);
    return;
  }
  
  // Set direction
  if (direction == "forward") {
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    Serial.println("Motor direction: FORWARD");
  } 
  else if (direction == "backward") {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
    Serial.println("Motor direction: BACKWARD");
  }
  else {
    Serial.print("Invalid direction: ");
    Serial.println(direction);
  }
}

void handleMotorStop(String command) {
  // Format: motor_stop pin1 [pin2]
  // Example: motor_stop 9
  // Example: motor_stop 8 9
  
  int firstSpace = command.indexOf(' ');
  int secondSpace = command.indexOf(' ', firstSpace + 1);
  
  int pin1 = command.substring(firstSpace + 1, secondSpace > 0 ? secondSpace : command.length()).toInt();
  
  // Validate pin
  if (pin1 < 2 || pin1 > 13) {
    Serial.print("Invalid pin: ");
    Serial.println(pin1);
    return;
  }
  
  // Stop motor
  analogWrite(pin1, 0);
  digitalWrite(pin1, LOW);
  
  // If second pin provided, stop it too
  if (secondSpace > 0) {
    int pin2 = command.substring(secondSpace + 1).toInt();
    if (pin2 >= 2 && pin2 <= 13) {
      analogWrite(pin2, 0);
      digitalWrite(pin2, LOW);
    }
  }
  
  Serial.println("Motor stopped");
}
