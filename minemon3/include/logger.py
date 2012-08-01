import database

mysql = database.log()

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

    #save to the raw log
    raw_log("executing "+command+ " [ " + name + " ]")

    #if usertrigged command, save to the user command-log
    if "!" in command:
        mysql.add(command, name)

def save2(timestamp, c, command, name, fulhack, target):
    print color[c] + timestamp.strftime("%H:%M:%S") + " | executing " + command + color["NAME"], "[ " + name, fulhack, target + " ]" + color["SYS"]

    #save to the raw log
    raw_log("executing " + command + " [ " + name +" "+ fulhack +" "+ target + " ]")

    #temp
    if "!update" in command:
        #do nothing as of now.
        pass

    #if usertrigged command, save to the user command-log
    elif "!" in command:
        mysql.addopt(command, name, target)

def raw_log(msg):
    mysql.raw(msg)

def save_chat(name, chatlog):
    chatlog = chatlog[28:]
    chatlog = chatlog.replace(name, "", 1)
    msg = chatlog[2:]
    mysql.chat(name, msg)