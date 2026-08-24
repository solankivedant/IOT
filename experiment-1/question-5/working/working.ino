int led9 = 9, brightness = 0, fadeAmount = 5;
int led13 = 13;
unsigned long previousMillis = 0;
bool led13State = LOW;

void setup() {
  pinMode(led9, OUTPUT);
  pinMode(led13, OUTPUT);
}
void loop() {
  analogWrite(led9, brightness);
  brightness += fadeAmount;
  if (brightness <= 0 || brightness >= 255) fadeAmount = -fadeAmount;

  if (millis() - previousMillis >= 1000) {
    previousMillis = millis();
    led13State = !led13State;
    digitalWrite(led13, led13State);
  }
  delay(30);
}