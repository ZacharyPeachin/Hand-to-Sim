// Voltage Check Test
// Measures voltage on analog pins to help debug power issues

void setup() {
  Serial.begin(9600);
  delay(100);
  
  Serial.println("\n\n====================================");
  Serial.println("VOLTAGE CHECK TEST");
  Serial.println("====================================\n");
  
  // Test multiple analog pins for voltage
  Serial.println("Reading analog pins...\n");
  
  // Read 5V reference (should be around 1023)
  int raw_5v = analogRead(A0);  // Connect to 5V for reference
  int raw_gnd = analogRead(A1); // Connect to GND for reference
  
  Serial.print("A0 (test 5V): ");
  Serial.println(raw_5v);
  Serial.print("A1 (test GND): ");
  Serial.println(raw_gnd);
  
  // Calculate voltage if using 5V reference
  float volt_5v = (raw_5v / 1023.0) * 5.0;
  float volt_gnd = (raw_gnd / 1023.0) * 5.0;
  
  Serial.print("\nEstimated voltage A0: ");
  Serial.print(volt_5v);
  Serial.println("V");
  Serial.print("Estimated voltage A1: ");
  Serial.print(volt_gnd);
  Serial.println("V");
  
  Serial.println("\n====================================");
  Serial.println("INSTRUCTIONS:");
  Serial.println("====================================");
  Serial.println("Before uploading:");
  Serial.println("1. Connect A0 wire to the 5V line from your power supply");
  Serial.println("2. Connect A1 wire to GND");
  Serial.println("3. Upload and run this sketch");
  Serial.println("");
  Serial.println("Expected results:");
  Serial.println("- A0 should read around 1023 (5V)");
  Serial.println("- A1 should read around 0 (0V)");
  Serial.println("");
  Serial.println("If A0 is LOW (< 500):");
  Serial.println("  → Your 5V power supply may not be working");
  Serial.println("  → Check power supply connection");
  Serial.println("  → Check Servo Bonnet power pins");
  Serial.println("====================================\n");
}

void loop() {
  delay(1000);
}
