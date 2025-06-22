int relay_pin = 4;
const String SignalfromPy = "";
unsigned long currentTime = 0;

void setup()
{
  Serial.begin(9600); 
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, LOW); 
}
void loop(){
  if (Serial.available()) {
    SignalfromPy = Serial.readStringUntil('\n');
    if (SignalfromPy == "D") { //circle disappear/wait for mouse click, python->arduino, send time to python
      digitalWrite(relay_pin, HIGH);// block
      currentTime = millis();
      Serial.println(currentTime);
    }
    else if (SignalfromPy == "S") {// screen clicked, python->arduino, 
      digitalWrite(relay_pin, LOW);// trans
      currentTime = millis();
      Serial.println(currentTime);
    } 
  }
}