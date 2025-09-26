// Simulated Temperature, Distance Sensor
// Arduino sends fake temp values to Serial
int ledTemp = 2;
int ledDist = 3;
int ledSpeed = 4;

unsigned long tempOFFTime = 0;
unsigned long distOFFTime = 0;
unsigned long speedOFFTime = 0;



void setup() {
  Serial.begin(115200); // Start serial at 115200 baud
  randomSeed(analogRead(A0)); //seed RNG 
  pinMode(ledTemp, OUTPUT);
  pinMode(ledDist, OUTPUT);
  pinMode(ledSpeed, OUTPUT);
}

void loop() {
  
  int tempC = random(20, 110); // fake "temperature" between 20°C and 110°C
  int distance = random(5, 200); // fake "distance" between 5-200cm
  int speed = random(0, 100); //fake "speed" between 0-100m/s
  // Print it to Serial
  Serial.print(tempC);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(",");
  Serial.println(speed);

  // led control from python
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd = "TEMP_ON") {
      digitalWrite(ledTemp, HIGH);
      tempOFFTime = millis() +1000;
      printf("TEMP ON");
    } 
    

    if (cmd = "DIST_ON") {
      digitalWrite(ledDist, HIGH);
      distOFFTime = millis() + 1000;
      printf("DIST ON");
    }
    

    if (cmd = "SPEED_ON") {
      digitalWrite(ledSpeed, HIGH);
      speedOFFTime = millis() + 1000;
      printf("SPEED ON");
    }

  }

  if (millis() > tempOFFTime) digitalWrite(ledTemp, LOW);
  if (millis() > distOFFTime) digitalWrite(ledDist, LOW);
  if (millis() > speedOFFTime) digitalWrite(ledSpeed, LOW);


  delay(400); // Wait .4 second before sending again
}
