import configparser

class PermissionManager:

    def __init__(self, server):
        self.server = server
        self.config = configparser.ConfigParser()

    def hasPermission(self, role_list, command):
        self.config.read('config/' + str(self.server) + '.conf')
        for role in role_list:
            if isinstance(role, str):
                if config[role][command] == 'True':
                    return True
            else:
                if config[role.name][command] == 'True':
                    return True
        return False

    def addPerm(self, role, permission):
        self.config.read('config/' + str(self.server) + '.conf')
        if not self.config[role][permission]:
            raise KeyError
        self.config.set(role, permission, 'True')
        with open('config/' + self.server + '.conf', 'w') as configfile:
            self.config.write(configfile)

    def removePerm(self, role, permission):
        self.config.read('config/' + str(self.server) + '.conf')
        if not self.config[role][permission]:
            raise KeyError
        self.config.set(role, permission, 'False')
        with open('config/' + self.server + '.conf', 'w') as configfile:
            self.config.write(configfile)

    def toggleChannel(self, channel):
        self.config.read('config/' + str(self.server) + '.conf')
        if not isinstance(channel, str):
            channel = channel.name
        boolean = self.config['Active Channels'][channel]
        if boolean == 'True':
            boolean = 'False'
            return_message = 'disabled'
        elif boolean == 'False':
            boolean = 'True';
            return_message = 'enabled'
        self.config.set('Active Channels', channel, boolean)
        with open('config/' + str(self.server) + '.conf', 'w') as configfile:
            self.config.write(configfile)
        return return_message

    def channelActive(self, channel):
        self.config.read('config/' + str(self.server) + '.conf')
        if not isinstance(channel, str):
            channel = channel.name
        if self.config['Active Channels'][channel] == 'True':
            return True
        return False

    def activeServer(self):
        self.config.read('config/' + str(self.server) + '.conf')
        if self.config['Server Information']['Active'] == 'True':
            return True
        return False

    def togglePerms(self):
        self.config.read('config/' + str(self.server) + '.conf')
        if self.config['Server Information']['Active'] == 'True':
            self.config.set('Server Information', 'Active', 'False')
            return 'disabled'
        else:
            self.config.set('Server Information', 'Active', 'True')
            return 'enabled'
