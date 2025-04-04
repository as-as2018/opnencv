// Define the LED pins
const int ledRecognizedPin = 8;  // LED to turn ON when a face is recognized
const int ledUnknownPin = 9;     // LED to turn ON when face is unknown or not found

void setup() {
  // Start Serial communication - MUST match BAUD_RATE in Python script
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port connection (needed for some boards like Leonardo)
  }

  // Set LED pins as outputs
  pinMode(ledRecognizedPin, OUTPUT);
  pinMode(ledUnknownPin, OUTPUT);

  // Turn both LEDs off initially
  digitalWrite(ledRecognizedPin, LOW);
  digitalWrite(ledUnknownPin, LOW);

  Serial.println("Arduino Ready. Waiting for commands ('R' or 'U')...");
}

void loop() {
  // Check if data is available from the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte (character)
    char command = Serial.read();

    Serial.print("Received: ");
    Serial.println(command); // Print received command for debugging

    // Control LEDs based on the command
    if (command == 'R') { // Recognized
      digitalWrite(ledRecognizedPin, HIGH); // Turn Recognized LED ON
      digitalWrite(ledUnknownPin, LOW);    // Turn Unknown LED OFF
      Serial.println("Status: Recognized -> LED 8 ON, LED 9 OFF");
    }
    else if (command == 'U') { // Unknown or No Face
      digitalWrite(ledRecognizedPin, LOW);     // Turn Recognized LED OFF
      digitalWrite(ledUnknownPin, HIGH);    // Turn Unknown LED ON
      Serial.println("Status: Unknown/None -> LED 8 OFF, LED 9 ON");
    }
    else {
      // Optional: Handle unexpected characters
      Serial.print("Ignoring unknown command: ");
      Serial.println(command);
    }
  }
}