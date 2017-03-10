'''
TODO:

 Permissions

 er.. more games?

 lots of cleanup work.   yay.
'''
import discord
import logging
import asyncio
import random
import aiohttp
import time
import sys
import subprocess
import youtube_dl
import random
import configparser
import json
import requests
from osu import getOsu
from overwatch import getOverwatch
from config import kohaiKey, devKey
import perms
import configparser
from util import *
import configGen

if not discord.opus.is_loaded():
    discord.opus.load_opus()

debug = True
player = fakePlayer
client = discord.Client()
config_list = []
channelid = ''
config = configparser.ConfigParser()

#RussianRoulette variables
players = []
index = 0
size = 0
started = False

@client.event
async def on_ready():
    if debug:
        print('='*20)
        print('Debug is active')
    print('='*20)
    print('curtime =', getHTime())
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    print('='*20)
    print('Generating Config files for servers')
    with open('texts/config_list.conf') as fileHandle:
        for line in fileHandle:
            config_list.append(line.strip('\n'))
    fileHandle.close()
    for server in client.servers:
        role_list = []
        if not server.name in config_list:
            for role in server.roles:
                role_list.append(role.name)
            configGen.generate(server.name, role_list)
            with open('texts/config_list.conf', 'a+') as fileHandle:
                print(server.name.strip('\n'), file=fileHandle)
            fileHandle.close()
            print('Generated conf for server: ' + server.name)
        else:
            print('Found config for: ' + server.name)
    print('='*20)

class Main:

    @client.event
    async def on_message(message):
    #Begin Music Bot Commands
        author_role_list = []
        for role in message.author.roles:
            if not role.name in author_role_list:
                author_role_list.append(role.name)

        if message.content.startswith('?summon'):
            if perms.hasPermission(message.server.name, author_role_list, 'music commands'):
                if message.content.strip('?summon ') == '':
                    try:
                        for server in client.servers:
                            if server == message.server:
                                for channel in server.channels:
                                    if channel.name == message.channel.name and str(channel.type) is 'voice':
                                        voice = await client.join_voice_channel(channel)
                    except discord.errors.ClientException:
                        await client.send_message(message.channel, 'Already connected to a voice channel in this server!')
                else:
                    gottochannel = message.content.strip('?summon ')
                    try:
                        for server in client.servers:
                            if server == message.server:
                                for channel in server.channels:
                                    if channel.name == gottochannel and str(channel.type) is 'voice':
                                        voice = await client.join_voice_channel(channel)
                    except discord.errors.ClientException:
                        await client.send_message(message.channel, 'Already connected to a voice channel in this server.')


        elif message.content.startswith('?play'):
            if  perms.hasPermission(message.server.name, author_role_list, 'music commands'):
                global player

                song = message.content.strip('?play ')
                voice = client.voice_client_in(message.server)
                if player.is_playing:
                    player.stop()
                opts = {
                    'default_search': 'auto',
                    'quiet': True,
                }

                player = await voice.create_ytdl_player(song, ytdl_options=opts)
                player.start()
                await client.send_message(message.channel, '"{}" is now playing!'.format(player.title))


        elif message.content.startswith('?stop'):
            if  perms.hasPermission(message.server.name, author_role_list, 'music commands'):
                server = message.server
                voice = client.voice_client_in(server)
                player.stop()

        elif message.content.startswith('?disconnect'):
            if  perms.hasPermission(message.server.name, author_role_list, 'music commands'):
                voice = client.voice_client_in(message.server)
                await voice.disconnect()

        elif message.content.startswith('?restart'):
            if  perms.hasPermission(message.server.name, author_role_list, 'music commands'):
                server = message.server
                voice = client.voice_client_in(server)
                await voice.disconnect()
                for server in client.servers:
                    if server == message.server:
                        for channel in server.channels:
                            if channel.name == message.channel.name and str(channel.type) is 'voice':
                                voice = await client.join_voice_channel(channel)

#Basic Commands

        elif message.content.startswith('?ping'):
            if perms.hasPermission(message.server.name, author_role_list, 'basic commands'):
                await client.send_message(message.channel, 'Pong!')

        elif message.content.startswith('?help'):
            if perms.hasPermission(message.server.name, author_role_list, 'basic commands'):
                await client.send_message(message.author, 'Please refer to the KohaiBot wiki: https://github.com/synlogic/kohaibot-for-discord/wiki')

        elif message.content.startswith('?coinflip'):
            if perms.hasPermission(message.server.name, author_role_list, 'basic commands'):
                flip = random.randint(1,2)
                if flip == 1:
                    await client.send_message(message.channel, 'You flipped heads!')
                else:
                    await client.send_message(message.channel, 'You flipped tails!')

        elif message.content.startswith('?gg ez'):
            if perms.hasPermission(message.server.name, author_role_list, 'basic commands'):
                fileHandle = open('texts/ggez.txt')
                ranLine = random.choice(fileHandle.readlines())
                await client.send_message(message.channel, ranLine)
                fileHandle.close()

