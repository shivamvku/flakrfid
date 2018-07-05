import os
import MFRC522
import signal
import subprocess

p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
out, err = p.communicate()


def find_process(out):
    for line in out.splitlines():
        if 'PID' in line:
            words = format_line(line)
            index = int(words.index('PID'))
            print "Index of PID is " + str(index)
            if 'sudo python read.py' in line or 'sudo python reader.py' in line:
                print "Task to be stopped: "
                words = format_line(line)
                pid = int(words[index])
                print "PID of reader-task is " + str(pid)
                os.kill(pid, signal.SIGKILL)


def format_line(line):
    words = []
    for word in line.split(" "):
        if word is not " " and word is not "":
            words.append(word)
    return words

find_process(out)

MIFAREReader = MFRC522.MFRC522()

MIFAREReader.GPIO_CLEEN()
