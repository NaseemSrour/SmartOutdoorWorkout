/*
  Example code for Benewake TFMini time-of-flight distance sensor.
  by Peter Jansen (December 11/2017)
  This example code is in the public domain.

  This example communicates to the TFMini using a SoftwareSerial port at 115200,
  while communicating the distance results through the default Arduino hardware
  Serial debug port.

  SoftwareSerial for some boards can be unreliable at high speeds (such as 115200).
  The driver includes some limited error detection and automatic retries, that
  means it can generally work with SoftwareSerial on (for example) an UNO without
  the end-user noticing many communications glitches, as long as a constant refresh
  rate is not required.

  The (UNO) circuit:
   Uno RX is digital pin 10 (connect to TX of TF Mini)
   Uno TX is digital pin 11 (connect to RX of TF Mini)

  THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
#include <Wire.h>
#include <SoftwareSerial.h>
#include "TFMini.h"
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#define USE_SERIAL Serial

// Setup software serial port
SoftwareSerial mySerial(13, 15);      // Uno RX (TFMINI TX), Uno TX (TFMINI RX)
TFMini tfmini;
double prevAvgSpeed=0;
int prevDir = 0;
uint16_t prevDist = 0;
unsigned long start = 0, finished;
double elapsed;
double diffDist;
ESP8266WiFiMulti WiFiMulti;

void setup() {
  // Step 1: Initialize hardware serial port (serial debug port)
  Serial.begin(115200);
  // wait for serial port to connect. Needed for native USB port only
  while (!Serial);

  Serial.println ("Initializing...");

  // Step 2: Initialize the data rate for the SoftwareSerial port
  mySerial.begin(TFMINI_BAUDRATE);

  // Step 3: Initialize the TF Mini sensor
  tfmini.begin(&mySerial);

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("HANTAZ", "123456789O");

  delay(3000);
  start = millis();
}


void loop() {
  // Take one TF Mini distance measurement
  uint16_t dist = tfmini.getDistance();
  uint16_t strength = tfmini.getRecentSignalStrength();
  int dir;
  double avgSpeed=0;
  double currAcc = 0;

  if ((WiFiMulti.run() == WL_CONNECTED) && dist >= 0 && strength >= 0) {
    HTTPClient http;
    //USE_SERIAL.print("[HTTP] begin...\n");

    if (abs(dist - prevDist) > 2)
    {
      if (prevDist < dist)
        dir = 1; // up
      else
        dir = 2; // down
    }
    else
      dir = 0;
    
    if(dir!=0)
    {
      finished = millis();
      elapsed = (double) (finished - start) / 1000;
      start = finished;
      diffDist = (double) abs(dist - prevDist);
      avgSpeed = diffDist / elapsed;
      currAcc = (avgSpeed-prevAvgSpeed)/elapsed;
      if(avgSpeed != 0)
      {
        if (dir == 1)
          http.begin("http://40.113.134.7/Arduino/reports?machineID=1&speed=" + String(avgSpeed) + "&timeInterval=" + String(elapsed) + "&acc=" + String(currAcc) + "&dir=up"); //HTTP
        if (dir == 2)
          http.begin("http://40.113.134.7/Arduino/reports?machineID=1&speed=" + String(avgSpeed) + "&timeInterval=" + String(elapsed) + "&acc=" + String(currAcc) + "&dir=down");
        USE_SERIAL.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        int httpCode = http.GET();
        // httpCode will be negative on error
        if (httpCode > 0) {
          // HTTP header has been sent and Server response header has been handled
          USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);
          // file found at server
          if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            USE_SERIAL.println(payload);
          }
        } else {
          USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }
        http.end(); 
      }
    }
    else{
      start = millis();
    }
    prevAvgSpeed = avgSpeed;
    prevDist = dist;
    prevDir = dir;
    prevDist = dist;
    // Display the measurement
    if (dir != 0)
    {
      Serial.println("  dist = " + String(dist) + ",  diff = " + String(diffDist) + ",  signal = " + String(strength) + " ,  dir = " + String(dir) + ", avdSpeed: " + String(avgSpeed) + ", currAcc = "+ String(currAcc) + ", elapsed: " + elapsed);
    }
  }
  // Wait some short time before taking the next measurement
  delay(100); // was 25
}

