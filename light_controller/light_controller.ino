void setup() {
  // put your setup code here, to run once:

  /*** SERIAL PORT ***/
  // baudrate of 9600 for serial communication
  Serial.begin(9600);

  // allows for faster serial communication
  Serial.setTimeout(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    // read input from serial
    int in = Serial.read();

    Serial.println(in);
  }
}
