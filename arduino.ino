const unsigned int MAX_MESSAGE_LENGTH = 5;
static int message[MAX_MESSAGE_LENGTH];

#define MOTOR1 0
#define MOTOR2 1
#define MOTOR3 2
#define MOTOR1 3
#define SERVO1 4


void setup() {
  Serial.begin(115200);
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

void loop() 
{
    readCommand();
}
