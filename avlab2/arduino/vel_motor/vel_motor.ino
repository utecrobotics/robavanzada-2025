#include "vel_motor.h"

ros::NodeHandle nh;

void setup() {

  nh.initNode();
  
  nh.advertise(encoder);

  pinMode(ENC_IN_RIGHT_A , INPUT_PULLUP);
  pinMode(ENC_IN_RIGHT_B , INPUT);

  pinMode(PWM_M2A, OUTPUT);
  pinMode(PWM_M2B, OUTPUT);
  
  digitalWrite(PWM_M2A, LOW);       // MOTOR
  digitalWrite(PWM_M2B, LOW);

  attachInterrupt(digitalPinToInterrupt(ENC_IN_RIGHT_A), right_wheel_tick, RISING);
}

void loop() {

  unsigned long t = micros();

  if ((t - tTime[0]) >= (1000000 / ENCODER_FREQUENCY))
  {
    newtime_motor = micros();

    analogWrite(PWM_M2B, 255); // velocidad maxima del motor
    digitalWrite(PWM_M2A, LOW);

    delta_tiempo = 1.0/ENCODER_FREQUENCY;
    right_enc_w = (right_wheel_tick_count - last_right_wheel_tick_count)/delta_tiempo;
    right_w_msg.data = right_enc_w*(2.0*PI)/(7.0*60.0);  
    encoder.publish(&right_w_msg);

    // Reduccion = 60.0
    // Cuentas por revolucion = 7.0
    // Resolucion de 1.496 rad/s a una frecuencia de 100 Hz
    // Resolucion de 0.1496 rad/s a una frecuencia de 10 Hz

    last_right_wheel_tick_count = right_wheel_tick_count;
    
    oldtime_motor = newtime_motor;
    tTime[0] = t;
  }

  nh.spinOnce();
}


// Increment the number of ticks
void right_wheel_tick() {
   
  // Read the value for the encoder for the right wheel
  int val = digitalRead(ENC_IN_RIGHT_B);
 
  if(val == LOW) {
    right_wheel_tick_count++; 
  }
  else {
    right_wheel_tick_count--;
  }
   
}
