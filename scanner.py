import pytesseract
import cv2
import time
import json
import urllib.request
import re

UPPER = 0
LOWER = 200
LEFT = 0
RIGHT = 1000

api_url = "https://api.scryfall.com/cards/named?fuzzy="

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    resized = frame[UPPER:LOWER, LEFT:RIGHT]

    cv2.imshow("frame", resized)

    text = pytesseract.image_to_string(resized)

    name = text.strip()

    words = name.split()
    url_ending = ""
    for word in words:
        url_ending += re.sub('[^A-Za-z0-9]+', '', word)+"-"
        url_ending = url_ending[:-1]

    if name != "":
        # print(f"'{url_ending}'")
        try:
            response = urllib.request.urlopen(api_url+url_ending)
            data = json.loads(response.read())
            if data["object"] == "card":
                print(data["name"])
            response.close()
        except:
            pass

    time.sleep(0.1)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
