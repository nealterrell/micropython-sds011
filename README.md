# ESP8266 MicroPython air quality sensor (SDS011)

This is my mediocre attempt at running an SDS011 air quality sensor (PM2.5 and PM10) on a Wemos D1 Mini (ESP8266) microcontroller with MicroPython. The two sensor outputs are displayed on a 16x2 LCD display.

## Wiring diagram

![](https://raw.githubusercontent.com/nealterrell/micropython-sds011/master/air-sensor_bb.png)

## Photo

![](https://lh3.googleusercontent.com/aNSQ38goDbYtVshTzClRuuZH3N6JB7b3TV848pGMMqUj3jI43SJhVkRNlKGPCv6CglQANd4Zugpt-9j-CgUJXKTcMjWrQPcs-nR6ASsodBXw0p71nFbhh_vcBFm2riLtJw1woyqq8Ia9nICBOU1KBLibDbXqoGJgOV14E52ViHj6OeOfrSuWHLFvLffntddoBvOUyNu3_xO3gQHieEBUsxL1pu1d1gIspPbHiiuw4NoTV0EZRKb04rDhncyQpUO2tApH5LsStd2aFoyBzxNJuvBc16v9kaLOpWpzahsYvd1ma11CXb2bHewUhXE_PpBPWV9IytFBhhmEaPmy01hr7jTu1mby6F-wMB9zxWqGmjRxy3v3l4oQT4OydDRlxSTJS0oLQErUVknlbeXNiTdulm7qWcp9KOLxobHFstqbL_LgHAuEQEbaKxgC5ZiH8TTzdo0C1juTPakLID61dVLy9S17ddzx5dqCZ5MheJIycfEwbT3rPc1bcFE6GH6379yok1TMu4yzWIEpGtkl9KkRtiaq8xnWghal0wrFwAaqqakczbhY1YQelhfwjuM8sU2fUNbI-ULspvgKer6WdCzFFRLAyYkFLYZCzs6f_xpEn82ih3IQsKvmhpoTOC3vPi_DfHBcla8pBh8kPMyC494g0D0Kzm_aJK4s78PaWwm-bJJR8q5i1EGYF80GKJEN=w1605-h903-no?authuser=0)


## Why MicroPython?

I teach an introductory programming course at [CSULB](https://www.csulb.edu) using Python, and one project involves calculating Air Quality Index given user inputs about the concentration of various pollutants, including PM2.5 and PM10. I wanted to run my students' code on a microcontroller with sensor inputs so they can see their work "in the wild".

## Difficulties and lessons learned

The SDS011 module I purchased has modified firmware compared to the reference specs I found. In the reference, the numeric values returned by the sensor must be divided by 10 to put into micrograms per meter cubed. My sensor has done that in the firmware -- unless my average house interior has *impossibly small* PM2.5 and PM10 concentrations.

This change seems to have also broken the PWM outputs from the device. (The Amazon seller's page does mention that the PWM wires are not used.) 

 MicroPython relies on the RX/TX pins to communicate with its Web REPL. The ESP8266 only has one each of these pins, but the SDS011 uses UART over RX/TX to send sensor values to the controller. Using UART with the SDS011 corrupts the Web REPL, which makes development harder... in Arduino IDE with C++ we'd use SoftwareSerial to do UART over different pins, but that isn't available in MicroPython. So I found a trick to use `uos.dupterm()` to "disable" the Web REPL while communicating with the SDS011, and then re-enable it after the sensor is read.

 `main.py` starts the sensor read and display on an infinite loop with a 1 second delay per loop. This should probably be hooked to a button to trigger a single update.
