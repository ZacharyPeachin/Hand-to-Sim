// I2C Pin Test - Check if A4 and A5 are responding
// This helps identify if the pins themselves are working

void setup() {
  Serial.begin(9600);
  delay(100);
  
  Serial.println("\n\n====================================");
  Serial.println("I2C PIN TEST");
  Serial.println("====================================\n");
  
  // Set A4 and A5 as inputs and read their state
pinMode(A4, INPUT_PULLUP);
pinMode(A5, INPUT_PULLUP);
  
  Serial.println("Testing I2C pin states...\n");
  
  for (int i = 0; i < 10; i++) {
    int sda_state = digitalRead(A4);
    int scl_state = digitalRead(A5);
    
    Serial.print("Read ");
    Serial.print(i + 1);
    Serial.print(": SDA(A4)=");
    Serial.print(sda_state);
    Serial.print("  SCL(A5)=");
    Serial.println(scl_state);
    
    delay(500);
  }
  
  Serial.println("\n====================================");
  Serial.println("Analysis:");
  Serial.println("  If SDA and SCL are both HIGH (1) most of the time:");
  Serial.println("    → Pull-up resistors are working (good!)");
  Serial.println("    → Problem is likely Servo Bonnet not responding");
  Serial.println("");
  Serial.println("  If SDA or SCL are stuck LOW (0):");
  Serial.println("    → Check for shorts or loose wires");
  Serial.println("    → Check if Servo Bonnet is powered");
  Serial.println("");
  Serial.println("  If they're toggling randomly:");
  Serial.println("    → I2C bus activity detected!");
  Serial.println("====================================\n");
}

void loop() {
  // Just do the test once in setup
  delay(1000);
}
