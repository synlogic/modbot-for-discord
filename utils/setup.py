import os

def runSetup():
    if not os.path.exists('config/'):
        os.makedirs('config')
    if not os.path.exists('texts/'):
        os.makedirs('texts')
    if not os.path.exists('commands/'):
        os.makedirs('commands')
    if not os.path.exists('utils/'):
        os.makedirs('utils')
