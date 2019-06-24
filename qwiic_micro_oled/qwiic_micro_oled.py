#-----------------------------------------------------------------------------
# qwiic_micro_oled.py
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https:= www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:= www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
from __future__ import print_function
import sys

import qwiic_i2c

from . import moled_fonts as mfonts
import math

# Define the device name and I2C addresses. These are set in the class defintion 
# as class variables, making them avilable without having to create a class instance.
#
# The base class and associated support functions use these class varables to 
# allow users to easily identify connected devices as well as provide basic 
# device services.
#
# The name of this device - note this is private 
_DEFAULT_NAME = "Qwiic Micro OLED"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x3D, 0x3C]


# The defines from the OLED Aurdino library

I2C_COMMAND = 0x00
I2C_DATA = 0x40

LCDWIDTH			= 64
LCDHEIGHT			= 48
FONTHEADERSIZE		= 6


WIDGETSTYLE0			= 0
WIDGETSTYLE1			= 1
WIDGETSTYLE2			= 2

SETCONTRAST 		= 0x81
DISPLAYALLONRESUME 	= 0xA4
DISPLAYALLON 		= 0xA5
NORMALDISPLAY 		= 0xA6
INVERTDISPLAY 		= 0xA7
DISPLAYOFF 			= 0xAE
DISPLAYON 			= 0xAF
SETDISPLAYOFFSET 	= 0xD3
SETCOMPINS 			= 0xDA
SETVCOMDESELECT		= 0xDB
SETDISPLAYCLOCKDIV 	= 0xD5
SETPRECHARGE 		= 0xD9
SETMULTIPLEX 		= 0xA8
SETLOWCOLUMN 		= 0x00
SETHIGHCOLUMN 		= 0x10
SETSTARTLINE 		= 0x40
MEMORYMODE 			= 0x20
COMSCANINC 			= 0xC0
COMSCANDEC 			= 0xC8
SEGREMAP 			= 0xA0
CHARGEPUMP 			= 0x8D
EXTERNALVCC 		= 0x01
SWITCHCAPVCC 		= 0x02

#  Scroll
ACTIVATESCROLL 					= 0x2F
DEACTIVATESCROLL 				= 0x2E
SETVERTICALSCROLLAREA 			= 0xA3
RIGHTHORIZONTALSCROLL 			= 0x26
LEFT_HORIZONTALSCROLL 			= 0x27
VERTICALRIGHTHORIZONTALSCROLL	= 0x29
VERTICALLEFTHORIZONTALSCROLL	= 0x2A


# Define a function to Init a screen buffer that is setup for the sparkfun OLED.
# This is copied from the Arduino lib.

