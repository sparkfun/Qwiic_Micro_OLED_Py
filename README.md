# Qwiic_Micro_OLED_Py
Python package for the qwiic [Micro OLED board](https://www.sparkfun.com/products/14532)

![SparkFun Qwiic Micro OLED Breakout](https://cdn.sparkfun.com//assets/parts/1/2/6/2/1/14532-SparkFun_Micro_OLED_Breakout__Qwiic_-01.jpg)

This package is a port of the [SparkFun Micro OLED Breakout Arduino Library](https://github.com/sparkfun/SparkFun_Micro_OLED_Arduino_Library)

## Dependencies 
This driver package depends on the qwii I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

## Installation

### PyPi Installation
On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```
  sudo pip install sparkfun_qwiic_micro_oled
```
For the current user:

```
  pip install sparkfun_qwiic_micro_oled
```

### Local Installation
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```
  $ python setup.py install
```

To build a package for use with pip:
```
  $ python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```
  cd dist
  pip install sparkfun_micro_oled-<version>.tar.gz
```
  
## Example Use
See the examples directory for more detailed use examples.

```python
import qwiic_micro_oled
import sys




def runExample():

    #  These three lines of code are all you need to initialize the
    #  OLED and print the splash screen.
  
    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.


    print("\nSparkFun Micro OLED Hello Example\n")
    myOLED = qwiic_micro_oled.QwiicMicroOled()

    if myOLED.isConnected() == False:
        print("The Qwiic Micro OLED device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    myOLED.begin()
    #  clear(ALL) will clear out the OLED's graphic memory.
    #  clear(PAGE) will clear the Arduino's display buffer.
    myOLED.clear(myOLED.ALL)  #  Clear the display's memory (gets rid of artifacts)
    #  To actually draw anything on the display, you must call the
    #  display() function. 
    myOLED.display()

runExample()
```
