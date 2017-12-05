import configparser
import discord
import os

def generate(server, roles, channel_list):
    config = configparser.ConfigParser()
    config['Server Information'] = {'Server Name': server}
    config['Server Information']['Active'] = 'True'
    for role in roles:
        config[role] = {}
        config[role]['basic'] = 'True'
        config[role]['music'] = 'True'
        config[role]['stat'] = 'True'
        config[role]['game'] = 'True'
        config[role]['admin'] = 'False'
    config['Active Channels'] = {}
    for channel in channel_list:
        config['Active Channels'][channel.name] = 'True'
    with open('config/' + str(server) + '.conf', 'w') as configfile:
        print('', file=configfile)
        config.write(configfile)

def refresh(server, channel_list, role_list):
    # Checks for new channels and roles.
    config = configparser.ConfigParser(strict=False)
    config.read('config/' + str(server) + '.conf')
    for role in role_list:
        role = role.name
        try:
            config[role]
        except KeyError:
            config.add_section(role)
            config.set(role, 'basic', 'True')
            config.set(role, 'music', 'True')
            config.set(role, 'stat', 'True')
            config.set(role, 'game', 'True')
            config.set(role, 'admin', 'False')
    for channel in channel_list:
        try:
            config['Active Channels'][channel.name] == ''
        except:
            config.set('Active Channels', channel.name, 'True')
    with open('config/' + str(server) + '.conf', 'w') as configfile:
        config.write(configfile)

def destroy(server):
    os.remove('config/' + str(server) + '.conf')
