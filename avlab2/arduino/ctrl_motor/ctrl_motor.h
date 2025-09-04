#define MOTOR_FREQUENCY                 1000   //hz

#define PWM_M2A  10
#define PWM_M2B  11

unsigned long  oldtime_motor = 0;
unsigned long  newtime_motor;

int motor_control = 0;

float input = 0;
float motor_err = 0;
float motor_ref = 0;
float enc_w = 0;

float last_input = 0;
float last_motor_err = 0;

unsigned long tTime[4];
