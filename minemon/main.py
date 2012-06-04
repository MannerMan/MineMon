# -*- coding: utf-8 -*-
import os
import sys
import thread
import threading
import time
import datetime
from datetime import datetime
import random
import filecmp
import ConfigParser
import socket
import wow as wowish
import smtplib
from email.mime.text import MIMEText

######## somewhat spam

global fileList # global var filelist
running = True # loopen startad

os.system("clear") # tömmer sys w/e

#version
version = "1.7.1"
version = str(version)
print version

if "BETA" in version:
    print "[Warning] Running in BETA mode, assuming options."
    screen = "mc_hax"
    karta = "THIS! IS! BETA!"
    commands = "beta"
    commandsnew = "beta"
    location = "/home/oscar/servers/minecraft/minecraft_server_1_2/"

else:
    screen = raw_input("Enter screenname: ") # screen-namn

    if screen == "mc_hax":
        karta = "http://eth1.nu/minecraft"
        location = "/home/oscar/servers/minecraft/minecraft_server_1_2/"
    elif screen == "mc_real":
        karta = "http://eth1.nu/minecraft"
        location = "/home/oscar/servers/minecraft_real/"
    elif screen == "mc_random":
        karta = "http://eth1.nu/minecraft"
        location = "/home/oscar/servers/minecraft_random/"
    elif screen == "mc_semper":
        karta = "http://eth1.nu/minecraft"
        location = "/home/oscar/servers/minecraft_semper/"

    else:
        location = raw_input("location to minecraft: ")
        karta = raw_input("Enter map-url: ") #karta


# Announce script running
os.system("screen -S "+ screen +" -p 0 -X stuff \"`printf \"say Minecraft Monitor is now running! type !help for commandlist\r\"`\";")
os.system("screen -S "+ screen +" -p 0 -X stuff \"`printf \"say Version [ "+ version +" ]\r\"`\"; sleep 0.1")
os.system("screen -S "+ screen +" -p 0 -X stuff \"`printf \"say Changelog: http://eth1.nu/minemon\r\"`\";")

# Colors is NYAN
class c:
    TEXT = '\033[93m'
    NAME = '\033[94m'
    SYSTEM = '\033[95m'
    LOGIN = '\033[92m'
    FAIL = '\033[96m'
    QUIT = '\033[91m'
    SYS = '\033[0m'

#### Random variables ####

# Sheen wins in many ways
sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]

# Hälsa på trevliga sätt
hello = ["Welcome ", "Greetings ", "Hai ", "Hai thar ", "Oh hai "]

#infostuff
commands = "Please see: http://eth1.nu/minemon for full list."
commandsnew = "!restart"

#Announce var.
#END_ANN = True

#load OP's
op = location
op = op + "ops.txt"

isop = 'troll'

legit = False

#### Load settings ####
setting_file = sys.argv[2]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

enabled = False
silent_enabled = False

#### functions ####

def settings(onoroff):
    global enabled
    setting = config.get('config', onoroff)
    if "enabled" in setting:
        enabled = True
    else:
        enabled = False
        if not "manner" in onoroff or "bukkit" not in onoroff:
            send_task("say This command has been disabled!", 0)

def silent_settings(onoroff):
    global silent_enabled
    setting = config.get('config', onoroff)
    if "enabled" in setting:
        silent_enabled = True
    else:
        silent_enabled = False

def announce():
    while END_ANN:
        time.sleep(3)
        print "qwop"

def extract_name(player):
    # extrahera namn
    global name
    player = player[28:]
    bort = '>'
    player = player.split(bort, 1)[0]
    name = player

def send_task(task, time):
    os.system("screen -S "+ screen +" -p 0 -X stuff \"`printf \""+ task +" \r\"`\"; sleep "+ str(time))

def send_sys(command, time):
    if time == 0:
        execute = command
    else:
        execute = command + " ; sleep " + str(time)
    os.system(execute)

