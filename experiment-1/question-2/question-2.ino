void setup() {
  pinMode(13, OUTPUT);
}
void loop() {
  digitalWrite(13, HIGH);
  delay(400);   // ON 40% of 1000 ms
  digitalWrite(13, LOW);
  delay(600);   // OFF 60% of 1000 ms
}