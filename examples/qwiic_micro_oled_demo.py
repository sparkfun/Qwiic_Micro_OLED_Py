#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_micro_oled_demo.py
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
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:# www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
# Example - simple command to setup the OLED.
#

from __future__ import print_function, division
import qwiic_micro_oled
import time
import sys
import math
from random import randint

#-------------------------------------------------------------------
def pixelExample(myOLED):

    print("Pixels!")
    
    lWidth = myOLED.getLCDWidth()
    lHeight = myOLED.getLCDHeight()
    for i in range(128):
        myOLED.pixel(randint(0, lWidth), randint(0, lHeight))
        myOLED.display()

    myOLED.clear(myOLED.PAGE)
#-------------------------------------------------------------------
def lineExample(myOLED):

    middleX = myOLED.getLCDWidth() // 2
    middleY = myOLED.getLCDHeight() // 2

    lineWidth = min(middleX, middleY)
  
    print("Lines!")
  
    for i in range(2):

        for deg in range(0, 360, 15):

            xEnd = lineWidth * math.cos(deg * math.pi / 180.0)
            yEnd = lineWidth * math.sin(deg * math.pi / 180.0)
      
            myOLED.line(middleX, middleY, middleX + xEnd, middleY + yEnd)
            myOLED.display()
            time.sleep(.05)

        for deg in range(0, 360, 15): 

            xEnd = lineWidth * math.cos(deg * math.pi / 180.0)
            yEnd = lineWidth * math.sin(deg * math.pi / 180.0)
      
            myOLED.line(middleX, middleY, middleX + xEnd, middleY + yEnd, myOLED.BLACK, myOLED.NORM)
            myOLED.display()
            time.sleep(.05)
