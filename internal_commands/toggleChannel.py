import discord
from perms import PermissionManager

async def run(client, message, object_list=None):
    perms = PermissionManager(message.server)
    channel_name = message.channel
    try:
        enable_or_disable = perms.toggleChannel(channel_name)
        await client.send_message(message.channel, 'Succesfully {} channel.'.format(enable_or_disable))
    except Exception as e:
        await client.send_message(message.channel, 'Something went wrong!')
        print('Error on toggeling active channel at ', str(message.server), ': ', e)


def getName():
    return 'toggleChannel'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
