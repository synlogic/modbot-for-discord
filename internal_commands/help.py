import discord

async def run(client, message, object_list=None):
    await client.send_message(message.author, "Please refer to the kohaibot wiki for usage of commands! https://github.com/synlogic/kohaibot-for-discord/wiki")

def getName():
    # What the user will input in discord to call the command.
    # Needs to be without the prefix!
    return 'help'

def permType():
    # Returns the type of permission this command uses.  Can be ignored if permissions are disabled.
    return 'basic'
