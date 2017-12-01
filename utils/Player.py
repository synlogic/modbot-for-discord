import discord
import dill
import os

def getPlayer(server):
    server = str(server)
    if not os.path.isfile('texts/' + server + '_player.txt'):
        return None
    with open('texts/ '+ server + '_player.txt', 'rb') as fileHandle:
        return dill.load(fileHandle)
    fileHandle.close()

def addPlayer(server, player):
    server = str(server)
    with open('texts/' + server + '_player.txt', 'wb') as fileHandle:
        dill.dump(player, fileHandle)
    fileHandle.close()

def removePlayer(server, player):
    server = str(server)
    if os.path.isfile('texts/' + server + '_player.txt'):
        os.remove('texts/' + server + '_player.txt')
