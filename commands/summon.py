import discord

async def run(client, message, object_list=None):
    # Checks if opus is loaded, this is needed for the bots voice client to work.
    if not discord.opus.is_loaded():
        try:
            # opus library on Linux
            discord.opus.load_opus('libopus0')
        except:
            try:
                # opus library on Windows
                discord.opus.load_opus('opus')
            except:
                await client.send_message(message.channel, 'Bot failed to find opus library, notify administrator to install opus library.')
                return

    if message.content.strip('?summon ') == '':
        # If the ?summon command has no message then the client joins the voice channel with the same name as the channel the
        # message author is in.  Otherwise join the same channel as stated after the summon command.
        try:
            for channel in message.server.channels:
                # Ensures the channel type is of voice
                if channel.name == message.channel.name and str(channel.type) is 'voice':
                    voice = await client.join_voice_channel(channel)
        except discord.errors.ClientException:
            await client.send_message(message.channel, 'Already connected to a voice channel in this server! Use "?disconnect" command before summoning again.')
    else:
        try:
            for channel in message.server.channels:
                # Ensures the channel type is of voice and has the same name as stated after the command
                if channel.name == message.content.strip('?summon ') and str(channel.type) is 'voice':
                    voice = await client.join_voice_channel(channel)
        except discord.errors.ClientException:
            await client.send_message(message.channel, 'Already connected to a voice channel in this server.')

def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'summon'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'music'
