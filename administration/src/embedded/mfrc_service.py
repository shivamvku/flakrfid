def load_src(name, fdir, fpath):
    import os, imp
    res_full_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), fdir, fpath)
    return imp.load_source(name, res_full_path)


load_src("MFRC522", "rfid_python_lib", "MFRC522.py")
import MFRC522
import time


class ServiceMFRC:
    def __init__(self):
        self.continue_reading = True
        self.MIFAREReader = MFRC522.MFRC522()
        self.message = ""
        self.counter = 30

    def end_read(self):
        self.continue_reading = False
        self.counter = -1
        print "Ctrl+C captured, ending read."
        self.MIFAREReader.GPIO_CLEEN()

    def do_read(self):
        self.continue_reading = True
        while self.continue_reading and self.counter > 0:
            # print('Reader TTL: %s' % self.counter)
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            if status == self.MIFAREReader.MI_OK:
                self.message += "Card detected. "
            (status, backData) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                self.message += (
                    "Card read UID: " + str(backData[0]) + "," + str(backData[1]) + "," + str(backData[2]) + "," + str(
                        backData[3]) + "," + str(backData[4])
                )
                self.end_read()
                return {
                    'message': self.message,
                    'data': reduce(lambda x, y: str(x) + str(y), backData)
                }
            self.counter -= 1
            time.sleep(0.5)
        print('No tag data found...')
        return {
            'message': 'No tag data detected...',
            'data': '00000000'
        }
