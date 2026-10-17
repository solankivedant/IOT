/*
 Experiment 31 - Board A (web server)

 Same as Experiment 18 sketch, only the IP is changed to 192.168.0.177
 so that Board B (exp-31.cpp, IP 192.168.0.178) can read this page.

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Potentiometer: outer legs to 5V and GND, middle leg to A0
 */

#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // Board B uses ...0xEE
IPAddress ip(192, 168, 0, 177);                        // Board A address

EthernetServer server(80);

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac, ip);
  Serial.print("Hardware status: ");
  Serial.println(Ethernet.hardwareStatus());
  Serial.print("Link status: ");
  Serial.println(Ethernet.linkStatus());
  server.begin();
  Serial.print("Server is at ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    boolean blankLine = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        if (c == '\n' && blankLine) {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println();
          client.println("<!DOCTYPE HTML><html>");
          for (int a = 0; a < 6; a++) {
            client.print("analog input ");
            client.print(a);
            client.print(" is ");
            client.print(analogRead(a));
            client.println("<br />");
          }
          client.println("</html>");
          break;
        }
        blankLine = (c == '\n') ? true : (c == '\r') ? blankLine : false;
      }
    }
    delay(1);
    client.stop();
  }
}
