// I2C Diagnostic Sketch
// Scans for I2C devices and tests Servo Bonnet communication
// This helps identify wiring or communication issues

#include <Wire.h>
#include "Adafruit_PWMServoDriver.h"

// Try to create PCA9685 object (Servo Bonnet)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(9600);
  delay(100);
  
  Serial.println("\n\n====================================");
  Serial.println("I2C DIAGNOSTIC SKETCH");
  Serial.println("====================================\n");
  
  // Initialize I2C
  Wire.begin();
  Serial.println("I2C initialized on pins A4 (SDA), A5 (SCL)");
  
  // Scan for I2C devices
  Serial.println("\nScanning for I2C devices...");
  byte deviceCount = 0;
  
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("✓ Found device at address 0x");
      Serial.println(address, HEX);
      deviceCount++;
      
      // Check if this is the Servo Bonnet (should be at 0x40)
      if (address == 0x40) {
        Serial.println("  → This is the Servo Bonnet (PCA9685)!");
      }
    }
  }
  
  Serial.print("\nTotal devices found: ");
  Serial.println(deviceCount);
  
  if (deviceCount == 0) {
    Serial.println("\n✗ ERROR: No I2C devices found!");
    Serial.println("Troubleshooting:");
    Serial.println("  1. Check SDA (Arduino A4) ↔ Bonnet SDA connection");
    Serial.println("  2. Check SCL (Arduino A5) ↔ Bonnet SCL connection");
    Serial.println("  3. Check that Servo Bonnet is powered");
    Serial.println("  4. Try 4.7kΩ pull-up resistors on SDA/SCL");
    Serial.println("  5. Check for loose connectors");
  }
  
  // Try to initialize Servo Bonnet
  Serial.println("\n====================================");
  Serial.println("Attempting to initialize Servo Bonnet...");
  
  if (pwm.begin()) {
    Serial.println("✓ Servo Bonnet initialized successfully!");
    Serial.println("✓ I2C communication is working!");
    
    // Set frequency
    pwm.setPWMFreq(50);
    Serial.println("✓ PWM frequency set to 50 Hz");
    
    // Try to set a test pulse on channel 0
    Serial.println("\nTesting servo output on Channel 0...");
    pwm.setPWM(0, 0, 1500);  // Mid-point pulse
    Serial.println("✓ Pulse sent to Channel 0 (1500 ticks)");
    Serial.println("If servo doesn't move, check:");
    Serial.println("  1. Servo connector fully inserted in Channel 0");
    Serial.println("  2. Servo power connector (external 5V supply)");
    Serial.println("  3. Servo signal cable orientation");
    
  } else {
    Serial.println("✗ Failed to initialize Servo Bonnet!");
    Serial.println("Troubleshooting:");
    Serial.println("  1. Check I2C wiring (SDA/SCL)");
    Serial.println("  2. Verify Servo Bonnet is powered");
    Serial.println("  3. Check Servo Bonnet address with scanner above");
    Serial.println("  4. Try restarting Arduino and Servo Bonnet");
  }
  
  Serial.println("\n====================================");
  Serial.println("Commands for further testing:");
  Serial.println("  pulse <channel> <value>  - Send pulse to channel");
  Serial.println("  scan                      - Rescan I2C devices");
  Serial.println("====================================\n");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toLowerCase();
    
    if (command == "scan") {
      Serial.println("\nRescanning I2C devices...");
      byte deviceCount = 0;
      
      for (byte address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        byte error = Wire.endTransmission();
        
        if (error == 0) {
          Serial.print("✓ Found device at 0x");
          Serial.println(address, HEX);
          deviceCount++;
        }
      }
      
      Serial.print("Total: ");
      Serial.println(deviceCount);
    }
    else if (command.startsWith("pulse")) {
      // Format: pulse <channel> <value>
      int firstSpace = command.indexOf(' ');
      int secondSpace = command.indexOf(' ', firstSpace + 1);
      
      if (firstSpace > 0 && secondSpace > firstSpace) {
        int channel = command.substring(firstSpace + 1, secondSpace).toInt();
        int value = command.substring(secondSpace + 1).toInt();
        
        if (channel >= 0 && channel < 16 && value >= 0 && value <= 4095) {
          pwm.setPWM(channel, 0, value);
          Serial.print("Pulse sent to channel ");
          Serial.print(channel);
          Serial.print(": ");
          Serial.println(value);
        } else {
          Serial.println("Invalid parameters: channel (0-15), value (0-4095)");
        }
      } else {
        Serial.println("Format: pulse <channel> <value>");
      }
    }
    else {
      Serial.println("Unknown command");
    }
  }
}
