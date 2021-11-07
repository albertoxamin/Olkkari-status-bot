import urllib.request
import numpy as np
import requests
import time
import cv2
import os

if not os.environ.get('TELEGRAM_BOT_TOKEN'):
    print('Please set the TELEGRAM_BOT_TOKEN environment variable')
    exit(1)

def telegram_bot_sendtext(bot_message):
   bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
   bot_chatID = '@olkkaristatus'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   return response.json()

def get_image():
    req = urllib.request.urlopen(f'https://athene.fi/olocam/latest.jpg?{int(round(time.time() * 1000))}')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr, -1)

def loop():
    last_open = False
    diff_count = 0
    while True:
        img = get_image()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if np.mean(img) > 90:
            if not last_open:
                diff_count += 1
                if diff_count > 5:
                    print('Open')
                    telegram_bot_sendtext('🟢🟢🟢 now *open* 🟢🟢🟢')
                    last_open = True
                    diff_count = 0
        else:
            if last_open:
                diff_count += 1
                if diff_count > 5:
                    print('Closed')
                    telegram_bot_sendtext('❌❌ now *closed* ❌❌')
                    last_open = False
                    diff_count = 0
        time.sleep(5)

if __name__ == '__main__':
    loop()