#osu Commands

        elif message.content.startswith("?osu"):
            if perms.hasPermission(message.server.name, author_role_list, 'stat commands'):
                mode = 0
                msg = message.content[5:]
                if 'mania' in msg:
                    user = msg[6:]
                    username, user_id, pp_raw, pp_rank, accuracy, country_rank, country = getOsu(user, 3)
                    mode = 3
                elif 'fruit' in msg:
                    user = msg[6:]
                    username, user_id, pp_raw, pp_rank, accuracy, country_rank, country = getOsu(user, 2)
                    mode = 2
                elif 'taiko' in msg:
                    user = msg[6:]
                    username, user_id, pp_raw, pp_rank, accuracy, country_rank, country = getOsu(user, 1)
                    mode = 1
                else:
                    username, user_id, pp_raw, pp_rank, accuracy, country_rank, country = getOsu(msg, 0)

                osu_stats = discord.Embed(
                    color = 13074380,
                    title = '**osu! stats**',
                    description = 'Click on the username to go to their page!'
                ).set_author(
                    name = username,
                    url = 'http://osu.ppy.sh/u/' + user_id,
                    icon_url = 'http://w.ppy.sh/c/c9/Logo.png',
                ).set_thumbnail(
                    url = 'https://a.ppy.sh/' + user_id
                ).add_field(
                    name = 'Raw PP',
                    value = pp_raw
                ).add_field(
                    name = 'Accuracy',
                    value = '{:.2f}'.format(float(accuracy))
                ).add_field(
                    name = 'WorldWide Ranking',
                    value = '#{:,}'.format(int(pp_rank))
                ).add_field(
                    name =  country + ' Ranking',
                    value = '#{:,}'.format(int(country_rank))
                )
                await client.send_message(message.channel, embed=osu_stats)


        elif message.content.startswith('?ow '):
            if perms.hasPermission(message.server.name, author_role_list, 'stat commands'):
                region = ''
                msg = message.content[4:]
                opts = msg.split(' ')
                if len(opts) == 3:
                    option = opts[0]; username = opts[1]; region = opt[2]
                elif len(opts) == 2:
                    option = opts[0]; username = opts[1]
                elif len(opts) == 1:
                    username = opts[0]
                    option = 'qp'
                username = username.replace('#','-')
                print
                if option == 'qp':
                    gamemode = 'Quick Play '
                    avatar, rank, win_rate, wins, losses = getOverwatch(username, region, 'quickplay')
                if option == 'comp':
                    gamemode = 'Competitive '
                    avatar, rank, win_rate, wins, losses = getOverwatch(username, region, 'competitive')

                ow_stats = discord.Embed(
                    color = 15566637,
                    title = '**Overwatch stats**',
                    description = gamemode + region.upper()
                ).set_author(
                    name = username,
                    icon_url = 'http://i.imgur.com/YZ4w2ey.png',
                ).set_thumbnail(
                    url = avatar
                )

                if option == 'comp':
                    ow_stats.add_field(
                        name = 'Competitive Rank',
                        value = rank
                    )

                ow_stats.add_field(
                    name = 'Win Rate',
                    value = str(win_rate) + '%'
                ).add_field(
                    name = 'Wins',
                    value = wins
                ).add_field(
                    name = 'Losses',
                    value = losses
                )

                await client.send_message(message.channel, embed=ow_stats)


        elif message.content.startswith('?rr'):
            if perms.hasPermission(message.server.name, author_role_list, 'game commands'):
                global players
                global size
                global started
                global index
                msg = message.content.strip('?rr ')
                if msg == 'join':
                    if not(message.author in players):
                        players.insert(index, message.author)
                        print(players)
                        index += 1
                        await bot.say(message.channel, '{} has joined the game of Russian Roulette!'.format(message.author))
                    else:
                        await client.send_message(message.channel, "You're already in the game, what are you trying to achieve?")
                elif 'size' in msg:
                    size = int(msg.strip('size '))
                    print('size at ', size)
                    await client.send_message(message.channel, 'The gun now has a magazine of {}.'.format(size))
                elif 'begin' in msg:
                    if len(players) < 1:
                        await client.send_message(message.channel, "Not enough players!")
                        print(players)
                    else:
                        if size == 0:
                            await client.send_message(message.channel, 'No size specified, magazine set to 6')
                            size = 6
                        await client.send_message(message.channel, "A new Russian Roulette game has started!  When it's your turn say \"shoot\"")
                        started = True
                        finished = False
                        current_container = 0
                        bullet = random.randint(0, size)
                        print('bullet at: ', bullet)
                        print('size: ', size)
                        while current_container < size and not finished:
                            for person in players:
                                if not finished:
                                    await client.send_message(message.channel, "It's {}'s turn!".format(person))
                                    await client.wait_for_message(author=person, content="shoot")
                                    if current_container == bullet:
                                        await client.send_message(message.channel, '{} has been shot! Rest in peace... **Game Over**'.format(person))
                                        started = False
                                        finished = True
                                        players = []
                                        size = 0
                                        current_container += 1
                                    else:
                                        await client.send_message(message.channel, '{} has survived another round'.format(person))
                                        current_container += 1

        elif message.content.startswith('$p-ar') and perms.hasPermission(message.server.name, author_role_list, 'admin commands'):
            opts = message.split()
            role = opt[0]; permission = opt[0]
            try:
                perms.addPerm(message.server.name, role, permission)
                await client.send_message(message.channel, 'Added {0} to {1}\'s permissions'.format(role, permission))
            except KeyError:
                await client.send_message(message.channel, 'Invalid arguments.')

        elif message.content.startswith('$p-ls') and perms.hasPermission(message.server.name, author_role_list, 'admin commands'):
            await client.send_message(message.author, 'Current list of permissions can be found at the wiki:  https://github.com/synlogic/kohaibot-for-discord/wiki/Permissions')


client.run( devKey() )
