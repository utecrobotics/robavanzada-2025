void setup() {
  pinMode(LED_BUILTIN, OUTPUT);   // Built-in LED pin
  Serial.begin(9600);             // Start Serial communication at 9600 baud
}

void loop() {
  // Check if data is available to read from Serial
  if (Serial.available()) {
    char command = Serial.read();  // Read the incoming byte

    if (command == '1') {
      digitalWrite(LED_BUILTIN, HIGH);  // Turn LED on
    }
    else if (command == '0') {
      digitalWrite(LED_BUILTIN, LOW);   // Turn LED off
    }
  }
}