import discord
import perms

async def run(client, message, object_list=None):
    server = message.server
    try:
        enable_or_disable = perms.togglePerms(message.server)
        await client.send_message(message.channel, 'Succesfully {} server permissions!'.format(enable_or_disable))
    except Exception as e:
        await client.send_message(message.channel, 'Something went wrong!')
        print('Error on toggeling active channel at ', str(message.server), ': ', e)


def getName():
    return 'togglePerms'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
