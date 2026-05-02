// E-Nose Sensor Interface
// Connects MQ-2, MQ-3, MQ-5, MQ-7, MQ-135 to Analog Pins A0-A4


const int MQ2_PIN = A0;
const int MQ3_PIN = A1;
const int MQ5_PIN = A2;
const int MQ7_PIN = A3;
const int MQ135_PIN = A4;

void setup() {
  Serial.begin(9600);
  Serial.println("E-Nose System Initializing...");
  delay(2000); // Warm up sensors
}

void loop() {
  int mq2 = analogRead(MQ2_PIN);
  int mq3 = analogRead(MQ3_PIN);
  int mq5 = analogRead(MQ5_PIN);
  int mq7 = analogRead(MQ7_PIN);
  int mq135 = analogRead(MQ135_PIN);

  // Send data in JSON format for easy parsing by Python backend
  Serial.print("{\"mq2\": ");
  Serial.print(mq2);
  Serial.print(", \"mq3\": ");
  Serial.print(mq3);
  Serial.print(", \"mq5\": ");
  Serial.print(mq5);
  Serial.print(", \"mq7\": ");
  Serial.print(mq7);
  Serial.print(", \"mq135\": ");
  Serial.print(mq135);
  Serial.println("}");

  delay(2000); // Send data every 2 seconds
}
