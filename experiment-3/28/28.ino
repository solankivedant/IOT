const int segPins[7] = {2, 3, 4, 5, 6, 7, 8};
 
const byte digits[10] = {
  0x3F,  // 0
  0x06,  // 1
  0x5B,  // 2
  0x4F,  // 3
  0x66,  // 4
  0x6D,  // 5
  0x7D,  // 6
  0x07,  // 7
  0x7F,  // 8
  0x6F   // 9
};
 
void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(segPins[i], OUTPUT);
  }
}
void loop() {
  for (int n = 0; n < 10; n++) {
	for (int s = 0; s < 7; s++) {
      		digitalWrite(segPins[s], !bitRead(digits[n], s));

    	}
    delay(2000);   
  }
}
