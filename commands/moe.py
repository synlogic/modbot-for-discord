import discord

async def run(client, message, object_list=None):
    player = None
    in_list = False

    # Checks if object is already in the object_list, then returns as a player object if true.
    index = 0
    for item in object_list:
        # Checks if the object is for the current server, and has player within the name
        if item[1] == str(message.server) + ' player':
            player = item[0]
            in_list = True
            break
        # Grabbing the index location for later use
        index += 1

    # Checks if the player exists and if it is already playing, then returns back to main if true
    if player != None and player.is_playing():
        await client.send_message(message.channel, "Already playing! Use '?stop' command to end the audio stream")
        return

    # This sets up the voice client, or grabs the voice client in the current server
    voice = client.voice_client_in(message.server)
    #Creates a ffmpeg player that grabs audio streaming from listen.moe's website.
    player = voice.create_ffmpeg_player("https://listen.moe/vorbis", headers={"User-Agent": 'Kohaibot for Discord'})
    await client.send_message(message.channel, 'You are now listening to listen.moe!')
    player.start()

    # If the player doesn't exist within the list, adds it for usage by other commands
    if not in_list:
        return (player, str(message.server) + ' player')
    else:
    # Here's where the index is used to replace the object within the object_list
    # and return a new list for the main function to use
        object_list[index] = (player, str(message.server) + ' player')
        return object_list


def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'moe'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'music'
