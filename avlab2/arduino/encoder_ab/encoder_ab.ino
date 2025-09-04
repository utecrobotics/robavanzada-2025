// Encoder output to Arduino Interrupt pin. Tracks the tick count.
#define ENC_IN_RIGHT_A 2
 
// Other encoder output to Arduino to keep track of wheel direction
// Tracks the direction of rotation.
#define ENC_IN_RIGHT_B 3
 
// True = Forward; False = Reverse
boolean Direction_right = true;
 
// Keep track of the number of wheel ticks
volatile int right_wheel_tick_count = 0;
 
// One-second interval for measurements
int interval = 1000;
long previousMillis = 0;
long currentMillis = 0;
 
void setup() {
 
  // Open the serial port at 9600 bps
  Serial.begin(9600); 
 
  // Set pin states of the encoder
  pinMode(ENC_IN_RIGHT_A , INPUT_PULLUP);
  pinMode(ENC_IN_RIGHT_B , INPUT);
 
  // Every time the pin goes high, this is a tick
  attachInterrupt(digitalPinToInterrupt(ENC_IN_RIGHT_A), right_wheel_tick, RISING);
}
 
void loop() {
 
  // Record the time
  currentMillis = millis();
 
  // If one second has passed, print the number of ticks
  if (currentMillis - previousMillis > interval) {
     
    previousMillis = currentMillis;
 
    Serial.println("Number of Ticks: ");
    Serial.println(right_wheel_tick_count);
    Serial.println();
  }
}
 
// Increment the number of ticks
void right_wheel_tick() {
   
  // Read the value for the encoder for the right wheel
  int val = digitalRead(ENC_IN_RIGHT_B);
 
  if(val == LOW) {
    right_wheel_tick_count--;  // Reverse
  }
  else {
    right_wheel_tick_count++;  // Forward
  }
}
