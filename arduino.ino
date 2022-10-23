const unsigned int MAX_MESSAGE_LENGTH = 10;


void setup() {
  Serial.begin(115200);
  Serial.print("#ok\n");
}


void readCommand()
{
  while (Serial.available() > 0)
   {
     static char message[MAX_MESSAGE_LENGTH];
     static unsigned int message_pos = 0;
     char inByte = Serial.read();
     if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
     {
       message[message_pos] = inByte;
       message_pos++;
     }
     else
     {
       Serial.print("#done\n");
       message_pos = 0;
     }
   }
}

void loop() 
{
    readCommand();
}
