import MFRC522
import signal
import requests
import json
import time
import datetime

continue_reading = True
MIFAREReader = MFRC522.MFRC522()


def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    print('Ctrl+C captured, ending read.')
    MIFAREReader.GPIO_CLEEN()


def post_tag_data(data):
    url = 'http://0.0.0.0:80/api/user/session'
    r = requests.post(url, json=json.dumps(data), headers={'Content-type': 'application/json'})
    if r.status_code == requests.codes.ok or r.status_code == 200:
        print('Tag data posted to server...')
        print(r.json())


current_userId = -1

signal.signal(signal.SIGINT, end_read)

print('Reader active and awaiting input...')

while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print('Tag detected')
        (status, backData) = MIFAREReader.MFRC522_Anticoll()
        current_userId = int(str(backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(backData[4]))
        print('User ID: %s' % current_userId)
        user_data = {
            'user_id': str(current_userId),
            'timestamp': str(datetime.datetime.now())
        }
        post_tag_data(data=user_data)
        current_userId = -1
        time.sleep(5)
