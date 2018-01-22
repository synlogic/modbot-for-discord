import discord
from perms import PermissionManager

async def run(client, message, object_list=None):
    perms = PermissionManager(message.server)

    if not perms.activeServer():
        await client.send_message(message.channel, 'Permissions are not enabled on this server.  Use ?togglePerms to enable them.')
        return
    with open('config/' + str(message.server) + '.conf') as fileHandle:
        await client.send_message(message.channel, '```{}```'.format(fileHandle.read()))
    fileHandle.close()


def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'showPerms'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
