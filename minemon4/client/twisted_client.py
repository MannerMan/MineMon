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
from twisted.web import xmlrpc, server
from twisted.internet.threads import deferToThread
import xmlrpclib

#### Load settings ####
setting_file = sys.argv[1]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

alias = config.get('config', 'alias')
port = config.get('config', 'port')
serverip = config.get('config', 'serverip')
serverport = config.get('config', 'serverport')

running = True

#### XML RPC Interface ####
class MMClient(xmlrpc.XMLRPC):
    """
    Client objects that MMServer calls.
    """

    def xmlrpc_mconline(self):
        print "online"
        return "OK"

    def xmlrpc_say(self, msg):
        log = "["+current_date()+"] ["+current_time()+"] [Say] ["+msg+"]"
        print log

        #log the command
        write2comlog(log)

        #log the request
        log_xmlrpc.recieved("say", [msg])

        return "OK"

    def xmlrpc_fault(self):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        raise xmlrpc.Fault(123, "The fault procedure is faulty.")


#### XML RPC 2 Server ####
mmserver=xmlrpclib.ServerProxy("http://"+serverip+":"+serverport)

#### Logging ####

def write2comlog(msg):
    try:
        with open('logs/command_'+alias+'.log', 'a') as file:
            file.write(msg+"\n")
    except:
        os.system('touch logs/command_'+alias+'.log')
        with open('logs/command_'+alias+'.log', 'a') as file:
            file.write(msg+"\n")

def write2xmllog(msg):
    try:
        with open('logs/xmlrpc_'+alias+'.log', 'a') as file:
            file.write(msg+"\n")
    except:
        os.system('touch logs/xmlrpc_'+alias+'.log')
        with open('logs/xmlrpc_'+alias+'.log', 'a') as file:
            file.write(msg+"\n")

class log_xmlrpc:
    def recieved(self, req, parameters):
        parameters = ' | '.join(parameters)
        
        write2xmllog("["+ current_date() +"] ["+current_time()+"] [XMLRPC] [<--] [INCOMING] ["+req+"] ["+parameters+"]")

    def sent(self, req, parameters):
        parameters = ' | '.join(parameters)
        
        write2xmllog("["+ current_date() +"] ["+current_time()+"] [XMLRPC] [-->] [OUTGOING] ["+req+"] ["+parameters+"]")

log_xmlrpc = log_xmlrpc()

#### Log Parsing ####
def analyze(log):
    #General playernick extractor, does only work for regular !commands
    nick = extract_name(log)

    if "logged in with entity" in log and not "[Rcon]" in log:
        #get nick
        name = extract_visit_name(log, '[')

        #log the request
        log_xmlrpc.sent("login", [alias, name])

        #send the XML-RPC Request
        mmserver.login(alias, name)


    elif "lost connection:" in log and not "[Rcon]" in log:
        #get nick
        name = extract_visit_name(log, ' ')

        #log the request
        log_xmlrpc.sent("logout", [alias, name])

        #send the XML-RPC Request
        mmserver.logout(alias, name)



#### Parsing functions ####
def extract_visit_name(log, bort):
    name = log
    name = name[27:]
    return name.split(bort, 1)[0]

def extract_name(player):
    # extrahera namn
    player = player[28:]
    bort = '>'
    player = player.split(bort, 1)[0]
    return player

def current_time():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%H:%M:%S.%f")
    return timestamp[:-3]

def current_date():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d")
    return timestamp

#### Follow the log ####
def follow(thefile):
    global running
    thefile.seek(0,2) # Go to the end of the file
    while running:
         line = thefile.readline()
         if not line:
             time.sleep(0.05) # Sleep briefly
             continue
         yield line

def read_log():
    logfile = open("/home/oscar/mcserv/server.log")
    loglines = follow(logfile)
    for line in loglines:
        stamp = datetime.now()
        analyze(line)


#### Stop client ####
def stop_app():
    global running
    print "press any key to exit"
    raw_input()
    print "Stopping threads.."
    running = False
    reactor.stop()
    print "Bye!"

### Threads ####
class ReadLogThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        read_log()

class StopAppThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        stop_app()


#### Start program ###
from twisted.internet import reactor
r = MMClient()

readThread = ReadLogThread(2)
readThread.start()
print "Started Log-reader thread"

StopThread = StopAppThread(1)
StopThread.start()
print "Started Stop-event thread"

reactor.listenTCP(int(port), server.Site(r))
reactor.run()