#-------------------------------------------------------------------
def shapeExample(myOLED):

    print("Shapes!")
  
    # Silly pong demo. It takes a lot of work to fake pong...
    paddleW = 3  # Paddle width
    paddleH = 15  # Paddle height

    lWidth = myOLED.getLCDWidth()
    lHeight = myOLED.getLCDHeight()

    # Paddle 0 (left) position coordinates
    paddle0_Y = (lHeight // 2) - (paddleH // 2)
    paddle0_X = 2

    # Paddle 1 (right) position coordinates
    paddle1_Y = (lHeight // 2) - (paddleH // 2)
    paddle1_X = lWidth - 3 - paddleW

    ball_rad = 2  #Ball radius
    # // Ball position coordinates
    ball_X = paddle0_X + paddleW + ball_rad
    ball_Y = randint(1 + ball_rad, lHeight - ball_rad) #paddle0_Y + ball_rad
    ballVelocityX = 1  # Ball left/right velocity
    ballVelocityY = 1  # Ball up/down velocity
    paddle0Velocity = -1  # Paddle 0 velocity
    paddle1Velocity = 1  # Paddle 1 velocity
    

    while (ball_X - ball_rad > 1) and (ball_X + ball_rad < lWidth - 2):
  
        # // Increment ball's position
        ball_X += ballVelocityX
        ball_Y += ballVelocityY
        # // Check if the ball is colliding with the left paddle
        if ball_X - ball_rad < paddle0_X + paddleW:

            # // Check if ball is within paddle's height
            if (ball_Y > paddle0_Y)  and (ball_Y < paddle0_Y + paddleH):
    
                ball_X +=1  # Move ball over one to the right
                ballVelocityX = -ballVelocityX # Change velocity

        # Check if the ball hit the right paddle
        if ball_X + ball_rad > paddle1_X:

            # Check if ball is within paddle's height
            if (ball_Y > paddle1_Y) and (ball_Y < paddle1_Y + paddleH):

                ball_X -= 1  # Move ball over one to the left
                ballVelocityX = -ballVelocityX # change velocity

        # // Check if the ball hit the top or bottom
        if (ball_Y <= ball_rad) or (ball_Y >= (lHeight - ball_rad - 1)):

            # Change up/down velocity direction
            ballVelocityY = -ballVelocityY

        # // Move the paddles up and down
        paddle0_Y += paddle0Velocity
        paddle1_Y += paddle1Velocity

        # // Change paddle 0's direction if it hit top/bottom
        if (paddle0_Y <= 1) or (paddle0_Y > lHeight - 2 - paddleH):

            paddle0Velocity = -paddle0Velocity

        # // Change paddle 1's direction if it hit top/bottom
        if (paddle1_Y <= 1) or (paddle1_Y > lHeight - 2 - paddleH):

            paddle1Velocity = -paddle1Velocity
    
        # Draw the Pong Field
        myOLED.clear(myOLED.PAGE)  # Clear the page

        # Draw an outline of the screen:
        myOLED.rect(0, 0, lWidth - 1, lHeight)

        # Draw the center line
        myOLED.rectFill(lWidth//2 - 1, 0, 2, lHeight)

        # Draw the Paddles:
        myOLED.rectFill(paddle0_X, paddle0_Y, paddleW, paddleH)
        myOLED.rectFill(paddle1_X, paddle1_Y, paddleW, paddleH)

        # # Draw the ball:
        myOLED.circle(ball_X, ball_Y, ball_rad)

        # Actually draw everything on the screen:
        myOLED.display()
        time.sleep(.01)  # Delay for visibility

    time.sleep(.2)

#-------------------------------------------------------------------
def textExamples(myOLED):

    print("Text!")
    
    # Demonstrate font 0. 5x8 font
    myOLED.clear(myOLED.PAGE)     # Clear the screen
    myOLED.setFontType(0)  # Set font to type 0
    myOLED.setCursor(0, 0) # Set cursor to top-left
    # There are 255 possible characters in the font 0 type.
    # Lets run through all of them and print them out!
    for i in range(256):

        # You can write byte values and they'll be mapped to
        # their ASCII equivalent character.
        myOLED.write(i)  # Write a byte out as a character
        myOLED.display() # Draw on the screen
        # time.sleep(.05)

        # We can only display 60 font 0 characters at a time.
        # Every 60 characters, pause for a moment. Then clear
        # the page and start over.
        if (i%60 == 0) and (i != 0):

            time.sleep(.1)
            myOLED.clear(myOLED.PAGE)     # Clear the page
            myOLED.setCursor(0, 0) # Set cursor to top-left

    time.sleep(.5) # Wait 500ms before next example
    
    # Demonstrate font 1. 8x16. Let's use the print function
    # to display every character defined in this font.
    myOLED.setFontType(1)  # Set font to type 1
    myOLED.clear(myOLED.PAGE)     # Clear the page
    myOLED.setCursor(0, 0) # Set cursor to top-left
    # Print can be used to print a string to the screen:
    myOLED.print(" !\"#$%&'()*+,-./01234")
    myOLED.display()       # Refresh the display
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("56789:<=>?@ABCDEFGHI")
    myOLED.display()
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("JKLMNOPQRSTUVWXYZ[\\]^")
    myOLED.display()
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("_`abcdefghijklmnopqrs")
    myOLED.display()
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("tuvwxyz{|}~")
    myOLED.display()
    time.sleep(1)    

    # Demonstrate font 2. 10x16. Only numbers and '.' are defined. 
    # This font looks like 7-segment displays.
    # Lets use this big-ish font to display readings from the
    # analog pins.
    for i in range(25):

        myOLED.clear(myOLED.PAGE)            # Clear the display
        myOLED.setCursor(0, 0)        # Set cursor to top-left
        myOLED.setFontType(0)         # Smallest font
        myOLED.print("A0: ")          # Print "A0"
        myOLED.setFontType(2)         # 7-segment font
        myOLED.print("%.3d" % randint(0,255))

        myOLED.setCursor(0, 16)       # Set cursor to top-middle-left
        myOLED.setFontType(0)         # Repeat
        myOLED.print("A1: ")
        myOLED.setFontType(2)

        myOLED.print("%.3d" % randint(0,255))
        myOLED.setCursor(0, 32)
        myOLED.setFontType(0)
        myOLED.print("A2: ")
        myOLED.setFontType(2)
        myOLED.print("%.3d" % randint(0,255))     

        myOLED.display()
        time.sleep(.1)

    # Demonstrate font 3. 12x48. Stopwatch demo.
    myOLED.setFontType(3)  # Use the biggest font
    ms = 0
    s = 0
    
    while s <= 5:

        myOLED.clear(myOLED.PAGE)     # Clear the display
        myOLED.setCursor(0, 0) # Set cursor to top-left
        if s < 10:
            myOLED.print("00")   # Print "00" if s is 1 digit
        elif s < 100:     
            myOLED.print("0")    # Print "0" if s is 2 digits

        myOLED.print(s)        # Print s's value
        myOLED.print(":")      # Print ":"
        myOLED.print(ms)       # Print ms value
        myOLED.display()       # Draw on the screen
        ms +=1         # Increment ms
        if ms >= 10 : #If ms is >= 10
            ms = 0     # Set ms back to 0
            s +=1        # and increment s
    
    # Demonstrate font 4. 31x48. Let's use the print function
    # to display some characters defined in this font.
    myOLED.setFontType(4)  # Set font to type 4
    myOLED.clear(myOLED.PAGE)     #Clear the page
    myOLED.setCursor(0, 0) #Set cursor to top-left

    # Print can be used to print a string to the screen:
    myOLED.print("OL")
    myOLED.display()       # Refresh the display
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("ED")
    myOLED.display()
    time.sleep(1)

    myOLED.setFontType(1)
    myOLED.clear(myOLED.PAGE)
    myOLED.setCursor(0, 0)
    myOLED.print("DONE!")
    myOLED.display()
    time.sleep(1)


#-------------------------------------------------------------------

def runExample():

    #  These three lines of code are all you need to initialize the
    #  OLED and print the splash screen.
  
    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.


    print("\nSparkFun Micro OLED Everything Example\n")
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
    time.sleep(1)

    myOLED.clear(myOLED.PAGE)

    print("-"*30)
    pixelExample(myOLED)
    print("-"*30)    
    lineExample(myOLED)
    print("-"*30)    
    shapeExample(myOLED)
    print("-"*30)    
    textExamples(myOLED)
    print("-"*30)
    print("DONE")    

#-------------------------------------------------------------------

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding OLED Everything Example")
        sys.exit(0)
