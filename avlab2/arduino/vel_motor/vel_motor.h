#include <ros.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32.h>

#define ENCODER_FREQUENCY                 10   //hz

#define PWM_M2A  10
#define PWM_M2B  11

#define ENC_IN_RIGHT_A 21
#define ENC_IN_RIGHT_B 20

unsigned long  oldtime_motor = 0;
unsigned long  newtime_motor;

float right_enc_w = 0.0;
float delta_tiempo = 0.0;

volatile int right_wheel_tick_count = 0;
volatile int last_right_wheel_tick_count = 0;

unsigned long tTime[4];


/********* Publishers *********/

std_msgs::Float32 right_w_msg;
ros::Publisher encoder("encoder", &right_w_msg);
