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

#### Load settings ####
setting_file = sys.argv[1]
config = ConfigParser.RawConfigParser()
config.read(setting_file)

alias = config.get('config', 'alias')
port = config.get('config', 'port')
serverip = config.get('config', 'serverip')

#### XML RPC Interface ####
class MMClient(xmlrpc.XMLRPC):
    """
    Client objects that MMServer calls.
    """

    def xmlrpc_mconline(self):
        print "online"
        return "OK"

    def xmlrpc_say(self, msg):
        print msg
        return "OK"

    def xmlrpc_fault(self):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        raise xmlrpc.Fault(123, "The fault procedure is faulty.")



#### Log Parsing ####
def analyze(log):
    print "NEW: "+log

#### Follow the log ####
def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
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

if __name__ == '__main__':
    from twisted.internet import reactor
    r = MMClient()
    reactor.callInThread(read_log)
    reactor.listenTCP(int(port), server.Site(r))
    reactor.run()