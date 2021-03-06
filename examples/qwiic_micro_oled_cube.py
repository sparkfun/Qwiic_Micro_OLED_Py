#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_micro_oled_cube.py
#
# Simple Example for the Qwiic MicroOLED Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers.
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================
# Example - simple command to draw a cube the OLED.
#

from __future__ import print_function, division
import qwiic_micro_oled
import sys
import time
import math

d = 3
px = [-d,  d,  d, -d, -d,  d,  d, -d ]
py = [-d, -d,  d,  d, -d, -d,  d,  d ]
pz = [-d, -d, -d, -d,  d,  d,  d,  d ]

p2x = [0,0,0,0,0,0,0,0]
p2y = [0,0,0,0,0,0,0,0]

r = [0,0,0]

SHAPE_SIZE=600
def drawCube(oled):

    global p2x, p2y, r


    r[0]=r[0] + math.pi/180.0 #  Add a degree
    r[1]=r[1] + math.pi/180.0 #  Add a degree
    r[2]=r[2] + math.pi/180.0 #  Add a degree
    if r[0] >= 360.0*math.pi/180.0:
        r[0] = 0
    if r[1] >= 360.0*math.pi/180.0:
        r[1] = 0
    if r[2] >= 360.0*math.pi/180.0:
        r[2] = 0

    scrWidth = oled.get_lcd_width()
    scrHeight = oled.get_lcd_height()

    for i in range(8):

        px2 = px[i]
        py2 = math.cos(r[0])*py[i] - math.sin(r[0])*pz[i]
        pz2 = math.sin(r[0])*py[i] + math.cos(r[0])*pz[i]

        px3 = math.cos(r[1])*px2 + math.sin(r[1])*pz2
        py3 = py2
        pz3 = -math.sin(r[1])*px2 + math.cos(r[1])*pz2

        ax = math.cos(r[2])*px3 - math.sin(r[2])*py3
        ay = math.sin(r[2])*px3 + math.cos(r[2])*py3
        az = pz3-150

        p2x[i] = scrWidth/2+ax*SHAPE_SIZE/az
        p2y[i] = scrHeight/2+ay*SHAPE_SIZE/az

    oled.clear(oled.PAGE)

    for i in range(3):

        oled.line(p2x[i],p2y[i],p2x[i+1],p2y[i+1])
        oled.line(p2x[i+4],p2y[i+4],p2x[i+5],p2y[i+5])
        oled.line(p2x[i],p2y[i],p2x[i+4],p2y[i+4])

    oled.line(p2x[3],p2y[3],p2x[0],p2y[0])
    oled.line(p2x[7],p2y[7],p2x[4],p2y[4])
    oled.line(p2x[3],p2y[3],p2x[7],p2y[7])
    oled.display()

def runExample():

    #  These three lines of code are all you need to initialize the
    #  OLED and print the splash screen.

    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.

    print("\nSparkFun Micro OLED Cube Example\n")
    myOLED = qwiic_micro_oled.QwiicMicroOled()

    if not myOLED.connected:
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


    while True:

        drawCube(myOLED)
        time.sleep(.01)



if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding OLED Cube Example")
        sys.exit(0)
