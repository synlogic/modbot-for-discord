import configparser

config = configparser.ConfigParser()
def hasPermission(server, role_list, command):
    config.read('config/' + server + '_conf.ini')
    for role in role_list:
        if config[role][command] == 'True':
            return True
        else:
            hasPerms = False
    return hasPerms

def addPerm(server, role, permission):
    config.read('config/' + server + '_conf.ini')
    if not config[role][permission]:
        raise KeyError
    config.set(role, permission, 'True')
    with open('config/' + server + '_conf.ini', 'w') as configfile:
        config.write(configfile)

def removePerm(server, role, permission):
    config.read('config/' + server + '_conf.ini')
    if not config[role][permission]:
        raise KeyError
    config.set(role, permission, 'False')
    with open('config/' + server + '_conf.ini', 'w') as configfile:
        config.write(configfile)
