import time
import json
import requests


def getHTime():
    return time.strftime('%I:%M %p')

def getBTime():
    return time.strftime('%a:%H:%M:%S')

def getServers():
    server_list = []
    with open('texts/server_list.txt', 'r') as fileHandle:
        for line in fileHandle:
            server_list.append(line)
    fileHandle.close()
    return server_list

class fakePlayer():

    def is_playing():
        return False

    def stop():
        pass
