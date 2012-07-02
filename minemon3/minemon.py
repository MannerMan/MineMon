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

#### code start ####

#### version ####
version = "3.0.0 alpha 2"
version = str(version)
print "starting up MineMon "+version
time.sleep(0.2)
print "Author: Oscar Carlberg"

#### Load settings ####
setting_file = sys.argv[1]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

#### Connect to MC rcon ###
mchost = config.get('config', 'rhost')
mcport = config.get('config', 'rport')
mcpwd = config.get('config', 'rpass')

#### announce that i'm running ####
action.connect(mchost, mcport, mcpwd)
action.say("Minecraft Monitor Version "+version+" now running!", 1)
action.say("Type !help for available commands", 0)

#### check if enabled func ####

def enabled(onoroff):
    setting = config.get('config', onoroff)
    if "enabled" in setting:
        return True
    else:
        action.say("This command has been disabled!", 0)
        return False


#### Trigger on chattlog stuff ####
def trigger(name):
    if "!sheen" in lastLineFixed:
        if enabled("!sheen"):
            command.sheen()
            log.save(timestamp, "SYSTEM", "!sheen", name)

#### Name extractor
def extract_name(player):
    # extrahera namn
    player = player[28:]
    bort = '>'
    player = player.split(bort, 1)[0]
    return player

#### Mainloop ####
def func_checkLastLine(lastLine):
    global lastLineFixed
    global timestamp
    lastLineFixed = lastLine.replace("\n", "")
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

#### Start application
running = True
file = config.get('config', 'logpath')

fileHandle = open(file, 'r')
fileList = fileHandle.readlines()

loopThread = newLoopingThread(1)
loopThread.start()


#### exit ####
print "press any key to exit"
raw_input()
running = False
print "Waiting for looping thread to stop..."
while loopThread.isAlive(): time.sleep(0.5)
action.say("Minecraft Monitor Version "+version+" stopped!", 0)

#lol = action.send("list")
#print lol