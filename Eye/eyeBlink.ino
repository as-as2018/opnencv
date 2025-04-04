const int ledPin = 13; // LED connected to digital pin 13

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600); // Start serial communication
}

void loop() {
    if (Serial.available() > 0) { // Check if data is available
        char received = Serial.read(); // Read the incoming byte

        if (received == '1') {
            digitalWrite(ledPin, HIGH); // Turn LED ON
        } else if (received == '0') {
            digitalWrite(ledPin, LOW); // Turn LED OFF
        }
    }
}
