import discord

async def run(client, message, object_list=None):
    channel_name = message.content.split(' ')[1]
    msg = message.content.split(' ')[2]

    for channel in message.server.channels:
        if channel.name == channel_name:
            await client.send_message(channel, msg)
            break


def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'bt'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
