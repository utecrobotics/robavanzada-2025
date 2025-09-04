#include "ctrl_motor.h"

void setup() {

  pinMode(PWM_M2A, OUTPUT);
  pinMode(PWM_M2B, OUTPUT);
  
  digitalWrite(PWM_M2A, LOW);       // MOTOR
  digitalWrite(PWM_M2B, LOW);
}

void loop() {

  unsigned long t = micros();

  if ((t - tTime[0]) >= (1000000 / MOTOR_FREQUENCY))
  {
    newtime_motor = micros();

    motor_control = 0;
    //right_motor_err = right_motor_ref - right_enc_w;
  
    if (motor_control == 0) {
      digitalWrite(PWM_M2B, LOW);
      digitalWrite(PWM_M2A, LOW);
    }
    else if (motor_control > 0 and motor_control <= 255) {
      analogWrite(PWM_M2B, motor_control);
      digitalWrite(PWM_M2A, LOW);
    }
    else if (motor_control > 255) {
      digitalWrite(PWM_M2B, HIGH);
      digitalWrite(PWM_M2A, LOW);
    }
    else if (motor_control < 0 and motor_control >= -255) {
      digitalWrite(PWM_M2B, LOW);
      analogWrite(PWM_M2A, motor_control*(-1));
    }
    else if (motor_control < -255) {
      digitalWrite(PWM_M2B, LOW);
      digitalWrite(PWM_M2A, HIGH);
    }

    //last_motor_err = motor_err;    
    oldtime_motor = newtime_motor;
    tTime[0] = t;
  }
}
