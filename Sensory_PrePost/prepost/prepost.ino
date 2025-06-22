// Arduino code with improved time synchronization and millisecond precision
int relay_pin = 4;
String inputBuffer = "";
unsigned long arduinoStartMillis = 0;  // When Arduino starts
unsigned long pythonEpochOffset = 0;   // Offset to convert Arduino time to Unix time
bool timeInitialized = false;

void setup() {
  Serial.begin(9600);
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, LOW);
  arduinoStartMillis = millis();  // Record when Arduino starts
  
  // Send ready message when Arduino starts
  Serial.println("ARDUINO_READY");
}

void loop() {
  // Read any incoming serial data
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    
    // Add to buffer if not end of line
    if (inChar != '\n') {
      inputBuffer += inChar;
    }
    // Process the command when a newline is received
    else {
      processCommand(inputBuffer);
      inputBuffer = ""; // Clear the buffer
    }
  }
}

// Process commands from Python
void processCommand(String command) {
  // Time sync command format: "T:1234567890.123"
  if (command.startsWith("T:")) {
    // Extract timestamp after the colon
    String timestampStr = command.substring(2);
    
    // Find decimal point position
    int decimalPos = timestampStr.indexOf('.');
    
    if (decimalPos == -1) {
      // No decimal point, treat as seconds only
      unsigned long pythonSeconds = strtoul(timestampStr.c_str(), NULL, 10);
      pythonEpochOffset = pythonSeconds - (millis() / 1000);
      timeInitialized = true;
    } else {
      // Handle decimal seconds
      String secondsStr = timestampStr.substring(0, decimalPos);
      String millisStr = timestampStr.substring(decimalPos + 1);
      
      // Convert seconds and milliseconds parts
      unsigned long pythonSeconds = strtoul(secondsStr.c_str(), NULL, 10);
      unsigned long pythonMillis = 0;
      
      // Handle first 3 digits of milliseconds (the rest is beyond Arduino precision)
      if (millisStr.length() > 3) {
        millisStr = millisStr.substring(0, 3);
      }
      pythonMillis = strtoul(millisStr.c_str(), NULL, 10);
      
      // Calculate millis of the full timestamp
      unsigned long pythonTotalMillis = (pythonSeconds * 1000) + pythonMillis;
      
      // Calculate offset (keep in milliseconds for precision)
      pythonEpochOffset = pythonSeconds - (millis() / 1000);
      timeInitialized = true;
    }
    
    // Send confirmation with the synchronized time that includes decimals
    Serial.print("SYNC_OK:");
    Serial.println(getUnixTimeWithMillis());
  }
  else if (command == "D") {  // Circle disappear/wait for mouse click
    digitalWrite(relay_pin, HIGH);  // Block
    
    // Send current Unix-style timestamp with milliseconds
    Serial.print("D:");
    Serial.println(getUnixTimeWithMillis());
  }
  else if (command == "S") {  // Screen clicked
    digitalWrite(relay_pin, LOW);  // Trans
    
    // Send current Unix-style timestamp with milliseconds
    Serial.print("S:");
    Serial.println(getUnixTimeWithMillis());
  }
}

// Convert Arduino time to Unix time using the calculated offset, including milliseconds
String getUnixTimeWithMillis() {
  if (timeInitialized) {
    // Get current millis
    unsigned long currentMillis = millis();
    
    // Cal/Users/leeliang/Desktop/shift_pilotculate seconds and milliseconds
    unsigned long seconds = (currentMillis / 1000) + pythonEpochOffset;
    unsigned long millisPart = currentMillis % 1000;
    
    // Format as seconds.milliseconds
    String timeStr = String(seconds) + "." + String(millisPart);
    return timeStr;
  } else {
    // If not synchronized yet, just return millis in seconds.milliseconds
    unsigned long currentMillis = millis();
    unsigned long seconds = currentMillis / 1000;
    unsigned long millisPart = currentMillis % 1000;
    
    String timeStr = String(seconds) + "." + String(millisPart);
    return timeStr;
  }
}