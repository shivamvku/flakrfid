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
    print("Ctrl+C captured, ending read.")
    MIFAREReader.GPIO_CLEEN()


def post_tag_data(data):
    url = 'http://0.0.0.0:80/api/sessions/new'
    print('From passive reader - posting data to server - (data: %s , url: %s)' % (data, url))
    r = requests.post(url, json=json.dumps(data), headers={'Content-type': 'application/json'})
    print('From passive reader - Tag data posted to server...')
    if r.status_code == requests.codes.ok or r.status_code == 200:
        print('From passive reader - Response from server is %s' % r.json())


current_userId = -1
current_keyId = -1
current_userTTL = -1

signal.signal(signal.SIGINT, end_read)

print("Reader active and awaiting input...")

while continue_reading:
    try:
        if current_userTTL <= time.time() and not current_userTTL == -1:
            print("2 minutes elapsed.\nPlease register your ID card again...")
            current_userId = -1
            current_keyId = -1
            current_userTTL = -1
            continue
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print("Tag detected")
            (status, backData) = MIFAREReader.MFRC522_Anticoll()
            if "" == backData or None is backData:
                continue
            tag_data = int(str(backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(backData[4]))
            if len(str(tag_data)) == 13:
                current_userTTL = time.time() + 120
                current_userId = tag_data
                print("User ID: %s" % current_userId)
            elif len(str(tag_data)) == 12:
                if current_userId == -1:
                    current_userTTL = time.time() + 120
                current_keyId = tag_data
                print("Key ID: %s" % current_keyId)
            if current_keyId > -1 and current_userId > -1:
                session = {
                    'user_id': str(current_userId),
                    'key_id': str(current_keyId),
                    'timestamp': str(datetime.datetime.now())
                }
                post_tag_data(session)
                current_keyId = -1
                time.sleep(2)
    except:
        continue
