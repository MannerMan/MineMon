#!/usr/local/bin/python
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
serverstop = False

#### version ####
v = "3.3.1"
print "Starting up MineMon "+v
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
mc_mem = config.get('config', 'mc_mem')

gmail = config.get('config', 'gmail')
gpw = config.get('config', 'gmailpw')
mailrcvr = config.get('config', 'sendto')

#### announce that i'm running ####
try:
    action.connect(mchost, mcport, mcpwd)
except:
    print "Coult not connect to Minecraft Rcon!"
    sys.exit()

action.load(gmail, gpw, mailrcvr, screen, mc_mem)
action.say("§aMinecraft Monitor Version "+v+" now running!", 1)
action.say("§aType !help for available commands", 0)

ops = action.load_op(mcpath)
timetrk=timetrack.playtime()

#### check if enabled & op func ####

def enabled(onoroff):
    #Check if regular command or feature
    if "!" in onoroff:
        setting = database.check_enabled_command(onoroff)

        #If not enabled say so.
        if not setting:
            action.say("This command has been disabled for this world!", 0)
        return setting

    else:
        try:
            setting = config.get('config', onoroff)
        except:
            setting = "disabled"
            print "NO setting entry for "+onoroff+", disabled."
        if "enabled" in setting:
            return True
        else:
            action.say("This command has been disabled for this world!", 0)
            return False

def silent_enabled(onoroff):
    try:
        setting = config.get('config', onoroff)
    except:
        setting = "disabled"
        print "NO setting entry for "+onoroff+", disabled."
    if "enabled" in setting:
        return True
    else:
        return False

def check_op(name, command):
    op = database.check_command_op(command)

    #If commmand does not need op, return OK
    if not op:
        return True

    else:
        #else, check if user is op, and return true
        if name.lower() in ops:
            return True

        #if not, deny.
        else:
            action.say("This command is not allowed for non-op's.", 0)

