# -*- coding: utf-8 -*-

import action
import random
import os
import filecmp
import sys
import time
import database
import thread
import threading
#import achievement as achi

mysql = database.db_queries()

def login(player, v, server):

    #Choose greeting
    hello = ["Welcome ", "Greetings ", "Hai ", "Hai thar ", "Oh hai ", "Hello "]
    greetnum = random.randint(0,5)
    hail = (hello[greetnum])

    #temp
    time.sleep(5)
    action.say(hail+player, 0, server)
    mysql.login(player, v, server)

    #skip all this right now
    """
    #check who's online
    online = action.send("list", 0.1)
    online = online.split("There are ")[-1]
    online = online[5:]
    online = online.split("players online:")[-1]
    online = online.split(name, 1)[0] #remove playername from online
    if online == "":
        online = "None. "
    online = online[:-2]

    #greet and return nick
    action.say("§a"+hail + name + "! Online: " + online, 0)
    mysql.login(name, v)

    #check if a new MM version was deployed since last visit.
    vermatch = mysql.version(name, v)
    if vermatch:
        time.sleep(1)
        action.say("§bA §cnew version§b of MineMon was deployed since your last visit!", 2)
        action.say("§bUse §c!version§b for a summary of changes", 0.2)
        mysql.upd_version(name, v)

    #check if user was temphaxed
    temphax_check(name)

    #check for 100 logins achi
    achi.loyal_cust(name)
    """

def logout(player, server):
    time.sleep(10)
    #say goodbye & return nick for logg
    action.say("§cGoodbye " + player + " !", 0, server)
    mysql.logout(player, server)
    return player
