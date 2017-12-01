import discord

async def run(client, message, object_list=None):

    index = 0
    for item in object_list:
        if item[1] == str(message.server) + ' player':
            player = item[0]
            player.stop()
            object_list[index] = (player, str(message.server) + ' player')
            return object_list
        index += 1
    await client.send_message(message.channel, 'Nothing is playing!')

def getName():
    return 'stop'
