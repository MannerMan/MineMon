#colors
color = {   'SYSTEM': '\033[95m',
            'NAME': '\033[94m',
            'TEXT': '\033[93m',
            'GREEN': '\033[92m',
            'FAIL': '\033[96m',
            'RED': '\033[91m',
            'SYS': '\033[0m',}

def save(timestamp, c, command, name):
    print color[c] + timestamp.strftime("%H:%M:%S") + " | executing " + command + color["NAME"], "[ " + name + " ]" + color["SYS"]

def save2(timestamp, c, command, name, fulhack, target):
    print color[c] + timestamp.strftime("%H:%M:%S") + " | executing " + command + color["NAME"], "[ " + name, fulhack, target + " ]" + color["SYS"]