def send_logg(color, func, name):
    if name == 0:
        print color + stamp.strftime("%H:%M:%S") + " | executing " + func
        try:
            l.broadcast(stamp.strftime("%H:%M:%S") + " | executing " + func)
            #client.send(stamp.strftime("%H:%M:%S") + " | executing " + func)
            #client.close()
        except:
            pass
    else:
        print color + stamp.strftime("%H:%M:%S") + " | executing " + func + c.NAME, "[ " + name + " ]"
        try:
            l.broadcast(stamp.strftime("%H:%M:%S") + " | executing " + func + "[ " + name + " ]")
            #client.send(stamp.strftime("%H:%M:%S") + " | executing " + func + " [ " + name + " ]")
            #client.close()
        except:
            pass

def send_logg3(color, func, name, fulhack, attr):
    print color + stamp.strftime("%H:%M:%S") + " | executing " + func + c.NAME, "[ " + name, fulhack, attr + " ]"
    try:
        l.broadcast(stamp.strftime("%H:%M:%S") + " | executing " + func + " [ " + name + " " + fulhack + " " + attr + " ]")
    except:
        pass

def send_chat(chatmsg):
    try:
        q.broadcast(chatmsg)
    except:
        pass

def extr_name():
    lastLine = func_getLastLine()
    global mange
    mange = lastLine
    mange = mange[27:]
    bort = ' '
    mange = mange.split(bort, 1)[0]

def extr_logout():
    global maker
    lastLine = func_getLastLine()
    name = lastLine
    name = name[27:]
    bort = ' '
    maker = name.split(bort, 1)[0]

def who_online():
    global ppl
    global hai
    # extrahera namn
    extr_name()
    manner = random.randint(0,4)
    hai = (hello[manner])

    # kolla vilka som ar inne
    send_task("list", 0.35)
    lastLine = func_getLastLine()
    ppl = lastLine
    ppl = ppl[27:]
    ppl = ppl.split("Connected players: ")[-1]
    ppl = ppl.split(mange, 1)[0]
    if ppl == "":
        ppl = "None. "
    ppl = ppl[:-1]

def op_check():
    if name.lower() in isop:
        return True
    else:
        send_task("say This command is not allowed for non-op's.", 0)

def stop_server():
    send_task("say [Warning] Server restarting in 10 seconds!", 5)
    send_task("say [Warning] Server restarting in 5 seconds!", 5)
    send_task("stop", 4)

def start_server():
    time.sleep(2)
    send_task("java -Xmx700M -Xms700M -jar minecraft_server.jar nogui", 0)

def monsters_change():
    properties = location
    properties = properties + "server.properties"
    mc_settings = properties

    mc_out = "/tmp/tempsett.txt"

    mc_settings = open(mc_settings, "r")
    mc_out = open(mc_out, "w")

    # loop through the test file line by line
    # and write only the lines back out that do
    # not contain the search string
    search = "spawn-monsters="
    for line in mc_settings:
        if search not in line:
            mc_out.write(line)
        else:
            if "False" in line:
                send_task("say [Warning] Turning monsters ON!", 2)
                send_task("say [Warning] Monsters will appear in the next night cycle.", 3)
                stop_server()
                mc_out.write("spawn-monsters=True\n")
                send_logg(c.SYSTEM, "monsters ON", 0)
            if "True" in line:
                send_task("say [Warning] Turning monsters OFF!", 2)
                send_task("say [Warning] Monsters will stop spawning.", 3)
                stop_server()
                mc_out.write("spawn-monsters=False\n")
                send_logg(c.SYSTEM, "monsters OFF", 0)
            send_sys("rm " + str(location) + "server.properties", 0)
            send_sys("mv /tmp/tempsett.txt " + str(location) + "server.properties", 0)
            time.sleep(1)
            start_server()

    # close the file handles
    mc_settings.close()
    mc_out.close()

def check_temp(userlegit):


    #print "debug"
    legituser = userlegit
    global legituser
    templist = location
    filename = templist + "auth.temp"
    lines = open(filename).read().splitlines()
    lines = [x.lower() for x in lines]
    username = legituser
    username = username.lower()
    #print lines

    exploitlist = lines[:]
    global exploitlist

    if username in lines:
        print "got match"
        lines.remove(username)
        print "removed bad user"
        print lines

        write_temphax(lines)

        haxThread = haxLoopingThread(2)
        print "start net1"
        haxThread.start()



