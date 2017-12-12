import discord
import logging
import asyncio
import os
import sys
import importlib
import time
from perms import PermissionManager
from utils import configGen
# config.py is the file that contains tokens and keys and any other private imformation not to be shared with git
from utils import config
from utils import setup


# Clears the screen for readability.  Feel free to disable this
os.system('clear')
# if on windows use
# os.system('cls')
command_path = './commands/'
internal_path = './internal_commands/'
sys.path.insert(0, command_path)
sys.path.insert(0, internal_path)
setup.runSetup()
client = discord.Client()
command_list = []
# used to preserve certain objects such as audio players.
object_list = []
prefix = '?'

@client.event
async def on_ready():

    print('='*20)
    print('Kohaibot Discord Bot, built by SynLogic')
    print('='*20)
    print('Current Time: ', time.strftime('%I:%M %p'))
    print('Logging in as: ', client.user.name)
    print('Bot ID: ', client.user.id)
    print("="*20)

    # Basic logging setup
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='output_log.txt', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    # Finds and imports command modules
    print('Finding command files')
    try:
        for command_file in os.listdir(command_path):
            if command_file != '__init__.py' and command_file.endswith(".py"):
                #Imports the file, basically from path import command
                command = importlib.import_module(os.path.splitext(command_file)[0])
                command_list.append(command)
                print('Command found [ {} ] and added succesfully'.format(command_file))
        for command_file in os.listdir(internal_path):
            if command_file != '__init__.py' and command_file.endswith(".py"):
                command = importlib.import_module(os.path.splitext(command_file)[0])
                command_list.append(command)
                print('Internal Command found [ {} ] and added succesfully'.format(command_file))
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
            configGen.generate(server.name, role_list, server.channels)
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
        # Only appears when bot sends messages to users.
        print('Bot sent message to user')

    if message.author == client.user:
        if message.content == '':
            return
        print('{0} responded with: {1}'.format(client.user.name, message.content))

    for command in command_list:
        if command.getName() == message.content.strip(prefix).split(' ')[0] and message.content.startswith(prefix):
            configGen.refresh(message.server, message.server.channels, message.server.roles)
            perms = PermissionManager(message.server)
            if not message.author.server_permissions.manage_server:
                if perms.activeServer() and not perms.hasPermission(message.author.roles, command.permType() ) and not perms.channelActive(message.channel):
                    print('{} has invalid permissions to issue the command "{}"'.format(message.author, message.content))
                    break
            print('{0}: [{2}]@{1}#{3}'.format(message.author, message.server, message.content, message.channel.name))
            currentCommand = await command.run(client, message, object_list)
            if currentCommand != None and currentCommand not in object_list:
                if type(currentCommand) == list:
                    object_list = currentCommand
                    print('INFO: Object_list was replaced with -{}-'.format(object_list))
                    break
                object_list.append(currentCommand)
                print("INFO: Added an object -{}- to object_list".format(currentCommand))
            break

# Either use config.py to add your token, or place it directly here as a string.
# Remeber to never share your discord api token.
client.run( config.getDevKey() )
