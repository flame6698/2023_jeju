//ultraSonicSensor
#include &lt;ros.h&gt;
//#include &lt;geometry_msgs/Twist.h&gt;
#include &lt;std_msgs/Float32.h&gt;
#include &lt;NewPing.h&gt;

float steering = 0;
float velocity = 0; //0430 int -&gt; float

#define TRIG_L 3
#define ECHO_L 2
#define TRIG_R 11
#define ECHO_R 10
#define MAXD 50

float sonar_L = MAXD;
float sonar_R = MAXD;

//drive_motor
#define MOTOR_PWM 5
#define MOTOR_DIR 4
int Motor_Speed = 0;

// Steering Servo Control
#include &lt;Servo.h&gt;
#define RC_SERVO_PIN 8
#def
…
;
  }
  Distance_L.data=sonar_L;
  Distance_R.data=sonar_R;
  //Serial.print("Sonar_L : ");
  //Serial.print(sonar_L);
  //Serial.print("cm");
  //delay(20);
  //Serial.print("  Sonar_R : ");
  //Serial.print(sonar_R); //측정된 물체로부터 거리값(cm값)을 보여줍니다.
  //Serial.println("cm");
  steering_control();
 
  if(Motor_Speed &gt; 0)      motor_control(1,Motor_Speed);
  else if(Motor_Speed &lt; 0) motor_control(-1,-Motor_Speed);
  else motor_control(0,0);
 
  pub_sensor_L.publish( &Distance_L);
  pub_sensor_R.publish( &Distance_R);
  nh.spinOnce();
  delay(10);
}