def write_temphax(lista):
    templist = location
    filename = templist + "auth.temp"
    f = open(filename, 'w')
    for i in lista:
        f.write(i + "\n")


def deop():
    send_task("say [Warning] " + legituser + " is NOT authed for this session!", 4)
    send_task("say " + legituser + " - You will be un-haxed!", 3)
    send_task("say " + legituser + " - You have 10 seconds to get to safety!", 5)
    send_task("say " + legituser + " - You have 5 seconds to get to safety!", 5)
    send_task("say " + legituser + " was un-haxed", 0.5)
    send_task("gamemode " + legituser + " 0", 0)
    send_logg(c.QUIT, "Unhax", legituser)
    time.sleep(1.4)
    print "Can't find user " + legituser
    print lastLineFixed
    if "Can't find user" in lastLineFixed:
        j = exploitlist
        print j
        write_temphax(j)
        send_task("say exploit-attempt, countermeasure activated.", 0.2)
        print "detected exploit attemt! restore list"

def mail(mailmsg):
    msg = MIMEText(mailmsg)
    msg['Subject'] = 'problemreport from minecraft'
    msg['From'] = "MineMon2"
    msg['Reply-to'] = "donotreply"
    msg['To'] = "Admin"

    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    #fix config-settings here.
    server.login('your_gmail_here','your_password_here')
    server.sendmail('your_gmail_here','reciving_email_here',msg.as_string())
    server.close()

######### Mina imports

silent_settings("networking")
if enabled:
    import network.chatserv as chatserv
    import network.loggserv as loggserv

#### Triggers ####

def trigger():
    if "!help" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        help()

    elif "!hax" in lastLineFixed and not "CONSOLE" in lastLineFixed:
        settings("!hax")
        if enabled:
            hax()

    elif "!xp" in lastLineFixed and not "CONSOLE" in lastLineFixed:
        settings("!xp")
        if enabled:
            xp()

    elif "!unhax" in lastLineFixed and not "CONSOLE" in lastLineFixed:
        settings("!unhax")
        if enabled:
            unhax()

    elif "!sheen" in lastLineFixed:
        settings("!sheen")
        if enabled:
            sheen()

    elif "!day" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!day")
        if enabled:
            day()

    elif "!night" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!night")
        if enabled:
            night()

    elif "!map" in lastLineFixed:
        settings("!map")
        if enabled:
            map()

    elif "logged in with entity" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("login_manner")
        if enabled:
            login()

    elif "!kit" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!kit")
        if enabled:
            kit()

    elif "!tnt" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!tnt")
        if enabled:
            tnt()

    elif "!solonius" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!solonius")
        if enabled:
            solonius()

    elif "!kill" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!kill")
        if enabled:
            kill()

    elif "!bow" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!bow")
        if enabled:
            bow()

    elif "!train" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!train")
        if enabled:
            train()

    elif "!sleep" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!sleep")
        if enabled:
            sleep()

    elif "!version" in lastLineFixed:
        version_mm()

    elif "!stone" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!stone")
        if enabled:
            stone()

    elif "!wood" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!wood")
        if enabled:
            wood()

    elif "!dirt" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!dirt")
        if enabled:
            dirt()

    elif "!rail" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!rail")
        if enabled:
            rail()

    elif "lost connection:" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("logout_manner")
        if enabled:
            lost()

    elif "!monsters" in lastLineFixed:
        settings("!monsters")
        if enabled:
            monsters()

    elif "!list" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!list")
        if enabled:
            list()

    elif "!roll" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!roll")
        if enabled:
            roll()

    elif "!item" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!item")
        if enabled:
            item()

    elif "!tp" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!tp")
        if enabled:
            tp()

    elif "!pull" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!pull")
        if enabled:
            pull()

    elif "!restart" in lastLineFixed:
        settings("!restart")
        if enabled:
            restart()

    elif "!update" in lastLineFixed or "Outdated server!" in lastLineFixed:
        settings("!update")
        if enabled:
            update()

    elif ('Opping' in lastLineFixed or 'De-opping' in lastLineFixed):
        read_op(True)

    elif "!food" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!food")
        if enabled:
            food()

    elif "!wow" in lastLineFixed:
        wowget()

    elif "!temphax" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        settings("!temphax")
        if enabled:
            temphax()

    elif "!report" in lastLineFixed:
        report()

    elif "[INFO] Done (" in lastLineFixed and "CONSOLE" not in lastLineFixed:
        print c.SYS + stamp.strftime("%H:%M:%S") + " | << Starting Server >> "

    elif "[INFO] Saving chunks" in lastLineFixed:
        print c.SYS + stamp.strftime("%H:%M:%S") + " | << Stopping Server >> "

    else:
        mightbechat = lastLineFixed
        if '<' in mightbechat:
            send_chat(mightbechat)
            print c.SYS + stamp.strftime("%H:%M:%S") + " | Sent chatmsg "

