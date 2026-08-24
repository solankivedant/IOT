int pins[] = {13, 11, 9, 7};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
}
void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], HIGH);
    delay(2000);
    digitalWrite(pins[i], LOW);
  }
}