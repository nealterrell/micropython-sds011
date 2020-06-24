# ESP8266 MicroPython air quality sensor (SDS011)

This is my mediocre attempt at running an SDS011 air quality sensor (PM2.5 and PM10) on a Wemos D1 Mini (ESP8266) microcontroller with MicroPython. The two sensor outputs are displayed on a 16x2 LCD display.

## Wiring diagram



## Photo



## Why MicroPython?

I teach an introductory programming course at [CSULB](https://www.csulb.edu) using Python, and one project involves calculating Air Quality Index given user inputs about the concentration of various pollutants, including PM2.5 and PM10. I wanted to run my students' code on a microcontroller with sensor inputs so they can see their work "in the wild".

## Difficulties and lessons learned

The SDS011 module I purchased has modified firmware compared to the reference specs I found. In the reference, the numeric values returned by the sensor must be divided by 10 to put into micrograms per meter cubed. My sensor has done that in the firmware -- unless my average house interior has *impossibly small* PM2.5 and PM10 concentrations.

This change seems to have also broken the PWM outputs from the device. (The Amazon seller's page does mention that the PWM wires are not used.) 

 MicroPython relies on the RX/TX pins to communicate with its Web REPL. The ESP8266 only has one each of these pins, but the SDS011 uses UART over RX/TX to send sensor values to the controller. Using UART with the SDS011 corrupts the Web REPL, which makes development harder... in Arduino IDE with C++ we'd use SoftwareSerial to do UART over different pins, but that isn't available in MicroPython. So I found a trick to use `uos.dupterm()` to "disable" the Web REPL while communicating with the SDS011, and then re-enable it after the sensor is read.

 `main.py` starts the sensor read and display on an infinite loop with a 1 second delay per loop. This should probably be hooked to a button to trigger a single update.