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
import Queue

#my stuff will go here
#import include.action as action
import include.command as command
import include.database as database
import include.action as action
import include.logger as logger

#### code start ####
legit = True
serverstop = False

#### version ####
v = "4.0 Alpha 4"
print "Starting up MineMon "+v
time.sleep(0.2)
print "Author: Oscar Carlberg"

#### Load settings ####
setting_file = sys.argv[1]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

#### Connect to MySQL ####
myhost = config.get('config', 'mysqlhost')
myuser = config.get('config', 'mysqluser')
mypass = config.get('config', 'mysqlpass')
database.settings(myhost, myuser, mypass)

clients = {}
que = {}

for s in config.sections():
    if s.startswith('client:'):
        alias = s[7:]
        clientdata = dict(config.items(s))

        clients[alias] = clientdata
        que[alias] = Queue.Queue()

print clients
action.load(clients)
database.load(clients)
log_xmlrpc = logger.log_xmlrpc()


class MMCore(xmlrpc.XMLRPC):
    """
    MineMon Core objects to be published for clients.
    """

    def xmlrpc_login(self, server, player):
        #Log the request
        log_xmlrpc.recieved("login", [server, player], server)

        RunCommand = RunCommandThread(que[server], command.login, player, v, server)
        RunCommand.start()
        RunCommand.join()

        #Log the command
        logger.save(server, "GREEN", "LOGIN", player)

        return "OK"

    def xmlrpc_logout(self, server, player):
        #Log the request
        log_xmlrpc.recieved("logout", [server, player], server)

        RunCommand = RunCommandThread(que[server], command.logout, player, server)
        RunCommand.start()
        que[server].join()

        #Log the command
        logger.save(server, "RED", "LOGOUT", player)

        return "OK"

    def xmlrpc_command(self, server, player, command, option1):
        print "["+server+"] "+player+": ["+command+"] ["+option1+"]"
        return "OK"

    def xmlrpc_start(self, server):
        print "["+server+"] Started."
        return "OK"

    def xmlrpc_shutdown(self, server):
        print "["+server+"] was shut down"
        return "OK"

    def xmlrpc_chat(self, server, player, message):
        print "["+server+"] "+player+": ["+message+"]"
        return "OK"

    def xmlrpc_listMethods():
        return "derp", "herp"

    def xmlrpc_fault(self):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        raise xmlrpc.Fault(123, "The fault procedure is faulty.")

#queue = Queue.Queue()

### Threads ####
class RunCommandThread (threading.Thread):
    def __init__(self, queue, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        self._target(*self._args)


if __name__ == '__main__':
    from twisted.internet import reactor
    core = MMCore()
    reactor.listenTCP(7080, server.Site(core))
    reactor.run()


"""
import threading
 
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
 
# Example usage
def someOtherFunc(data, key):
    print "someOtherFunc was called : data=%s; key=%s" % (str(data), str(key))
 
t1 = FuncThread(someOtherFunc, [1,2], 6)
t1.start()
t1.join()

"""
#client

#online
#msg
#command
#system

#server

#command
#login
#logout
#chat
#shutdown
#startup
