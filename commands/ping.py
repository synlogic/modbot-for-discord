import discord

async def run(client, message):
    await client.send_message(message.channel, 'Pong!')

def getName():
    return 'ping'
