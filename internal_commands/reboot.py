import discord
from utils import config
from utils import reboot

async def run(client, message, object_list=None):
    if not str(message.author) == 'SynLogic#5410':
        return
    await client.send_message(message.channel, 'Rebooting client! Please be patient.')
    voice = client.voice_client_in(message.server)
    try:
        await voice.disconnect()
    except:
        pass
    reboot.Reboot()
    sys.exit()

def getName():
    return 'reboot'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'admin'
