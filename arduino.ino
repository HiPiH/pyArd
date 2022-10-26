#include <AFMotor.h>
#include <Servo.h>

const unsigned int MAX_MESSAGE_LENGTH = 5;
static int message[MAX_MESSAGE_LENGTH];

#define MOTOR1 0
#define MOTOR2 1
#define MOTOR3 2
#define MOTOR1 3
#define SERVO1 4

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
AF_DCMotor allMotors[4] = {motor1, motor2, motor3, motor4};
Servo myservo;        // Создаем объект 

void setup() {
  Serial.begin(115200);

  myservo.attach(9);
  myservo.write(60);
  for(int x=0; x<4;x++)
     {
        allMotors[x].setSpeed(0);
        allMotors[x].run(RELEASE);
     }

  Serial.print("#ok\n");
}


void readCommand()
{
  while (Serial.available() > 0)
   {
     
     static unsigned int message_pos = 0;
     int inByte = Serial.read();
     if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
     {
       message[message_pos] = inByte-100;
       message_pos++;
     }
     else
     {
       message[message_pos] = '\0';
       Serial.print("#");
       for(int x = 0; x<MAX_MESSAGE_LENGTH; x++)
       {
          Serial.print(message[x],DEC);
          Serial.print(",");
       }
       Serial.print("\n");
       message_pos = 0;
     }
   }
}


float accel = 0;
int direct = -1;
int current = 60;
void servoProcess()
{
   direct = REG_Array[9];
   accel = REG_Array[10];
   Serial.print("Servo direct:");         
   Serial.println(direct);  
   Serial.print("Servo accel:");         
   Serial.println(accel);      
}
void servotik()
{ 
  if(accel != 0)
  {
  
         if(direct == 0)
        {
           if(current <120)
           {
               current = current + accel;
           }
        }else{
            if(current > 0)
           {
             current = current - accel;
            }
        }
        myservo.write(current);
        delay(100);
        Serial.print("Current angle:");         
        Serial.println(current);  
  }
  


}

struct motorStatus{
  int d = 0;
  int s = 0;
  int t = 0;
};
motorStatus lastMotorsStatrus[4];

void motortik(){
  for(int x=0;x<4;x++)
  {
    int d = REG_Array[x*2+1];
    int s = REG_Array[x*2+2];
    motorStatus last_status = lastMotorsStatrus[x];
    
    if(s == 0)
    {
        allMotors[x].run(RELEASE);
    }else{

        if (last_status.d != d)
        {
          allMotors[x].run(RELEASE);
        }
        if(d == 1)
        {
           allMotors[x].run(FORWARD);
        }else{
           allMotors[x].run(BACKWARD);
        }
        
        
        if (last_status.s != s) 
          allMotors[x].setSpeed(s);     
    }
  }
    
  
}

void loop() 
{
    readCommand();
    motortik();
    servotik();
}
