int led3 = 3;
int led4 = 4;
int led5 = 5;

void setup() {
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);

  Serial.begin(9600);
  Serial.println("Enter a number between 3 and 5:");
}

void loop() {
  if (Serial.available() > 0) {
    int num = Serial.parseInt();

    // Clear remaining serial input
    while (Serial.available() > 0) {
      Serial.read();
    }

    if (num < 3 || num > 5) {
      Serial.println("Number is out of Range.");
    }
    else {
      int ledPin = num;

      digitalWrite(ledPin, HIGH);
      delay(2000);
      digitalWrite(ledPin, LOW);
    }

    Serial.println("Enter a number between 3 and 5:");
  }
}