import discord

async def run(client, message, object_list=None):

    # Checks if player is in the object_list, and if it is stops the player then returns
    # an edited object list with the new player (discord player seems to change objects when stopped or started so this is necessary)
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
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'stop'
