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
from config import kohaiKey
from util import *

if not discord.opus.is_loaded():
    discord.opus.load_opus()

debug = False
player = fakePlayer
client = discord.Client()
channelid = ''
curtime = time.strftime('%H:%M:%S')
playing = False
if debug == False:
    subpro = True
    p = subprocess.Popen(['python3.5', 'ReminderBot.py'])
    print('Subprocess ID: ', p.pid)


with open('logs/textlog.txt', 'w') as fileHandle:
    fileHandle.write('')
fileHandle.close()


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
    print('Grabbing config files for all servers')
    for server in client.servers:
        print(server)

class Main:

    @client.event
    async def on_message(message):
        print(message.server, message.author, ': ', message.content)
        author = message.author
        with open('logs/textlog.txt', 'a+') as fileHandle:
            print(message.server, author, 'said:', message.content, file=fileHandle)
        fileHandle.close()
#Begin Music Bot Commands

        if message.content.startswith('?summon'):
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
            global player

            url = message.content.strip('?play ')
            voice = client.voice_client_in(message.server)
            if 'https://' in url or 'http://' in url:
                if player.is_playing:
                    player.stop()
                    player = await voice.create_ytdl_player(url)
                    player.start()
                    await client.send_message(message.channel, '"{}" is now playing!'.format(player.title))
                else:
                    player.stop()
                    player = await voice.create_ytdl_player(url)
                    await client.send_message(message.channel, '"{}" is now playing!'.format(player.title))
                    player.start()
            else:
                if player.is_playing:
                    player.stop()
                    subprocess.call(['rm', 'youvid.mp4'])
                    subprocess.call(['youtube-dl','ytsearch:' + url,'--audio-format', 'mp3', '--output', 'youvid.%(ext)s'], shell=False)
                    player = voice.create_ffmpeg_player('youvid.mp4')
                    player.start()
                    await client.send_message(message.channel, '"{}" is now playing!'.format(url))
                else:
                    player.stop()
                    subprocess.call(['youtube-dl','ytsearch:' + url,'--audio-format', 'mp3', '--output', 'youvid.%(ext)s'], shell=False)
                    player = voice.create_ffmpeg_player('youvid.mp4')
                    await client.send_message(message.channel, '"{}" is now playing!'.format(url))
                    player.start()


        elif message.content.startswith('?stop'):
            server = message.server
            voice = client.voice_client_in(server)
            player.stop()

        elif message.content.startswith('?disconnect'):
            voice = client.voice_client_in(message.server)
            await voice.disconnect()

        elif message.content.startswith('?restart'):
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
            await client.send_message(message.channel, 'Pong!')

        elif message.content.startswith('?usage'):
            helptext = open('texts/help.txt', 'r')
            await client.send_message(message.channel, helptext.read())
            helptext.close()

        elif message.content.startswith('?coinflip'):
            flip = random.randint(1,2)
            if flip == 1:
                await client.send_message(message.channel, 'You flipped heads!')
            else:
                await client.send_message(message.channel, 'You flipped tails!')

        elif message.content.startswith('?gg ez'):
            fileHandle = open('texts/ggez.txt')
            ranLine = random.choice(fileHandle.readlines())
            await client.send_message(message.channel, ranLine)
            fileHandle.close()

        elif message.content.startswith('?natsuccs'):
            await client.send_message(message.channel, 'He sure does.')

#remindbot commands


        elif message.content.startswith('?startremindbot'):
            if not subpro:
                p = subprocess.Popen(['python3.5', 'ReminderBot.py'])
                print('Subprocess ID: ', p.pid)
                subpro = True
                await client.send_message(message.channel, 'ReminderBot is now running!')
            elif subpro:
                await client.send_message(message.channel, 'ReminderBot is already running!')

        elif message.content.startswith('?stopremindbot'):
            try:
                p.terminate()
                returncode = p.wait()
                print('Returncode of subprocess: ', returncode)
                await client.send_message(message.channel, 'ReminderBot terminated.')
                subpro = False
            except:
                await client.send_message(message.channel, 'An error has occured')

#osu Commands

        elif message.content.startswith("?osu"):
            mode = 0
            msg = message.content[5:]
            print(msg)
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
            msg = message.content[4:]
            print(msg)
            option, username, region = msg.split()
            print(option, username, region)
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


        '''
        Needs cleanup work.  I do not want to be using too many global variables here.  Make things ugly. bleh.
        '''
        elif message.content.startswith('?rr'):
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


client.run( kohaiKey() )
