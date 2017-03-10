import time
import json
import requests


def getHTime():
    return time.strftime('%I:%M %p')

def getBTime():
    return time.strftime('%a:%H:%M:%S')


class fakePlayer():

    def is_playing():
        return False

    def stop():
        pass
