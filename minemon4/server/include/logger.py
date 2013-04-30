# -*- coding: utf-8 -*-

import time
import datetime
from datetime import datetime
import io
import os

#colors
color = {   'SYSTEM': '\033[95m',
            'NAME': '\033[94m',
            'TEXT': '\033[93m',
            'GREEN': '\033[92m',
            'FAIL': '\033[96m',
            'RED': '\033[91m',
            'SYS': '\033[0m',}

def current_time():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%H:%M:%S.%f")
    return timestamp[:-3]

def current_date():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d")
    return timestamp

def write2comlog(msg, alias):
    uni = type(msg)
    if uni == str:
        msg = unicode(msg, "utf-8")

    try:
        with io.open('logs/commands_'+alias+'.log', 'a', encoding='utf-8') as file:
            file.write(msg+"\n")
    except:
        os.system('touch logs/commands_'+alias+'.log')
        with io.open('logs/commands_'+alias+'.log', 'a', encoding='utf-8') as file:
            file.write(msg+"\n")

def write2xmllog(msg, alias):
    uni = type(msg)
    if uni == str:
        msg = unicode(msg, "utf-8")

    try:
        with io.open('logs/xmlrpc_'+alias+'.log', 'a', encoding='utf-8') as file:
            file.write(msg+"\n")
    except:
        os.system('touch logs/xmlrpc_'+alias+'.log')
        with io.open('logs/xmlrpc_'+alias+'.log', 'a', encoding='utf-8') as file:
            file.write(msg+"\n")

class log_xmlrpc:
    def recieved(self, req, parameters, alias):
        parameters = ' | '.join(parameters)
        
        write2xmllog("["+ current_date() +"] ["+current_time()+"] [XMLRPC] [<--] [INCOMING] ["+req+"] ["+parameters+"]", alias)

    def sent(self, req, parameters, alias):
        parameters = ' | '.join(parameters)
        
        write2xmllog("["+ current_date() +"] ["+current_time()+"] [XMLRPC] [-->] [OUTGOING] ["+req+"] ["+parameters+"]", alias)

def save(server, c, command, name):
    print "["+ current_date() +"] ["+current_time()+"] | " + server + " | [ " + color[c] + command + color["SYS"] + " ] [ " + color["NAME"] + name + color["SYS"] + " ]" 
    write2comlog("["+ current_date() +"] ["+current_time()+"] | " + server + " | [ " + command + " ] [ " + name + " ]", server)