#### Trigger on chattlog stuff ####
def trigger(name):
    global serverstop

    if "!help" in chatlog:
        if enabled("!help"):
            if check_op(name, "!help"):
                command.help(helpurl, chatlog)
                log.save(timestamp, "SYSTEM", "!help", name)

    elif "!sheen" in chatlog:
        if enabled("!sheen"):
            if check_op(name, "!sheen"):
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
            if check_op(name, "!hax"):
                command.hax(name)
                log.save(timestamp, "SYSTEM", "!hax", name)

    elif "!unhax" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!unhax"):
            if check_op(name, "!unhax"):
                command.unhax(name)
                log.save(timestamp, "SYSTEM", "!unhax", name)

    elif "!adv" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!adv"):
            if check_op(name, "!adv"):
                command.adv(name)
                log.save(timestamp, "SYSTEM", "!adv", name)

    elif "!day" in chatlog:
        if enabled("!day"):
            if check_op(name, "!day"):
                command.day()
                log.save(timestamp, "SYSTEM", "!day", name)

    elif "!night" in chatlog:
        if enabled("!night"):
            if check_op(name, "!night"):
                command.night()
                log.save(timestamp, "SYSTEM", "!night", name)

    elif "!tp" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!tp"):
            if check_op(name, "!tp"):
                who = command.tp(name, chatlog)
                log.save2(timestamp, "TEXT", "!tp", name, "] -> [", who)

    elif "!pull" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!pull"):
            if check_op(name, "!pull"):
                who = command.pull(name, chatlog)
                log.save2(timestamp, "TEXT", "!pull", name, "] <- [", who)

    elif "!map" in chatlog:
        if enabled("!map"):
            if check_op(name, "!map"):
                command.map(mapurl)
                log.save(timestamp, "SYSTEM", "!map", name)

    elif "!version" in chatlog:
        if enabled("!version"):
            if check_op(name, "!version"):
                command.version(v)
                log.save(timestamp, "SYSTEM", "!version", name)

    elif "!list" in chatlog:
        action.say("Deprecated. Press Tab on your keyboard", 0)

    elif "!roll" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!roll"):
            if check_op(name, "!roll"):
                roll = command.roll(name)
                log.save2(timestamp, "TEXT", "!roll", name, "] [", roll)

    elif "!rain" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!rain"):
            if check_op(name, "!rain"):
                command.rain()
                log.save(timestamp, "SYSTEM", "!rain", name)

    elif "!xp" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!xp"):
            if check_op(name, "!xp"):
                command.xp(name)
                log.save(timestamp, "TEXT", "!xp", name)

    elif "!kit" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!kit"):
            if check_op(name, "!kit"):
                command.kit(name)
                log.save(timestamp, "TEXT", "!kit", name)

    elif "!leatherset" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!leatherset"):
            if check_op(name, "!leatherset"):
                command.leatherset(name)
                log.save(timestamp, "TEXT", "!leatherset", name)

    elif "!diamondset" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!diamondset"):
            if check_op(name, "!diamondset"):
                command.diamondset(name)
                log.save(timestamp, "TEXT", "!diamondset", name)

    elif "!bow" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!bow"):
            if check_op(name, "!bow"):
                command.bow(name)
                log.save(timestamp, "TEXT", "!bow", name)

    elif "!train" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!train"):
            if check_op(name, "!train"):
                command.train(name)
                log.save(timestamp, "TEXT", "!train", name)

    elif "!sleep" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!sleep"):
            if check_op(name, "!sleep"):
                command.sleep(name)
                log.save(timestamp, "TEXT", "!sleep", name)

    elif "!rail" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!rail"):
            if check_op(name, "!rail"):
                command.rail(name)
                log.save(timestamp, "TEXT", "!rail", name)

    elif "!food" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!food"):
            if check_op(name, "!food"):
                command.food(name)
                log.save(timestamp, "TEXT", "!food", name)

    elif "!item" in chatlog and not "[Rcon]" in chatlog:
        if enabled("!item"):
            if check_op(name, "!item"):
                item = command.item(name, chatlog)
                log.save2(timestamp, "TEXT", "!item", name, "] [", item)

    elif "!restart" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!restart"):
            if check_op(name, "!restart"):
                command.restart()
                log.save(timestamp, "SYSTEM", "!restart", name)

    elif "!monsters" in chatlog:
        if enabled("!monsters"):
            if check_op(name, "!monsters"):
                onoff = command.monsters(mcpath)
                log.save2(timestamp, "SYSTEM", "!monsters", name, "] [", onoff)

    elif "!update" in chatlog:
        if enabled("!update"):
            if check_op(name, "update") or "CONSOLE" in chatlog:
                status = command.update(mcpath, mcport)
                log.save2(timestamp, "SYSTEM", "!update", name, "] [", status)

    elif "!temphax" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!temphax"):
            if check_op(name, "!temphax"):
                who = command.temphax(chatlog)
                log.save2(timestamp, "TEXT", "!temphax", name, "] -> [", who)

    elif "!report" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!report"):
            if check_op(name, "!report"):
                command.mail(name, chatlog, False)
                log.save(timestamp, "SYSTEM", "!report", name)

    elif "!played" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!played"):
            if check_op(name, "!played"):
                command.played(name)
                log.save(timestamp, "TEXT", "!played", name)

    elif "!world" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!world"):
            if check_op(name, "!world"):
                success = command.world(name, chatlog, mcpath)
                if success:
                    log.save2(timestamp, "SYSTEM", "!world", name, "] [", success)

    elif "!clear" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!clear"):
            if check_op(name, "!clear"):
                command.clear(name)
                log.save(timestamp, "TEXT", "!clear", name)

    elif "!spawn" in chatlog and not "CONSOLE" in chatlog:
        if enabled("!spawn"):
            if check_op(name, "!spawn"):
                command.spawn(name)
                log.save(timestamp, "TEXT", "!spawn", name)


    elif "Opped" in chatlog or "De-opped" in chatlog:
        global ops
        ops = action.load_op(mcpath)
        action.say("Detecting change in OP's, refreshing list!", 0)
        log.save(timestamp, "SYSTEM", "OP-refresh", "SYSTEM")

    elif "[INFO] Done (" in chatlog or "[INFO] RCON running on" in chatlog:
        print "< STARTING SERVER > - Reconnecting to rcon"
        action.connect(mchost, mcport, mcpwd)
        log.raw_log("< STARTING SERVER >")
        serverstop = False
        global timetrk
        if silent_enabled("timetrack"):
            timetrk=timetrack.playtime()
            timetrk.start()
            print "< Playtime-tracking started >"


    elif "[INFO] Saving chunks" in chatlog and serverstop == False:
        print "< STOPPING SERVER >"
        log.raw_log("< STOPPING SERVER >")
        serverstop = True
        if silent_enabled("timetrack"):
            try:
                timetrk.stop()
                while timetrk.isAlive():
                    time.sleep(1)
                del timetrk
                print "< Playtime-tracking stopped >"
            except:
                print "Could not stop timetrack!"
                log.raw_log("Could not stop timetrack!")

    #old non-supported commands
    elif "!tnt" in chatlog or "!stone" in chatlog or "!wood" in chatlog or "!dirt" in chatlog:
        action.say("Deprecated command. use !hax or !item", 0)

    elif "[SEVERE]" in chatlog or "(SourceFile:" in chatlog and not "<" in chatlog:
        command.mail("SYSTEM", "MINECRAFT SEVERE EXCEPTION - TRYING TO RESTART", True)
        action.say("§c[FATAL]: Minecraft Server encountered a serious error.", 4)
        action.say("§c[WARNING] MineMon will try to restart the server as a precaution", 3)
        time.sleep(2)
        command.restart()
        
    elif "qwop" in chatlog:
        command.late()

    else:
        if '<' in chatlog:
            log.save_chat(name, chatlog)



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

if silent_enabled("timetrack"):
    print "Timetracking enabled, starting timer"
    timetrk.start()

#log the start
log.raw_log("Minecraft Monitor Version "+v+" started!")

#### exit ####
print "press any key to exit"
raw_input()
running = False
print "Waiting for looping thread to stop..."
while loopThread.isAlive(): time.sleep(0.5)

if enabled("timetrack"):
    try:
        timetrk.stop()
        time.sleep(1)
    except:
        print "Could not stop timetracking, although its enabled - perhaps MC is not running?"

action.say("§cMinecraft Monitor Version "+v+" stopped!", 0)

#log the shutdown
log.raw_log("Minecraft Monitor Version "+v+" stopped!")
