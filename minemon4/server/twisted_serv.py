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

#my stuff will go here
#import include.action as action
import include.command as command
import include.database as database

#### code start ####
legit = True
serverstop = False

#### version ####
v = "4.0 Alpha 1"
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

class MMCore(xmlrpc.XMLRPC):
    """
    MineMon Core objects to be published for clients.
    """

    def xmlrpc_login(self, server, player):
        print "["+server+"] "+player+" logged in"
        command.login(player, v, server)
        return "OK"

    def xmlrpc_logout(self, server, player):
        print "["+server+"] "+player+" logged off"
        command.logout(player, server)
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

if __name__ == '__main__':
    from twisted.internet import reactor
    core = MMCore()
    reactor.listenTCP(7080, server.Site(core))
    reactor.run()


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
