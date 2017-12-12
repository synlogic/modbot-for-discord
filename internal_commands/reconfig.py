import discord
import perms
from utils import configGen

async def run(client, message, object_list=None):
    try:

        server = message.server
        print('='*20)
        print('Regenerating Config file for {}'.format(server))
        role_list = []
        for role in server.roles:
            role_list.append(role.name)
        configGen.destroy(server.name)
        print('INFO: Succesfully destroyed config for server')
        channel_list = []
        for channel in message.server.channels:
            channel_list.append(channel)
        configGen.generate(server.name, role_list, channel_list)
        print('INFO: Generated conf for server: ' + server.name)
        print('='*20)
        await client.send_message(message.channel, 'Succesfully regenerated config file for server')
    except Exception as e:
        await client.send_message(message.channel, 'Failure in regenerating config file')
        print('Failure in regenerating config file:\n\t ', e)

def getName():
    return 'reconfig'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
