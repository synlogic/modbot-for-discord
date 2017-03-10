import configparser

config = configparser.ConfigParser()
def hasPermission(server, role_list, command):
    config.read('config/' + server + '_conf.ini')
    for role in role_list:
        if config[role][command] == 'True':
            print('has Perms')
            return True
        else:
            hasPerms = False
    return hasPerms

def addPerm(server, role, permission):
    config.read('config/' + server + '_conf.ini')
    config.set(role, permission, 'True')
