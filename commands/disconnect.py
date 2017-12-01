import discord


async def run(client, message, object_list=None):

    for item in object_list:
        if item[1] == str(message.server) + ' player':
            player = item[0]
            player.stop()
            break

    voice = client.voice_client_in(message.server)
    await voice.disconnect()

def getName():
    return 'disconnect'
