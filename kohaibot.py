import discord
import logging
import asyncio
import os
import sys
import importlib
from utils import configGen
# config.py is the file that contains tokens and keys and any other private imformation not to be shared with git
from utils import config
from utils import setup
from utils import util

# Clears the screen for readability.  Feel free to disable this
os.system('clear')
# if on windows use
# os.system('cls')
command_path = './commands/'
sys.path.insert(0, command_path)
setup.runSetup()
client = discord.Client()
command_list = []
# used to preserve certain objects such as audio players.
object_list = []
prefix = '?'
# This was for my own testing of commands, this can be removed.
open('texts/players.txt', 'w').close()

@client.event
async def on_ready():

    print('='*20)
    print('Kohaibot Discord Bot, built by SynLogic')
    print('='*20)
    print('curtime =', util.getHTime())
    print('Logging in as')
    print('Bot Username: ', client.user.name)
    print('Bot ID: ', client.user.id)
    print("="*20)

    #Finds and imports command modules
    print('Finding command files')
    try:
        for command_file in os.listdir(command_path):
            if command_file != '__init__.py' and command_file.endswith(".py"):
                #Imports the file, basically from path import command
                command = importlib.import_module(os.path.splitext(command_file)[0])
                command_list.append(command)
                print('Command found [ {} ] and added succesfully'.format(command_file))
    except FileNotFoundError:
        print('No command files found')
    print('='*20)

    #Generates the configuration files for all servers connected
    print('Generating/Grabbing Config files for servers')
    config_list = []
    if not os.path.isfile('texts/config_list.conf'):
        open('texts/config_list.conf', 'a')
    with open('texts/config_list.conf') as fileHandle:
        for line in fileHandle:
            config_list.append(line.strip('\n'))
    fileHandle.close()
    for server in client.servers:
        role_list = []
        if not server.name in config_list:
            for role in server.roles:
                role_list.append(role.name)
            configGen.generate(server.name, role_list)
            with open('texts/config_list.conf', 'a+') as fileHandle:
                print(server.name.strip('\n'), file=fileHandle)
                config_list.append(server.name)
            fileHandle.close()
            print('Generated conf for server: ' + server.name)
        else:
            print('Found config for: ' + server.name)
    print('='*20)

@client.event
async def on_message(message):
    global object_list

    try:
        author_role_list = []
        for role in message.author.roles:
            author_role_list.append(role.name)
    except AttributeError:
        #Only appears when bot sends messages to users.
        print('Bot sent message to user')

    if message.author == client.user:
        print('{0} responded with: {1}'.format(client.user.name, message.content))

    for command in command_list:
        if command.getName() == message.content.strip(prefix).split(' ')[0]:
            print('{0} issued the command at {1}: {2}'.format(message.author, message.server, message.content))
            currentCommand = await command.run(client, message, object_list)
            if currentCommand != None and currentCommand not in object_list:
                if type(currentCommand) == list:
                    object_list = currentCommand
                    print('Object_list was replaced with {}'.format(object_list))
                    break
                object_list.append(currentCommand)
                print("INFO: Added an object -{}- to object_list".format(currentCommand))
            break


client.run( config.getKey() )
