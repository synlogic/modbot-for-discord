import discord

async def run(client, message, object_list=None):
    player = None
    in_list = False

    # Checks if object is already in the object_list, then returns as a player object if true.
    index = 0
    for item in object_list:
        if item[1] == str(message.server) + ' player':
            player = item[0]
            in_list = True
            break
        index += 1
    if player != None and player.is_playing():
        await client.send_message(message.channel, "Already playing! Use '?stop' command to end the audio stream")
        return

    voice = client.voice_client_in(message.server)
    player = voice.create_ffmpeg_player("https://listen.moe/vorbis", headers={"User-Agent": 'Kohaibot for Discord'})
    await client.send_message(message.channel, 'You are now listening to listen.moe!')
    player.start()
    if not in_list:
        return (player, str(message.server) + ' player')
    else:
        object_list[index] = (player, str(message.server) + ' player')
        return object_list


def getName():
    return 'moe'
