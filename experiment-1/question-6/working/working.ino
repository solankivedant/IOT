int pins[] = {13, 11, 9, 7};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
}
void loop() {
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], HIGH);
  delay(1000);
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], LOW);
  delay(1000);
}