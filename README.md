Robosub: Controls 2017-2018, (Add years changed here)
===========================
Last Updated: April 27, 2018

![](https://github.com/CSU-Robosub-2017-2018/Controls/blob/master/Pictures/20180328_211226.jpg "Robosub AUV Pool Test April 7, 2018")

CSU Robosub team is a senior desgin team with the goal of creating an autonomous underwater vehicle (AUV). The vehicle is made to compete in the [nationonal robosub competition](http://www.robonation.org/competition/robosub) hosted by the navy in [California](http://scripts.mit.edu/~orca/wiki/index.php?title=Transdec).

The [2017-2018 team](http://csuauv.colostate.edu/2017-2018/) is "vertically integrated" meaning that it is made up of 11 seniors as well as 4 underclassman and 2 gradutate advisors. The team is split up into 4 different subteams: Propulsion, Sensors, Mechanical, and Controls.

----

## Controls ##
The controls subteams goal is to integrate sensors and propulsion systems to make the AVU autonomous. 
We worked really hard in the 2017-2018 academic year to provide a robust variety of libraries specifially tailored to the robosub. They include:
* Computer Controller Motor Drivers
* PID Controller
* Xbox Controller Support
* Integration with Sensors.

### Motor Driver ###
This driver is the interface between running vision and stabilization on the Raspberry pi and Controlling the Electronic speed controllers(ESC) of the Propulsion subteams Motors.

Originally the decision was made to try and run all of the motor ESCs off of a PWM singal generated by an Arduino. All of our code was to be run off of a Raspberry Pi then sent to the Arduino.

A Considerable amount of time was spent trying to create a reliable interface between the Raspbewrry Pi and Arduino. Several methods of doing this were considered including SPI, I2C, and UART. Eventually it was decided to use serial because it only needed the USB cable to operate. This effort was abandon because a information was never able to be reliablly communicated between over serial. The communication would be consistant one run then not exsistant another.

We switched over to using and [Adafruit 12bit PWM hat](https://www.adafruit.com/product/2327) to control the ESCs. This solution is considerallby more reliable than the Arduino. It was exremely easy to get working as well. Only taking about 2 days of work to get the solution relablly outputting the values that we needed.

### PID Controller ###
One of the first challeneges that needed to be tackled in order for the submarine to be autonomous was to create a rilable way for the AUV to get into a stable orientation. To do this a PID controller was developed. As it stands at the end of 2017-2018 the controller is very generic and is able to be instanciated multiple times. For accurate control of the AUV a minimum of 3 PID controllers are required. One for each: Pitch, Roll, and Yaw.



## How To ##
 __Install__
 
 1. The PWM hat requires the [Adafruit_Pytohn PCA9685](https://github.com/adafruit/Adafruit_Python_PCA9685) Driver to operate.
    1. You may follow the install instructions provided but i found that for imports to work properly you needed to install it using both python 2 and python3.
    2. I used the following install commands:
    
            sudo apt-get install git build-essential python-dev python3-dev
            cd ~
            git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
            cd Adafruit_Python_PCA9685
            sudo python setup.py install
            sudo python3 setup.py install
     
    3. This may result inseveral warnings but again this is the only way that i reliablly was able to get the imports to work how they were supposed to.
2. To download, install, and use the Motorcontroller you need to git a version of the Controls Repo.

        git clone https://github.com/CSU-Robosub-2017-2018/Controls.git
        
3. The most up to example of how to use all of the functions of the Controls repo is contained in the Apr7Test.py file.
  



# Requirements
https://github.com/adafruit/Adafruit_Python_GPIO
https://github.com/adafruit/Adafruit_Python_PCA9685
https://github.com/adafruit/Adafruit_Python_PureIO
https://pypi.python.org/pypi/inputs
