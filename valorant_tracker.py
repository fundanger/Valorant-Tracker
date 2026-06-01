import urllib.request
import re
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import time, sleep


def find_nth(haystack, needle, n):
    """Return the index of the nth occurrence of needle in haystack."""
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def cleanNum(rawNum):
    """Strip non-numeric characters from a parsed stat string."""
    return re.sub(r"\D", "", rawNum)


def getOutputData(user, tagline):
    """Fetch the Tracker.gg profile page and return it as a string."""
    user_agent = "Valorant Tracker Bot"
    headers = {"User-Agent": user_agent}
    url = (
        "https://tracker.gg/valorant/profile/riot/"
        + user
        + "%23"
        + tagline
        + "/overview?playlist=competitive.html"
    )
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    return str(response.read())


def loop(output):
    mcp.output(3, 1)
    lcd.begin(16, 2)
    currentTime = int(time())

    numOfMatches = cleanNum(output[find_nth(output, "matchesPlayed", 0) + 125:
                                   find_nth(output, "matchesPlayed", 0) + 150])
    numOfWins = cleanNum(output[find_nth(output, "Wins", 0):
                                find_nth(output, "Wins", 0) + 78])
    numOfLosses = cleanNum(output[find_nth(output, "Losses", 0):
                                  find_nth(output, "Losses", 0) + 78])

    numOfUnratedMatches = cleanNum(output[find_nth(output, "matchesPlayed", 5) + 125:
                                          find_nth(output, "matchesPlayed", 5) + 150])
    numOfUnratedWins = cleanNum(output[find_nth(output, "Wins", 5):
                                       find_nth(output, "Wins", 5) + 78])
    numOfUnratedLosses = cleanNum(output[find_nth(output, "Losses", 5):
                                         find_nth(output, "Losses", 5) + 78])

    while True:
        if (int(time()) - currentTime) >= 180:
            output = getOutputData("username", "tagline")  # Change username and tagline here

            numOfMatches = cleanNum(output[find_nth(output, "matchesPlayed", 0) + 125:
                                           find_nth(output, "matchesPlayed", 0) + 150])
            numOfWins = cleanNum(output[find_nth(output, "Wins", 0):
                                        find_nth(output, "Wins", 0) + 78])
            numOfLosses = cleanNum(output[find_nth(output, "Losses", 0):
                                          find_nth(output, "Losses", 0) + 78])

            numOfUnratedMatches = cleanNum(output[find_nth(output, "matchesPlayed", 5) + 125:
                                                  find_nth(output, "matchesPlayed", 5) + 150])
            numOfUnratedWins = cleanNum(output[find_nth(output, "Wins", 5):
                                               find_nth(output, "Wins", 5) + 78])
            numOfUnratedLosses = cleanNum(output[find_nth(output, "Losses", 5):
                                                 find_nth(output, "Losses", 5) + 78])

            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.message("Updating Stats")
            sleep(5)
            currentTime = time()

        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.message("Competitive: ")
        lcd.setCursor(3, 1)
        lcd.message(numOfMatches + "/" + numOfWins + "/" + numOfLosses)
        sleep(5)

        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.message("Unrated Stats: ")
        lcd.setCursor(3, 1)
        lcd.message(numOfUnratedMatches + "/" + numOfUnratedWins + "/" + numOfUnratedLosses)
        sleep(5)


# I2C address of the PCF8574 chip
PCF8574_address = 0x27
PCF8574A_address = 0x3F

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print("I2C Address Error!")
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

output = getOutputData("username", "tagline")  # Change username and tagline here

if __name__ == "__main__":
    print("Program is starting...")
    try:
        loop(output)
    except KeyboardInterrupt:
        lcd.clear()
