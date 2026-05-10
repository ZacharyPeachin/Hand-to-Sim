// Arduino Uno R3 Serial Communication Sketch
// This sketch listens for serial messages and responds

void setup() {
  // Initialize serial communication at 9600 baud
  Serial.begin(9600);
  
  // Initialize built-in LED (pin 13)
  pinMode(13, OUTPUT);
  
  // Send a startup message
  Serial.println("Arduino is ready!");
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte
    String incoming = Serial.readStringUntil('\n');
    incoming.trim();
    
    // Echo the message back
    Serial.print("Received: ");
    Serial.println(incoming);
    
    // Flash the LED to show activity
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    
    // Respond to specific commands
    if (incoming == "ping") {
      Serial.println("pong");
    } else if (incoming == "led_on") {
      digitalWrite(13, HIGH);
      Serial.println("LED is ON");
    } else if (incoming == "led_off") {
      digitalWrite(13, LOW);
      Serial.println("LED is OFF");
    }
  }
}
