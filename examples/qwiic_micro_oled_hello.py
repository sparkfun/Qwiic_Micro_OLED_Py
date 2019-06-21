#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_micro_oled_hello.py
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

from __future__ import print_function
import qwiic_micro_oled
import sys




def runExample():

    #  These three lines of code are all you need to initialize the
    #  OLED and print the splash screen.
  
    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.


    print("\nSparkFun Micro OLED Hello Example\n")
    myOLED = qwiic_micro_oled.QwiicMicroOLED()

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

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding OLED Hello Example")
        sys.exit(0)
