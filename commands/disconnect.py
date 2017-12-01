import discord


async def run(client, message, object_list=None):
    # Checks for the player object and if found stops the player and removes it from the object_list
    for item in object_list:
        if item[1] == str(message.server) + ' player':
            player = item[0]
            player.stop()
            object_list.remove(item)
            break

    # Finds voice client in the current server, then disconnects the voice client.
    voice = client.voice_client_in(message.server)
    await voice.disconnect()
    #returns a new object_list with the removed object.
    return object_list

def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'disconnect'
