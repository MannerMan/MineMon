# -*- coding: utf-8 -*-

# importing regular stuff
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

#my stuff will go here
import include.action as action
import include.logreader as logreader
import include.command as command
import include.logger as log
import include.database as database
import include.timetrack as timetrack

#### code start ####
legit = True

#### version ####
version = "3.0.0 beta 2"
version = str(version)
print "starting up MineMon "+version
time.sleep(0.2)
print "Author: Oscar Carlberg"

#### Load settings ####
setting_file = sys.argv[1]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

#### Connect to MC rcon ####
mchost = config.get('config', 'rhost')
mcport = config.get('config', 'rport')
mcpwd = config.get('config', 'rpass')

#### Connect to MySQL ####
myhost = config.get('config', 'mysqlhost')
myuser = config.get('config', 'mysqluser')
mypass = config.get('config', 'mysqlpass')
mydb = config.get('config', 'mysqldb')
database.settings(myhost, myuser, mypass, mydb)

#### some settings-var ####
mcpath = config.get('config', 'mcpath')
mapurl = config.get('config', 'mapurl')
helpurl = config.get('config', 'helpurl')
screen = config.get('config', 'screen')

gmail = config.get('config', 'gmail')
gpw = config.get('config', 'gmailpw')
mailrcvr = config.get('config', 'sendto')

#### announce that i'm running ####
action.connect(mchost, mcport, mcpwd)
action.load(gmail, gpw, mailrcvr, screen)
action.say("Minecraft Monitor Version "+version+" now running!", 1)
action.say("Type !help for available commands", 0)

ops = action.load_op(mcpath)
timetrk=timetrack.playtime()

#### check if enabled & op func ####

def enabled(onoroff):
    try:
        setting = config.get('config', onoroff)
    except:
        setting = "disabled"
        print "NO setting entry for "+onoroff+", disabled."
    if "enabled" in setting:
        return True
    else:
        action.say("This command has been disabled!", 0)
        return False

def check_op(name):
    if name.lower() in ops:
        return True
    else:
        action.say("This command is not allowed for non-op's.", 0)

