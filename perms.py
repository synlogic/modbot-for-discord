import configparser

config = configparser.ConfigParser()
def hasPermission(server, role_list, command):
    config.read('config/' + str(server) + '.conf')
    for role in role_list:
        if isinstance(role, str):
            if config[role][command] == 'True':
                return True
        else:
            if config[role.name][command] == 'True':
                return True
    return False

def addPerm(server, role, permission):
    config.read('config/' + str(server) + '.conf')
    if not config[role][permission]:
        raise KeyError
    config.set(role, permission, 'True')
    with open('config/' + server + '.conf', 'w') as configfile:
        config.write(configfile)

def removePerm(server, role, permission):
    config.read('config/' + str(server) + '.conf')
    if not config[role][permission]:
        raise KeyError
    config.set(role, permission, 'False')
    with open('config/' + server + '.conf', 'w') as configfile:
        config.write(configfile)

def toggleChannel(server, channel):
    config.read('config/' + str(server) + '.conf')
    if not isinstance(channel, str):
        channel = channel.name
    boolean = config['Active Channels'][channel]
    if boolean == 'True':
        boolean = 'False'
        return_message = 'disabled'
    elif boolean == 'False':
        boolean = 'True';
        return_message = 'enabled'
    config.set('Active Channels', channel, boolean)
    with open('config/' + str(server) + '.conf', 'w') as configfile:
        config.write(configfile)
    return return_message

def channelActive(server, channel):
    config.read('config/' + str(server) + '.conf')
    if not isinstance(channel, str):
        channel = channel.name
    if config['Active Channels'][channel] == 'True':
        return True
    return False

def activeServer(server):
    config.read('config/' + str(server) + '.conf')
    if config['Server Information']['Active'] == 'True':
        return True
    return False

def togglePerms(server):
    config.read('config/' + str(server) + '.conf')
    if config['Server Information']['Active'] == 'True':
        config.set('Server Information', 'Active', 'False')
        return 'disabled'
    else:
        config.set('Server Information', 'Active', 'True')
        return 'enabled'
