import discord
from ctypes.util import find_library

player = None

async def run(client, message, object_list=None):
    if not discord.opus.is_loaded():
        try:
            #Linux
            discord.opus.load_opus('libopus0')
        except:
            try:
                #Windows
                discord.opus.load_opus('opus')
            except:
                await client.send_message(message.channel, 'Bot failed to find opus library, notify administrator to install opus library.')
                return

    if message.content.strip('?summon ') == '':
        try:
            for channel in message.server.channels:
                if channel.name == message.channel.name and str(channel.type) is 'voice':
                    voice = await client.join_voice_channel(channel)
        except discord.errors.ClientException:
            await client.send_message(message.channel, 'Already connected to a voice channel in this server!')
    else:
        try:
            for channel in message.server.channels:
                if channel.name == message.content.strip('?summon ') and str(channel.type) is 'voice':
                    voice = await client.join_voice_channel(channel)
        except discord.errors.ClientException:
            await client.send_message(message.channel, 'Already connected to a voice channel in this server.')

def getName():
    return 'summon'