#### Trigger on chattlog stuff ####
def trigger(name):
    if "!sheen" in chatlog:
        if enabled("!sheen"):
            command.sheen()
            log.save(timestamp, "TEXT", "!sheen", name)

    elif "logged in with entity" in chatlog and not "CONSOLE" in chatlog:
        if enabled("login_manner"):
            player = command.login(chatlog, version, helpurl)
            log.save(timestamp, "GREEN", "Login:", player)

    elif "lost connection:" in chatlog and not "CONSOLE" in chatlog:
        if enabled("logout_manner"):
            player = command.logout(chatlog)
            log.save(timestamp, "RED", "Logout:", player)

    elif "!hax" in chatlog and not "[Rcon]" in chatlog:
        if enabled("!hax"):
            if check_op(name):
                command.hax(name)
                log.save(timestamp, "SYSTEM", "!hax", name)

    elif "!unhax" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!unhax"):
            if check_op(name):
                command.unhax(name)
                log.save(timestamp, "SYSTEM", "!unhax", name)

    elif "!day" in chatlog:
        if enabled("!day"):
            command.day()
            log.save(timestamp, "SYSTEM", "!day", name)

    elif "!night" in chatlog:
        if enabled("!night"):
            command.night()
            log.save(timestamp, "SYSTEM", "!night", name)

    elif "!tp" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!tp"):
            who = command.tp(name, chatlog)
            log.save2(timestamp, "TEXT", "!tp", name, "] [ -> ] [", who)

    elif "!pull" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!pull"):
            if check_op(name):
                who = command.pull(name, chatlog)
                log.save2(timestamp, "TEXT", "!pull", name, "] [ <- ] [", who)

    elif "!map" in chatlog:
        if enabled("!map"):
            command.map(mapurl)
            log.save(timestamp, "SYSTEM", "!map", name)

    elif "!help" in chatlog:
        if enabled("!help"):
            command.help(helpurl)
            log.save(timestamp, "SYSTEM", "!help", name)

    elif "!version" in chatlog:
        action.say("Running MineMon version: " + version, 0)
        log.save(timestamp, "SYSTEM", "!version", name)

    elif "!list" in chatlog:
        action.say("Deprecated. Press <tab>", 0)

    elif "!roll" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!roll"):
            roll = command.roll(name)
            log.save2(timestamp, "TEXT", "!roll", name, "] [", roll)

    elif "!rain" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!rain"):
            command.rain()
            log.save(timestamp, "SYSTEM", "!rain", name)

    elif "!xp" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!xp"):
            if check_op(name):
                command.xp(name)
                log.save(timestamp, "TEXT", "!xp", name)

    elif "!kit" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!kit"):
            command.kit(name)
            log.save(timestamp, "TEXT", "!kit", name)

    elif "!leatherset" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!leatherset"):
            command.leatherset(name)
            log.save(timestamp, "TEXT", "!leatherset", name)

    elif "!diamondset" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!diamondset"):
            if check_op(name):
                command.diamondset(name)
                log.save(timestamp, "TEXT", "!diamondset", name)

    elif "!bow" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!bow"):
            command.bow(name)
            log.save(timestamp, "TEXT", "!bow", name)

    elif "!train" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!train"):
            command.train(name)
            log.save(timestamp, "TEXT", "!train", name)

    elif "!sleep" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!sleep"):
            command.sleep(name)
            log.save(timestamp, "TEXT", "!sleep", name)

    elif "!rail" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!rail"):
            command.rail(name)
            log.save(timestamp, "TEXT", "!rail", name)

    elif "!food" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!food"):
            command.food(name)
            log.save(timestamp, "TEXT", "!food", name)

    elif "!item" in chatlog and not "[Rcon]" in chatlog:
        if enabled("!item"):
            if check_op(name):
                item = command.item(name, chatlog)
                log.save2(timestamp, "TEXT", "!item", name, "] [", item)

    elif "!restart" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!restart"):
            if check_op(name):
                command.restart()
                log.save(timestamp, "SYSTEM", "!restart", name)

    elif "!monsters" in chatlog:
        if enabled("!monsters"):
            if check_op(name):
                onoff = command.monsters(mcpath)
                log.save2(timestamp, "SYSTEM", "!monsters", name, "] [", onoff)

    elif "!update" in chatlog:
        if enabled("!update"):
            if check_op(name) or "CONSOLE" in chatlog:
                status = command.update(mcpath, mcport)
                log.save2(timestamp, "SYSTEM", "!update", name, "] [", status)

    elif "!temphax" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!temphax"):
            if check_op(name):
                who = command.temphax(chatlog)
                log.save2(timestamp, "TEXT", "!temphax", name, "] -> [", who)

    elif "!report" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!report"):
            command.mail(name, chatlog)
            log.save(timestamp, "SYSTEM", "!report", name)
            
    elif "!played" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!played"):
            command.played(name)
            log.save(timestamp, "TEXT", "!played", name)



    elif "Opping" in chatlog or "De-opping" in chatlog:
        global ops
        ops = action.load_op(mcpath)
        action.say("Detecting change in OP's, refreshing list!", 0)
        log.save(timestamp, "SYSTEM", "OP-refresh", "SYSTEM")

    elif "[INFO] Done (" in chatlog or "[INFO] RCON running on" in chatlog:
        print "< STARTING SERVER > - Reconnecting to rcon"
        action.connect(mchost, mcport, mcpwd)

    elif "[INFO] Saving chunks" in chatlog:
        print "< STOPPING SERVER >"


    #old non-supported commands
    elif "!tnt" in chatlog or "!stone" in chatlog or "!wood" in chatlog or "!dirt" in chatlog:
        action.say("Deprecated command. use !hax or !item", 0)



#### Name extractor
def extract_name(player):
    # extrahera namn
    player = player[28:]
    bort = '>'
    player = player.split(bort, 1)[0]
    return player

#### Mainloop ####
def func_checkLastLine(lastLine):
    global chatlog
    global timestamp
    chatlog = lastLine.replace("\n", "")
    timestamp = datetime.now()
    name = extract_name(lastLine)
    trigger(name)

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
        fileHandle = open(logfile, 'r')
        newLines = fileHandle.readlines()
        if newLines != tempList and tempList != None:
            tempList = newLines
            newList = [item for item in tempList if item != '\n']
            if len(newList) > 0: func_checkLastLine(newList[len(newList) - 1])

def func_getLastLine():
    fileHandle = open(logfile, 'r')
    allLines = fileHandle.readlines()
    allLines = [item for item in allLines if item != '\n']
    return allLines[len(allLines) - 1]

#### Start application
running = True
logfile = mcpath + "server.log"

fileHandle = open(logfile, 'r')
fileList = fileHandle.readlines()

loopThread = newLoopingThread(1)
loopThread.start()

if enabled("timetrack"):
    print "Timetracking enabled, starting timer"
    timetrk.start()


#### exit ####
print "press any key to exit"
raw_input()
running = False
print "Waiting for looping thread to stop..."
while loopThread.isAlive(): time.sleep(0.5)

if enabled("timetrack"):
    timetrk.stop()
    time.sleep(1)
    
action.say("Minecraft Monitor Version "+version+" stopped!", 0)

#lol = action.send("list")
#print lol