import os
import sys

def Reboot():
    os.execv(sys.executable, ['python3'] + sys.argv)
