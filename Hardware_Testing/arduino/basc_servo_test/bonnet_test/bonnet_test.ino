#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_CHANNEL 0
#define STOP    310   // lowered from 370 — tune with +/- until servo stops
#define FORWARD 450
#define REVERSE 200

int currentPulse = STOP;

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);
  delay(500);

  Serial.println("======================");
  Serial.println("  Servo Control Boot  ");
  Serial.println("======================");

  Wire.begin();
  Wire.beginTransmission(0x40);
  byte err = Wire.endTransmission();
  if (err == 0) {
    Serial.println("PCA9685 found at 0x40 OK");
  } else {
    Serial.print("ERROR: PCA9685 not found, halting. Code: ");
    Serial.println(err);
    while (true) delay(1000);
  }

  pwm.begin();
  pwm.setPWMFreq(50);
  delay(100);

  // Set stop BEFORE servo powers up to prevent boot movement
  pwm.setPWM(SERVO_CHANNEL, 0, STOP);
  currentPulse = STOP;

  Serial.print("Boot pulse set to STOP=");
  Serial.println(STOP);
  Serial.println("If servo still moves on boot, use - to lower STOP value");
  Serial.println();
  Serial.println("f=forward  r=reverse  s=stop");
  Serial.println("+=increase pulse  -=decrease pulse");
  Serial.println("p=print values  q=set to stop");
  Serial.println("======================");
}

void setPulse(int pulse) {
  currentPulse = constrain(pulse, 100, 600);
  pwm.setPWM(SERVO_CHANNEL, 0, currentPulse);
  Serial.print("Pulse: ");
  Serial.print(currentPulse);
  if (currentPulse == STOP)    Serial.print(" [STOP]");
  if (currentPulse >= FORWARD) Serial.print(" [FULL FWD]");
  if (currentPulse <= REVERSE) Serial.print(" [FULL REV]");
  Serial.println();
}

void loop() {
  if (!Serial.available()) return;

  String input = Serial.readStringUntil('\n');
  input.trim();
  if (input.length() == 0) return;

  char cmd = input.charAt(0);
  Serial.print("CMD: "); Serial.println(cmd);

  switch (cmd) {
    case 'f': setPulse(FORWARD);           break;
    case 'r': setPulse(REVERSE);           break;
    case 's': setPulse(STOP);              break;
    case 'q': setPulse(STOP);              break;
    case '+': setPulse(currentPulse + 10); break;
    case '-': setPulse(currentPulse - 10); break;
    case 'p':
      Serial.print("Current="); Serial.print(currentPulse);
      Serial.print("  STOP="); Serial.print(STOP);
      Serial.print("  FWD="); Serial.print(FORWARD);
      Serial.print("  REV="); Serial.println(REVERSE);
      break;
    default:
      Serial.println("Unknown. Use f/r/s/+/-/p");
  }
}
