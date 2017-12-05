import discord
from utils import config
from utils import reboot

async def run(client, message, object_list=None):
    await client.send_message(message.channel, 'Rebooting client! Please be patient.')
    reboot.Reboot()
    sys.exit()

def getName():
    return 'reboot'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