####  Actions ####

def help():
    send_task("tell " + name + " commands: " + commands, 0)
    send_logg(c.TEXT, "!help", name)

def sheen():
    win = random.randint(0, 11)
    bro = (sheenstuff[win])
    send_task("say "+ bro, 0)
    send_logg(c.SYSTEM, "!sheen", 0)

def day():
    send_task("time set 10", 0)
    send_logg(c.SYSTEM, "!day", 0)

def night():
    send_task("time set 14000", 0)
    send_logg(c.SYSTEM, "!night", 0)

def map():
    send_task("say Karta: " + karta, 0)
    send_logg(c.SYSTEM, "!map", name)

def login():
    who_online()
    if "S3rR1" in mange:
        send_task("say ALL HAIL S3rR1, member of Mensa!", 0.1)
    else:
        send_task("say "+ hai + mange + "! Connected: " + ppl, 0.1)
    send_task("tell " + mange + " type !help for commands.", 0)
    send_logg(c.LOGIN, "Welcome", mange)
    check_temp(mange)

def kit():
    try:
        item = 276
        for antal in range(0,3):
            item = item + 1
            item = str(item)
            send_task("give " + name +" "+ item + " 1", 0.1)
            item = int(item)
    except (RuntimeError, TypeError, NameError):
        send_task("say [Warning] Execution failed", 0)
    send_logg(c.TEXT, "!kit", name)

def tnt():
    if op_check():
        for antal in range(0,3):
            send_task("give " + name + " 46 64", 0.1)
        send_logg(c.TEXT, "!tnt", name)

def solonius():
    item = 297
    for antal in range(0,4):
        item = item + 1
        send_task("give " + name +" "+ str(item) + " 1", 0.1)
    send_task("give " + name + " 268 1", 0)
    send_logg(c.TEXT, "!solonius", name)

def kill():
    if op_check():
        item = 309
        for antal in range(0,4):
            item = item + 1
            send_task("give " + name +" "+ str(item) + " 1", 0.1)
        send_task("give " + name + " 276 1", 0)
        send_logg(c.TEXT, "!kill", name)

def bow():
    send_task("give " + name + " 261 1", 0)
    for antal in range(0,3):
        send_task("give " + name + " 262 64", 0.1)
    send_logg(c.TEXT, "!bow", name)

def train():
    send_task("give " + name + " 328 5", 0.1)
    send_task("tell " + name + " Do _NOT_ leave empty trains on the rail!", 0)
    send_logg(c.TEXT, "!train", name)

def sleep():
    send_task("give " + name + " 355 5", 0)
    send_logg(c.TEXT, "!sleep", name)

def version_mm():
    send_task("say Minecraft Monitor version: " + version, 0.1)
    send_task("say changelog: http://eth1.nu/minemon", 0)
    send_logg(c.SYSTEM, "!version", 0)

def stone():
    for antal in range(0,5):
        send_task("give " + name + " 4 64", 0.1)
    send_logg(c.TEXT, "!stone", name)

def wood():
    for antal in range(0,5):
        send_task("give " + name + " 5 64", 0.1)
    send_logg(c.TEXT, "!wood", name)

def dirt():
    for antal in range(0,5):
        send_task("give " + name + " 3 64", 0.1)
    send_logg(c.TEXT, "!dirt", name)

