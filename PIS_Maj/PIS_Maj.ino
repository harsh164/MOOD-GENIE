#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.

PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"

const int PulseWire = A2;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 13;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
int GSRsensorPin = A0;
int ThermistorPin = A1;
int Vo;
float R1 = 10000; // value of R1 on board
float logR2, R2, T;
float c1 = 0.001129148, c2 = 0.000234125, c3 = 0.0000000876741; //steinhart-hart coeficients for thermistor
const int p=0;

void setup() 
{
  
  Serial.begin(9600); // open a serial port connection to computer
  pulseSensor.begin();  //to create pulsesensor object
  pinMode(GSRsensorPin, INPUT); // define which pins are used for input and output    
  pulseSensor.analogInput(PulseWire);   // Configure the PulseSensor object, by assigning our variables to it.
  pulseSensor.blinkOnPulse(LED13);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);    
  
}

void loop() 
{
  //for gsr sensor:
  int sensorVal = analogRead(GSRsensorPin)-150; // read data from appropriate pin and assign value to variable
  Serial.print(sensorVal);  // print sensor reading to the the computer via serial port

  //for temperature sensor:
  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0); //calculate resistance on thermistor
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2)); // temperature in Kelvin
  T = T - 273.15; //convert Kelvin to Celcius
  // T = (T * 9.0)/ 5.0 + 32.0; //convert Celcius to Farenheit

  Serial.print('\t'); //provide space between readings on serial monitor
  Serial.print(T);
  Serial.print('\t');

  //for pulse sensor:
  int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
                                                // "myBPM" hold this BPM value now. 
  if (pulseSensor.sawStartOfBeat()) // Constantly test to see if "a beat happened".
  {             
    Serial.print(myBPM);                       // Print the value inside of myBPM. 
  }
  else
  {
    Serial.print(p);
  }

  Serial.println(); //print new line in serial monitor
    
  delay(1000);  // wait for 1000 milliseconds before reading sensor again 
}
