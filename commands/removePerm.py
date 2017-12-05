import discord
import perms

async def run(client, message, object_list=None):
    try:
        role = message.content.split(' ')[1]
        permission = message.content.split(' ')[2]
        perms.removePerm(str(message.server), role, permission)
        await client.send_message(message.channel, 'Permission removed from role successfuly!')
    except:
        await client.send_message(message.channel, 'Failure removing permission from role. Make sure role and permissions exist!')

def getName():
    return 'removePerm'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