def _setSplashScreen(screenbuffer):

	# # LCD Memory organised in 64 horizontal pixel and 6 rows of byte
	#  B  B .............B  -----
	#  y  y .............y        \
	#  t  t .............t         \
	#  e  e .............e          \
	#  0  1 .............63          \
	#                                 \
	#  D0 D0.............D0            \
	#  D1 D1.............D1            / ROW 0
	#  D2 D2.............D2           /
	#  D3 D3.............D3          /
	#  D4 D4.............D4         /
	#  D5 D5.............D5        /
	#  D6 D6.............D6       /
	#  D7 D7.............D7  ----
	# */
	# SparkFun Electronics LOGO

	screenbuffer[:] = [\
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE0, 0xF8, 0xFC, 0xFE, 0xFF, 0xFF, 0xFF, 0xFF, \
		0xFF, 0xFF, 0xFF, 0x0F, 0x07, 0x07, 0x06, 0x06, 0x00, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x81, 0x07, 0x0F, 0x3F, 0x3F, 0xFF, 0xFF, 0xFF, \
		0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0xFE, 0xFC, 0xFC, 0xFC, 0xFE, 0xFF, 0xFF, 0xFF, 0xFC, 0xF8, 0xE0, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC, \
		0xFE, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF1, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xF0, 0xFD, 0xFF, \
		0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, \
		0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, \
		0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x3F, 0x1F, 0x07, 0x01, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, \
		0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x3F, 0x1F, 0x1F, 0x0F, 0x0F, 0x0F, 0x0F, \
		0x0F, 0x0F, 0x0F, 0x0F, 0x07, 0x07, 0x07, 0x03, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, \
		0x7F, 0x3F, 0x1F, 0x0F, 0x07, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported 
# from this module.

class QwiicMicroOled(object):

	# Constructor
	device_name = _DEFAULT_NAME
	available_addresses = _AVAILABLE_I2C_ADDRESS

	# user exposed constants
	BLACK = 0
	WHITE = 1

	NORM				= 0
	XOR					= 1

	PAGE				= 0
	ALL					= 1


	def __init__(self, address=None):


		self.address = address if address != None else self.available_addresses[0]
		
		# load the I2C driver

		self._i2c = qwiic_i2c.getI2CDriver()
		if self._i2c == None:
			print("Unable to load I2C driver for this platform.")
			return

		# define the screen buffer - since this is a two color display, only bits are used
		# So the height is 8  bits / byte or LCDHEIGHT/8

		# self._screenbuffer = bytearray(LCDWIDTH * int(math.ceil(LCDHEIGHT/8.)))
		self._screenbuffer = [0] * (LCDWIDTH * int(math.ceil(LCDHEIGHT/8.)))
		# Set initial contents
		_setSplashScreen(self._screenbuffer)

		self.cursorX = 0
		self.cursorY = 0

		self.foreColor = self.WHITE
		self.drawMode  = self.NORM

		# self.fontWidth = 0
		# self.fontHeight = 0
		# self.fontStartChar = 0
		# self.fontTotalChar = 0
		self.fontType = 0
		# self.fontData = None
		self._font = None

		self.nFonts = mfonts.count()


	def isConnected(self):
		return qwiic_i2c.isDeviceConnected(self.address)

	def begin(self):

		self.setFontType(0)
		self.setColor(self.WHITE)
		self.setDrawMode(self.NORM)
		self.setCursor(0,0)

		#  Display Init sequence for 64x48 OLED module
		self._i2c.writeByte(self.address, I2C_COMMAND, DISPLAYOFF)			#  0xAE

		self._i2c.writeByte(self.address, I2C_COMMAND, SETDISPLAYCLOCKDIV)	#  0xD5
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x80)					#  the suggested ratio 0x80
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETMULTIPLEX)			#  0xA8
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x2F)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETDISPLAYOFFSET)		#  0xD3
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x0)					#  no offset
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETSTARTLINE | 0x0)	#  line #0
		
		self._i2c.writeByte(self.address, I2C_COMMAND, CHARGEPUMP)			#  enable charge pump
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x14)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, NORMALDISPLAY)			#  0xA6
		self._i2c.writeByte(self.address, I2C_COMMAND, DISPLAYALLONRESUME)	#  0xA4
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SEGREMAP | 0x1)
		self._i2c.writeByte(self.address, I2C_COMMAND, COMSCANDEC)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETCOMPINS)			#  0xDA
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x12)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETCONTRAST)			#  0x81
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x8F)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETPRECHARGE)			#  0xd9
		self._i2c.writeByte(self.address, I2C_COMMAND, 0xF1)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, SETVCOMDESELECT)			#  0xDB
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x40)
		
		self._i2c.writeByte(self.address, I2C_COMMAND, DISPLAYON)				# --turn on oled panel
		self.clear(self.ALL)						#  Erase hardware memory inside the OLED controller to aself random data in memory.

	#----------------------------------------------------
	# brief Set SSD1306 page address.
	#     Send page address command and address to the SSD1306 OLED controller.

	def setPageAddress(self, add):

		self._i2c.writeByte(self.address, I2C_COMMAND, 0xb0|add)

	#----------------------------------------------------
    # Send column address command and address to the SSD1306 OLED controller.
	def setColumnAddress(self, add):
		self._i2c.writeByte(self.address, I2C_COMMAND, (0x10|(add>>4))+0x02)
		self._i2c.writeByte(self.address, I2C_COMMAND, (0x0f&add))

	#----------------------------------------------------
	#  To clear GDRAM inside the LCD controller, pass in the variable mode = ALL and to clear screen page buffer pass in the variable mode = PAGE.

	def clear(self,  mode, value=0):

		if mode == self.ALL:
			for i in range(8):
				self.setPageAddress(i)
				self.setColumnAddress(0)
				for j in range(0x80):
					self._i2c.writeByte(self.address, I2C_DATA, value)
		else:
			self._screenbuffer[:] = [value]*len(self._screenbuffer)

    # The WHITE color of the display will turn to BLACK and the BLACK will turn to WHITE.

	def invert(self, inv):
		if inv:
			self._i2c.writeByte(self.address, I2C_COMMAND, INVERTDISPLAY)
		else:
			self._i2c.writeByte(self.address, I2C_COMMAND, NORMALDISPLAY)

	# OLED contract value from 0 to 255. Note: Contrast level is not very obvious.

	def contrast(self, contrast): 
		self._i2c.writeByte(self.address, I2C_COMMAND, SETCONTRAST)		#  0x81
		self._i2c.writeByte(self.address, I2C_COMMAND, contrast)

    # Bulk move the screen buffer to the SSD1306 controller's memory so that images/graphics drawn on the screen buffer will be displayed on the OLED.

	def display(self):

		# the I2C library being used allows blocks upto 32 ints to be sent at a time. 
		# 
		# The screenbuffer is sliced into 32 int blocks and set. This results in a faster 
		# refresh than ported method (update a pixel at a time ...)
		#
		lenBlock = 32
		lenLine = self.getLCDWidth()		
		nBlocks = int(math.ceil(lenLine/lenBlock))

		for i in range(6):

			self.setPageAddress(i)
			lineStart = i * lenLine  # offset in the screen buffer for the current line/row

			for iBlock in range(nBlocks):

				iStart = iBlock * lenBlock
				self.setColumnAddress(iStart)
				iEnd = iStart  + min(lenLine - iStart, lenBlock) # what's left - not > 32 in len

				# Send the block - take into account the current line/row offset
				self._i2c.writeBlock(self.address, I2C_DATA, self._screenbuffer[lineStart+iStart:lineStart+iEnd])				
	
	#     Leftover from port -> Arduino's print overridden so that we can use uView.print().

	def write(self, c):

		if c == '\n':
			# self.cursorY += self.fontHeight
			self.cursorY += self._font.height			
			self.cursorX  = 0
		elif c != '\r' :
			self.drawChar(self.cursorX, self.cursorY, c)
			self.cursorX += self._font.width+1
			if self.cursorX > (LCDWIDTH - self._font.width):
				self.cursorY += self._font.height
				self.cursorX = 0
	
		return 1

	def print(self, text):

		# a list or array? If not, make it one
		if not hasattr(text, '__len__'): # scalar?
			text = str(text)

		if type(text) == str:
			text = bytearray(text, encoding='ascii')

		for i in range(len(text)):
			self.write(text[i])



	# MicroOLED's cursor position to x,y.

	def setCursor(self,  x,  y):
		self.cursorX = x
		self.cursorY = y

	# Draw color pixel in the screen buffer's x,y position with NORM or XOR draw mode.

	def pixel(self, x, y, color=None,  mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		if  x < 0 or  x >= LCDWIDTH or y < 0 or y >= LCDHEIGHT:
			return

		x = int(x)
		y = int(y)
		index = x + (y//8)*LCDWIDTH

		if mode == self.XOR:
			if color == self.WHITE:
				self._screenbuffer[index] ^= (1 << (y%8))

		else:
			if color == self.WHITE:
				self._screenbuffer[index] |= (1 << (y%8))
			else:
				self._screenbuffer[index] &= (~(1 << (y%8)) & 0xff)

	#  Draw line using color and mode from x0,y0 to x1,y1 of the screen buffer.

	def line(self, x0, y0, x1, y1, color=None, mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			# swap
			(x0, y0) = (y0, x0)
			(x1, y1) = (y1, x1)

		if x0 > x1:
			# swap
			(x0, x1) = (x1, x0)
			(y0, y1) = (y1, y0)

		dx = x1 - x0
		dy = abs(y1 - y0)

		err = dx // 2

		ystep = 1 if y0 < y1 else -1
			

		while x0 < x1:

			if steep:
				self.pixel(y0, x0, color, mode)			
			else:
				self.pixel(x0, y0, color, mode)	
				
			err -= dy
			if err < 0 : 
				y0 += ystep
				err += dx
			x0 += 1
	
	# Draw horizontal line using color and mode from x,y to x+width,y of the screen buffer.

	def lineH(self, x, y, width, color=None, mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		self.line( x, y, x+width, y, color, mode)


	# Draw vertical line using color and mode from x,y to x,y+height of the screen buffer.

	def lineV(self, x, y, height, color=None, mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		self.line(x, y, x, y+height, color, mode)

	# Draw rectangle using color and mode from x,y to x+width,y+height of the screen buffer.
	
	def rect(self, x,  y, width, height, color=None, mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		self.lineH(x, y, width, color, mode)
		self.lineH(x, y+height-1, width, color, mode)

		tempHeight = height-2

		# skip drawing vertical lines to aself overlapping of pixel that will
		# affect XOR plot if no pixel in between horizontal lines
		if tempHeight < 1:
			return

		self.lineV(x, y+1, tempHeight, color, mode)
		self.lineV(x+width-1, y+1, tempHeight, color, mode)

	#  Draw filled rectangle using color and mode from x,y to x+width,y+height of the screen buffer.
	
	def rectFill(self, x, y, width, height, color=None,  mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		# // TODO - need to optimise the memory map draw so that this function will not call pixel one by one
		for i in range(x, x+width):
			self.lineV(i, y, height, color, mode)

	# Draw circle with radius using color and mode at x,y of the screen buffer.
	
	def circle(self, x0, y0, radius, color=None, mode=None):

		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode

		#TODO - find a way to check for no overlapping of pixels so that XOR draw mode will work perfectly
		f = 1 - radius
		ddF_x = 1
		ddF_y = -2 * radius
		x = 0
		y = radius
	
		self.pixel(x0, y0+radius, color, mode)
		self.pixel(x0, y0-radius, color, mode)
		self.pixel(x0+radius, y0, color, mode)
		self.pixel(x0-radius, y0, color, mode)
	
		while x < y: 
			if f >= 0: 
				y -= 1
				ddF_y += 2
				f += ddF_y
	
			x += 1
			ddF_x += 2
			f += ddF_x
	
			self.pixel(x0 + x, y0 + y, color, mode)
			self.pixel(x0 - x, y0 + y, color, mode)
			self.pixel(x0 + x, y0 - y, color, mode)
			self.pixel(x0 - x, y0 - y, color, mode)
	
			self.pixel(x0 + y, y0 + x, color, mode)
			self.pixel(x0 - y, y0 + x, color, mode)
			self.pixel(x0 + y, y0 - x, color, mode)
			self.pixel(x0 - y, y0 - x, color, mode)	

	# The height of the LCD return as byte.
	
	def getLCDHeight(self):
		return LCDHEIGHT
	
	# The width of the LCD return as byte.

	def getLCDWidth(self):
		return LCDWIDTH

	# The cucrrent font's width return as byte.
	
	def getFontWidth(self):
		return self._font.width
	
	# The current font's height return as byte.
	
	def getFontHeight(self):
		return self._font.height
	
	# Return the starting ASCII character of the currnet font, not all fonts start with ASCII character 0. Custom fonts can start from any ASCII character.

	def getFontStartChar(self):
		return self._font.start_char
	
	# Return the total characters of the current font.

	def getFontTotalChar(self):
		return self._font.total_char
	
	
	# Return the total number of fonts loaded into the MicroOLED's flash memory.

	def getTotalFonts(self):
		return TOTALFONTS
	
	# Return the font type number of the current font.
	def getFontType(self):
		return self.fontType

 	# Set the current font type number, ie changing to different fonts base on the type provided.

	def setFontType(self, type):

		if type >= self.nFonts or type < 0:
			return False
	
		self.fontType=type
		self._font = mfonts.get_font(type)
		if self._font == None:
			return False;

		return True

	# Set the current draw's color. Only WHITE and BLACK available.

	def setColor(self, color):
		self.foreColor = color

	# Set current draw mode with NORM or XOR.

	def setDrawMode(self, mode):
		self.drawMode = mode

	# Draw character c using color and draw mode at x,y.
	
	def drawChar(self, x, y, c, color=None, mode=None):
		
		if color == None:
			color = self.foreColor

		if mode == None:
			mode = self.drawMode
	
		if self._font == None:
			return

		if c < self._font.start_char or c > (self._font.start_char + self._font.total_char - 1): # no bitmap for the required c
			return
	
		tempC = c - self._font.start_char
	
		# // each row (in datasheet is call page) is 8 bits high, 16 bit high character will have 2 rows to be drawn
		rowsToDraw = self._font.height//8	# 8 is LCD's page size, see SSD1306 datasheet
		
		if rowsToDraw <= 1: 
			rowsToDraw=1

		# figure out position of the character in the font map. integer math is key here
		charPerRow = self._font.map_width // self._font.width 	

		rowPos = tempC // charPerRow  # the number of full rows to skip
		colPos = tempC % charPerRow # the number of chars into the last 
		iStart =  rowPos * charPerRow * self._font.height//8 + colPos

		# each row on LCD is 8 bit height (see datasheet for explanation)
		for row in range(rowsToDraw):

			# load in the current character block. 
			fBuffer =  self._font[iStart + row * charPerRow]
			for i in range(len(fBuffer)):

				for j in range(8):	# 8 is the LCD's page height (see datasheet for explanation)

					self.pixel(x+i, y+j + (row*8), \
						color if fBuffer[i] & 0x01 << j else (~color & 0xFF), \
						mode)
	
	def scrollStop(self):

		self._i2c.writeByte(self.address, I2C_COMMAND, DEACTIVATESCROLL)


	# Set row start to row stop on the OLED to scroll right. Refer to http://learn.microview.io/intro/general-overview-of-microview.html for explanation of the rows.
	
	def scrollRight(self,  start, stop):

		if stop < start:		# stop must be larger or equal to start
			return
		
		self.scrollStop()		# need to disable scrolling before starting to avoid memory corrupt

		self._i2c.writeByte(self.address, I2C_COMMAND, RIGHTHORIZONTALSCROLL)
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x00)
		self._i2c.writeByte(self.address, I2C_COMMAND, start)
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x7)		# scroll speed frames , TODO
		self._i2c.writeByte(self.address, I2C_COMMAND, stop)
		self._i2c.writeByte(self.address, I2C_COMMAND, 0x00)
		self._i2c.writeByte(self.address, I2C_COMMAND, 0xFF)
		self._i2c.writeByte(self.address, I2C_COMMAND, ACTIVATESCROLL)

	
	# Flip the graphics on the OLED vertically.
	
	def flipVertical(self, flip):

		self._i2c.writeByte(self.address, I2C_COMMAND, COMSCANINC if flip else COMSCANDEC)

	
	
	# Flip the graphics on the OLED horizontally.
	
	def flipHorizontal(self, flip):

		self._i2c.writeByte(self.address, I2C_COMMAND, SEGREMAP | ( 0x0 if flip else 0x1))

	# Return a pointer to the start of the RAM screen buffer for direct access.
	def getScreenBuffer(self):
		self._screenbuffer
	
	
	# Draw Bitmap image on screen. The array for the bitmap can be stored in the Arduino file, so user don't have to mess with the library files.
	# To use, create uint8_t array that is 64x48 pixels (384 bytes). Then call .drawBitmap and pass it the array.

	def drawBitmap(self, bitArray):
	
		if len(bitArray) != len(self._screenbuffer):
			print("drawBitmap - Invalid Input size.", file-sys.stderr)
			return

		self._screenbuffer[:] = bitArray
