import discord

async def run(client, message, object_list=None):
    await client.send_message(message.channel, 'Pong!')

def getName():
    return 'ping'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'basic'