def rail():
    for antal in range(0,4):
        send_task("give " + name + " 27 64", 0.1)
    for antal in range(0,2):
        send_task("give " + name + " 28 64", 0.1)
    send_logg(c.TEXT, "!rail", name)

def lost():
    extr_logout()
    send_task("say Goodbye " + maker + "!", 0)
    send_logg(c.QUIT, "quit", maker)

def monsters():
    if op_check():
        monsters_change()

def list():
    send_task("list", 0.2)
    lastLine = func_getLastLine()
    ppl = lastLine
    ppl = ppl[27:]
    send_task("say " + ppl, 0)
    send_logg(c.SYSTEM, "!list", 0)

def roll():
    roll = random.randint(1, 100)
    roll = str(roll)
    send_task("say "+ name + " rolled "+ roll, 0)
    send_logg3(c.SYSTEM, "!roll", name, " ] [", roll)

def item():
    if op_check():
        item = lastLineFixed
        item = item[28:]
        item = item.split("!item ")[-1]
        item = item.replace("\n", "")
        send_task("give " + name +" "+ item +" 64", 0)
        send_logg3(c.TEXT, "!item", name, "] [", item)

def tp():
    #if op_check():
    who = lastLineFixed
    who = who[28:]
    who = who.split("> !tp")[-1]
    who = who.replace("\n", "")
    if who == "":
        send_task("say Need a target!", 0)
    else:

        who = who.split(" ")[-1]
        silent_settings("bukkit")
        if silent_enabled:
            if who.endswith('0m'):
                who = who[:-2]
        send_task("tp " + name +" "+ who, 0)
        send_logg3(c.TEXT, "TP", name, " ] -> [ ", who)

def pull():
    if op_check():
        who = lastLineFixed
        who = who[28:]
        who = who.split("> !pull")[-1]
        who = who.replace("\n", "")
        if who == "":
            send_task("say Need a target!", 0)
        else:
            who = who.split(" ")[-1]
            send_task("tp " + who +" "+ name, 0)
            send_logg3(c.TEXT, "pull", name, " ] <- [ ", who)

def update():
    if op_check() or "CONSOLE" in lastLineFixed:
        server = location
        send_task("say Downloading minecraft_server...", 0)
        send_sys("rm /tmp/minecraft_server.jar", 1)
        send_sys("wget -b --directory-prefix=/tmp/ https://s3.amazonaws.com/MinecraftDownload/launcher/minecraft_server.jar", 5)
        send_task("say Done, comparing versions..", 0.5)
        server = server + "minecraft_server.jar"
        compare = filecmp.cmp('/tmp/minecraft_server.jar', server)
        if compare == True:
            send_task("say Latest version installed", 1)
            send_task("say - Doing nothing.", 1)
            send_logg(c.SYSTEM, "update [No update found]", 0)
        else:
            send_task("say Versions does not match!", 3)
            send_task("say Im going to try something crazy and update myself!", 4)
            send_task("say Dont be mad if shit goes bad :3", 2)
            stop_server()
            send_sys("rm "+ server, 1)
            send_sys("mv /tmp/minecraft_server.jar "+ server, 1)
            start_server()
            send_logg(c.SYSTEM, "update [Updated server!]", 0)

def hax():
    if op_check():
        send_task("gamemode " + name + " 1", 0)
        send_logg(c.SYSTEM, "hax", name)

def unhax():
    if op_check():
        send_task("gamemode " + name + " 0", 0)
        send_logg(c.SYSTEM, "unhax", name)

def xp():
    if op_check():
        for antal in range(0,4):
            send_task("xp " + name + " 5000", 0.2)
        send_logg(c.SYSTEM, "XP 5000", name)

def restart():
    if op_check() or "CONSOLE" in lastLineFixed:
        send_task("say Okay =(", 1)
        stop_server()
        start_server()

def read_op(notify):
    global isop
    opfile = open(op, 'r')
    isop = opfile.read()
    if notify:
        send_task("say Detecting change in OP's, refreshing list!", 0)
        send_logg(c.SYSTEM, "OP-change", 0)

