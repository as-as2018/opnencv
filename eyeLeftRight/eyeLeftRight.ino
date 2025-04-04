#define LEFT_LED  12  // Pin for Left LED
#define RIGHT_LED 13  // Pin for Right LED

void setup() {
  pinMode(LEFT_LED, OUTPUT);
  pinMode(RIGHT_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();  // Read command from Python

    if (command == 'L') {
      digitalWrite(LEFT_LED, HIGH);
      digitalWrite(RIGHT_LED, LOW);
    } 
    else if (command == 'R') {
      digitalWrite(LEFT_LED, LOW);
      digitalWrite(RIGHT_LED, HIGH);
    } 
    else if (command == 'O') {
      digitalWrite(LEFT_LED, LOW);
      digitalWrite(RIGHT_LED, LOW);
    }
  }
}
