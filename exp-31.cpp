/*
 Experiment 31 - Read data from another Arduino's web server

 Board A (server) : runs Experiment 18 sketch, IP 192.168.0.177
 Board B (client) : this sketch,              IP 192.168.0.178
 Both boards connected to the SAME router with Ethernet cables.

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 */

#include <SPI.h>
#include <Ethernet.h>

// Board B needs its OWN MAC address (Board A uses ...0xED)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE };

IPAddress ip(192, 168, 0, 178);       // this board (Board B)
IPAddress server(192, 168, 0, 177);   // Board A (web server)

EthernetClient client;

void setup() {
  Serial.begin(9600);

  // fixed IP, so no long wait for DHCP
  Ethernet.begin(mac, ip);
  delay(1000);                          // give the shield time to start

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield not found");
  }
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected");
  }

  Serial.print("My IP: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  Serial.println("connecting to Board A...");

  if (client.connect(server, 80)) {
    Serial.println("connected");
    client.println("GET / HTTP/1.1");   // ask Board A for its web page
    client.println("Host: 192.168.0.177");
    client.println("Connection: close");
    client.println();

    // print the page, stop after 3 s if Board A does not close
    unsigned long start = millis();
    while (client.connected() && millis() - start < 3000) {
      while (client.available()) {
        char c = client.read();
        Serial.print(c);
      }
    }
    client.stop();
    Serial.println();
    Serial.println("disconnecting.");
  } else {
    Serial.println("connection failed");
  }

  Serial.println("-----------------------------");
  delay(5000);                          // read again after 5 s
}
