import discord
import logging
import asyncio
import os
import importlib
from utils import configGen
from utils import config
from utils import util

client = discord.Client()
command_list = []
command_path = "/root/discordbots/kohaibot-for-discord/commands/"

@client.event
async def on_ready():
    print('='*20)
    print('curtime =', util.getHTime())
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    print("="*20)
    print('Finding command files')
    try:
        for command_file in os.listdir(command_path):
            if command_file != '__init__.py' and command_file.endswith(".py"):
                print('Command Found: {}'.format(command_file))
                #Imports the file, basically from path import command
                command = importlib.import_module('.commands.' + command_file, '/root/discordbots/kohaibot-for-discord')
                command_list.append(command)
    except FileNotFoundError:
        print('ERROR INCORRECT DIRECTORY')
    print('='*20)
    print('Generating Config files for servers')

    config_list = []
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

    try:
        author_role_list = []
        for role in message.author.roles:
            author_role_list.append(role.name)
    except AttributeError:
        #Only appears when bot sends messages to users.
        print('Bot sent help message to user')

    if message.content.startswith('?') or message.content.startswith('$'):
        print('{0} issued the command at {1}: {2}'.format(message.author, message.server, message))

    for command in command_list:
        if command.getName() == message.content.strip('?'):
            command.run(client, message)


client.run( config.devKey() )
