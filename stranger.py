import time
import datetime
import dataset
import json
import settings
from twython import TwythonStreamer
from neopixel import *
from webcolors import *
from sqlalchemy.exc import ProgrammingError

db = dataset.connect(settings.CONNECTION_STRING)

# Letter to LED configuration:
ledAddress = {'A':50, \
           'B':53, \
           'C':56, \
           'D':58, \
           'E':61, \
           'F':65, \
           'G':68, \
           'H':71, \
           'I':100, \
           'J':98, \
           'K':95, \
           'L':92, \
           'M':89, \
           'N':86, \
           'O':83, \
           'P':80, \
           'Q':75, \
           'R':107, \
           'S':110, \
           'T':112, \
           'U':116, \
           'V':118, \
           'W':122, \
           'X':126, \
           'Y':129, \
           'Z':132, }

# LED colors:
xmasColor = ['red', 'yellow', 'green', 'cornflowerblue', \
        'darkorange','magenta']

letterColor = {'A':'red', \
           'B':'yellow', \
           'C':'lime', \
           'D':'cornflowerblue', \
           'E':'darkorange', \
           'F':'magenta', \
           'G':'red', \
           'H':'orange', \
           'I':'yellow', \
           'J':'green', \
           'K':'blue', \
           'L':'purple', \
           'M':'red', \
           'N':'orange', \
           'O':'yellow', \
           'P':'green', \
           'Q':'blue', \
           'R':'purple', \
           'S':'red', \
           'T':'orange', \
           'U':'yellow', \
           'V':'green', \
           'W':'blue', \
           'X':'purple', \
           'Y':'red', \
           'Z':'orange' }

gammaTable = [int(pow(float(i) / 255.0, 2.8) * 255.0) for i in range(256)]

# Setup callbacks from Twython Streamer
class twitterStream(TwythonStreamer):

    def on_success(self, data):
        
        tweet_id = data['id']
        tweet_author = data['user']['screen_name']
        tweet_fullname = data['user']['name']
        tweet_timestamp = float(data['timestamp_ms'])
        tweet_friendscount = data['user']['friends_count']
        tweet_text = data['text']
        tweet_convertedtime = datetime.datetime.fromtimestamp(tweet_timestamp/1000.0)


        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
                tweet_id=tweet_id,
                author=tweet_author,
                name=tweet_fullname,
                time=tweet_convertedtime,
                friends=tweet_friendscount,
                text=tweet_text,
            ))
        
        except ProgrammingError as err:
            print(err)

        if 'text' in data:
            print data['text'].encode('utf-8')
            newtweet = data['text'].encode('utf-8')
            newtweet = newtweet.lower()
            newtweet = newtweet.replace(TERMS, '')
            theaterChase(strip, Color(255,255,255))
            xmasChase(strip)
            textToLedAddress(newtweet)
            xmasFade(strip, 30)

    def on_error(self, status_code, data):
        print status_code

# Parse string and set LEDs
def textToLedAddress(word):
        for i in word:
            if i.isalpha():
                letter = ledAddress.get(i.upper())
                print(letter)
                
                currentColor = name_to_rgb(letterColor.get(i.upper()))
                colorR = gammaTable[currentColor[0]]
                colorG = gammaTable[currentColor[1]]
                colorB = gammaTable[currentColor[2]]
                print(letterColor.get(i.upper()))
                print(currentColor)
                print(colorR)
                print(colorG)
                print(colorB)

                strip.setPixelColor(letter, Color(colorG,colorR,colorB))
                strip.setBrightness(255)
                strip.show()
                time.sleep(1)
                strip.setPixelColor(letter, Color(0,0,0))
                strip.show()
                time.sleep(.5)

# Define functions which animate LEDs in various ways.
def lightLetter(position, color):
        strip.setPixelColor(position, color)
        strip.show()

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        currentColor = name_to_rgb(color)
        colorR = gammaTable[currentColor[0]]
        colorG = gammaTable[currentColor[1]]
        colorB = gammaTable[currentColor[2]]

        strip.setPixelColor(i, Color(colorG,colorR,colorB))
        strip.show()
        time.sleep(wait_ms/1000.0)

def xmasWipe(strip, wait_ms=50):
    j = 0
    for i in range(strip.numPixels()):
        currentColor = name_to_rgb(xmasColor[j])
        colorR = gammaTable[currentColor[0]]
        colorG = gammaTable[currentColor[1]]
        colorB = gammaTable[currentColor[2]]

        strip.setPixelColor(i, Color(colorG, colorR, colorB))
        strip.setBrightness(80)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if j < 5:
            j += 1
        else:
            j = 0

def xmasFade(strip, brightness, wait_ms=50):
    c = 0
    for i in range(brightness):
        for j in range(strip.numPixels()):
            currentColor = name_to_rgb(xmasColor[c])
            colorR = gammaTable[currentColor[0]]
            colorG = gammaTable[currentColor[1]]
            colorB = gammaTable[currentColor[2]]
            strip.setPixelColor(j, Color(colorG, colorR, colorB))
            if c < 5:
                c += 1
            else:
                c = 0
        strip.setBrightness(i)
        strip.show()
        time.sleep(wait_ms/1000.0)


def xmasChase(strip, wait_ms=50):
    j=0
    for i in range(strip.numPixels()):
        currentColor = name_to_rgb(xmasColor[j])
        colorR = gammaTable[currentColor[0]]
        colorG = gammaTable[currentColor[1]]
        colorB = gammaTable[currentColor[2]]

        strip.setPixelColor(i, Color(colorG, colorR, colorB))
        strip.setPixelColor(i-1, Color(0,0,0))
        if i == 149:
            strip.setPixelColor(i, Color(0,0,0))
        strip.setBrightness(255)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if j < 5:
            j += 1
        else:
            j = 0


def theaterChase(strip, color, wait_ms=50, iterations=10):
# Movie theater light style chaser animation.
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
# Generate rainbow colors across 0-255 positions.
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
# Draw rainbow that fades across all pixels at once.
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
# Draw rainbow that uniformly distributes itself across all pixels.
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
# Rainbow movie theater light style chaser animation.
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def clearWipe(strip, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def resetStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

# Main program logic follows:
if __name__ == '__main__':
	strip = Adafruit_NeoPixel(settings.LED_COUNT, settings.LED_PIN, settings.LED_FREQ_HZ, settings.LED_DMA, settings.LED_INVERT, settings.LED_BRIGHTNESS, settings.LED_CHANNEL, settings.LED_STRIP)
	strip.begin()

	print ('Press Ctrl-C to quit.')
        
        xmasFade(strip, 30)

        try:
            stream = twitterStream(settings.APP_KEY, settings.APP_SECRET, settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
            tweet = stream.statuses.filter(track=settings.TERMS)

        except KeyboardInterrupt:
            resetStrip(strip)
#            result = db[settings.TABLE_NAME].all()
#            dataset.freeze(result, format='csv', filename=settings.CSV_NAME)