def food():
    for antal in range(0,5):
        send_task("give " + name + " 363 64", 0.1)
    send_logg(c.TEXT, "!food", name)

def wowget():
    #if op_check():
    who = lastLineFixed
    who = who[28:]
    who = who.split("> !tp")[-1]
    who = who.replace("\n", "")
    if who == "":
        send_task("say Need a charname!", 0)
    else:
        who = who.split(" ")[-1]
        char = wowish.getchar(who)
        char = str(char)
        char = char.replace(",", "")
        char = char.replace("'", "")
        char = char.replace(")", "")
        char = char.replace("(", "")

        send_task("say "+char, 0)
        send_logg3(c.TEXT, "!wow", name, "] [", who)


def temphax():
    if op_check():
        templist = location
        templist = templist + "auth.temp"
        tempauth = templist
        print tempauth

    #authlist = "/tmp/tempsett.txt"

        tempauth = open(tempauth, "a")

        who = lastLineFixed
        who = who[28:]
        who = who.split("> !temphax")[-1]
        who = who.replace("\n", "")

        if who == "":
            send_task("say Need a target!", 0)
        else:
            who = who.split(" ")[-1]
            send_task("gamemode " + who + " 1", 0)
            send_task("say "+ who + " is now haxed for this session!", 0)

        tempauth.write(who + "\n")
        send_logg3(c.TEXT, "!temphax", name, "] -> [", who)

def report():
        issue = lastLineFixed
        issue = issue[28:]
        issue = issue.split("> !report")[-1]
        issue = issue.replace("\n", "")
        issue = "[ "+name+" ] "+issue
        mail(issue)
        send_task("say Problem was reported to the administrator!", 0)
        send_logg(c.SYSTEM, "report", name)


#### Mainloop ####
def func_checkLastLine(lastLine):
    global lastLineFixed
    global stamp
    global name
    lastLineFixed = lastLine.replace("\n", "")
    stamp = datetime.now()
    extract_name(lastLine)
    #name = lastLine
    #name = name[28:]
    #bort = '>'
    #name = name.split(bort, 1)[0]
    trigger()

#### Announce loop ####
#announce()

#### start of S3rR1 hax, i dont even what is this ####
class newLoopingThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        func_loop()

def func_loop():
    tempList = fileList
    while running:
        time.sleep(0.5)
        fileHandle = open(file, 'r')
        newLines = fileHandle.readlines()
        if newLines != tempList and tempList != None:
            tempList = newLines
            newList = [item for item in tempList if item != '\n']
            if len(newList) > 0: func_checkLastLine(newList[len(newList) - 1])

def func_getLastLine():
    fileHandle = open(file, 'r')
    allLines = fileHandle.readlines()
    allLines = [item for item in allLines if item != '\n']
    return allLines[len(allLines) - 1]

class netLoopingThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        global q
        q = chatserv
        q.start()

class netLoopingThread2 (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        global l
        l = loggserv
        l.start()

class haxLoopingThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        global h
        h = deop
        h()



#### app startz ####
if len(sys.argv) <= 2:
    print "You need to specify the log-file and settings-file as a parameter."
else:
    file = sys.argv[1]

    if (os.path.isfile(file) == False):
        print "The filename you have entered does not exist."
    else:

        fileHandle = open(file, 'r')
        fileList = fileHandle.readlines()

        print "Press any key to end loop...\n"
        #testing()
        read_op(False)
        loopThread = newLoopingThread(1)
        loopThread.start()
        silent_settings("networking")
        if enabled:

            netThread = netLoopingThread(2)
            print "start net1"
            netThread.start()
            print "started net1"

            netThread2 = netLoopingThread2(3)
            print "start net2"
            netThread2.start()
            print "started net2"


        raw_input()
        running = False
        send_task("say Minecraft Monitor [ " + version + " ] stopped!", 0.1)
        print "Waiting for looping thread to stop..."
        while loopThread.isAlive(): time.sleep(0.5)
        settings("networking")
        if enabled:
            while netThread.isAlive(): time.sleep(0.5)

#END_ANN = False

print "\nEnd of program.\n\n"
#client.close()

