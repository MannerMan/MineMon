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
import achievement as achi

mysql = database.insert()
dbtemphax = database.temphax()
dbworld = database.world()

#### Actual commands ####

def sheen():
    sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]
    win = random.randint(0, 11)
    bro = (sheenstuff[win])
    action.say(bro, 0)

def version():
    action.say("Running MineMon version: " + version+" by Oscar Carlberg", 0.2)
    action.say("New in this release:", 0.5)
    changes = database.get_changelog()
    changes = changes[0]['changes']
    changes = changes.split("\n")

    for info in changes:
        action.say("§a"+info, 0.2)

def login(chatlog, version, helpurl):

    #get nick
    name = chatlog
    name = name[27:]
    bort = '['
    name = name.split(bort, 1)[0]

    #Choose greeting
    hello = ["Welcome ", "Greetings ", "Hai ", "Hai thar ", "Oh hai ", "Hello "]
    greetnum = random.randint(0,5)
    hail = (hello[greetnum])

    #check who's online
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
    mysql.login(name, version)

    #check if a new MM version was deployed since last visit.
    vermatch = mysql.version(name, version)
    if vermatch:
        time.sleep(1)
        action.say("§bA §cnew version§b of MineMon was deployed since your last visit!", 2)
        action.say("§bUse §c!version§b for a summary of changes", 0.2)
        mysql.upd_version(name, version)

    #check if user was temphaxed
    temphax_check(name)

    #check for 100 logins achi
    achi.loyal_cust(name)
    
    return name

def logout(chatlog):

    #get nick
    name = chatlog
    name = name[27:]
    bort = ' '
    name = name.split(bort, 1)[0]

    #say goodbye & return nick for logg
    action.say("§cGoodbye " + name + " !", 0)
    mysql.logout(name)
    return name

def hax(name):
    action.send("gamemode 1 " +name, 0)

def unhax(name):
    action.send("gamemode 0 " + name, 0)

def adv(name):
	action.send("gamemode 2 " + name, 0)

def day():
    action.send("time set 10", 0)

def night():
    action.send("time set 14000", 0)

def tp(name, chatlog):
    who = chatlog
    who = who[28:]
    who = who.split("> !tp")[-1]
    who = who.replace("\n", "")
    if who == "":
        action.say("Need a target!", 0)
        return " (No target) "
    else:
        who = who.split(" ")[-1]
        action.send("tp " + name +" "+ who, 0)
        return who

def pull(name, chatlog):
    who = chatlog
    who = who[28:]
    who = who.split("> !tp")[-1]
    who = who.replace("\n", "")
    if who == "":
        action.say("Need a target!", 0)
        return " (No target) "
    else:
        who = who.split(" ")[-1]
        action.send("tp " + who +" "+ name, 0)
        return who

def map(url):
    action.say("See full map at: "+url, 0)

def help(url, chatlog):
    command = chatlog
    command = command[28:]
    command = command.split("> !help")[-1]
    command = command.replace("\n", "")
    if command == "":
        action.say("You can use !help !COMMAND to get detailed information about a specific command", 0.2)
        action.say("See all available commands at: "+url, 0)
    else:
        command = command.split(" ")[-1]
        result = mysql.load_help(command)
        if not result:
            action.say("Command not found", 0)
        else:
            action.say(result["desc"], 0.2)
            syntax = result["syntax"]
            syntax = syntax.split("\n")
            action.say("§aSyntax: §e"+syntax[0], 0.2)
            syntax = iter(syntax)
            next(syntax)
            for s in syntax:
                action.say(s, 0.2)

def roll(name):
    roll = random.randint(1, 100)
    roll = str(roll)
    if roll == "100":
        action.say(name + " rolled "+roll+" and gets rewarded with a diamond!", 0.5)
        action.send("give " + name + " 57 1", 0)
    else:
        action.say(name + " rolled "+roll, 0)
    return roll

def rain():
    action.send("toggledownfall", 0)
    action.say("Loading ...", 1.5)
    action.say("rain/snow was turned on/off", 0)

def xp(name):
    for antal in range(0,4):
        action.send("xp 5000 " + name, 0.2)

def kit(name):
    item = 276
    for antal in range(0,3):
        item = item + 1
        action.send("give " + name +" "+ str(item) + " 1", 0.1)

def leatherset(name):
    item = 297
    for antal in range(0,4):
        item = item + 1
        action.send("give " + name +" "+ str(item) + " 1", 0.1)
    action.send("give " + name + " 268 1", 0)

def diamondset(name):
    item = 309
    for antal in range(0,4):
        item = item + 1
        action.send("give " + name +" "+ str(item) + " 1", 0.1)
    action.send("give " + name + " 276 1", 0)

def bow(name):
    action.send("give " + name + " 261 1", 0)
    for antal in range(0,3):
        action.send("give " + name + " 262 64", 0.1)

def train(name):
    action.send("give " + name + " 328 5", 0.1)
    action.say("Do _NOT_ leave empty wagons on the rail!", 0)

def sleep(name):
    action.send("give " + name + " 355 5 ", 0)

def rail(name):
    for antal in range(0,4):
        action.send("give " + name + " 27 64", 0.1)
    for antal in range(0,2):
        action.send("give " + name + " 28 64", 0.1)

def food(name):
    for antal in range(0,5):
        action.send("give " + name + " 363 64", 0.1)

def item(name, chatlog):
    item = chatlog
    item = item[28:]
    item = item.split("!item ")[-1]
    item = item.replace("\n", "")
    action.send("give " + name +" "+ item +" 64", 0)
    return item

def restart():
    #stop
    action.say("[Warning] Server restarting in 10 seconds!", 5)
    action.say("[Warning] Server restarting in 5 seconds!", 5)
    action.send("save-all", 2)
    action.stop_server()

    #start
    #yeah this is hard though rcon >.<
    action.start_server()

def mail(name, chatlog, crash):
        issue = chatlog
        issue = issue[28:]
        issue = issue.split("> !report")[-1]
        issue = issue.replace("\n", "")
        issue_name = "[ "+name+" ] "+issue
        #action.mail(issue_name)

        #log the report to the database
        if crash:
            mysql.report(name, chatlog)
        else:
            mysql.report(name, issue)

        action.say("Problem was reported to the administrator!", 0)

def monsters(path):
    #real and tempfile
    properties = path + "server.properties"
    mc_out = "/tmp/tempsett.txt"

    #open them
    mc_settings = open(properties, "r")
    mc_out = open(mc_out, "w")

    # loop through the test file line by line
    # and write only the lines back out that do
    # not contain the search string
    search = "spawn-monsters="
    for line in mc_settings:
        if search not in line:
            mc_out.write(line)
        else:
            print "found monsters line!"
            print line
            if "false" in line:
                action.say("[Warning] Turning monsters ON!", 2)
                action.say("[Warning] Monsters will appear in the next night cycle.", 3)
                action.stop_server()
                mc_out.write("spawn-monsters=True\n")
                return "ON"
            if "true" in line:
                action.say("[Warning] Turning monsters OFF!", 2)
                action.say("[Warning] Monsters will stop spawning.", 3)
                action.stop_server()
                mc_out.write("spawn-monsters=False\n")
                return "OFF"
            action.send_sys("rm " + properties, 0)
            action.send_sys("mv /tmp/tempsett.txt " + properties, 0)
            time.sleep(1)
            action.start_server()

    # close the file handles
    mc_settings.close()
    mc_out.close()

def update(path, port):
    action.say("Downloading minecraft_server...", 0)

    #download latest version
    action.send_sys("wget --quiet --directory-prefix=/tmp/"+port+"/ https://s3.amazonaws.com/MinecraftDownload/launcher/minecraft_server.jar", 10)
    action.say("Done, comparing versions..", 0.5)
    server = path + "minecraft_server.jar"

    #compare with current
    compare = filecmp.cmp("/tmp/"+port+"/minecraft_server.jar", server)
    print "comparing " + '/tmp/'+port+'/minecraft_server.jar' + " with " + server

    #if no difference do nothing
    if compare == True:
        action.say("Latest version installed", 1)
        action.say("- Doing nothing.", 1)
        return "No update found"

    #else shutdown and update
    else:
        action.say("Versions does not match!", 3)
        action.say("Im going to try something crazy and update myself!", 4)
        action.say("Dont be mad if shit goes bad :3", 4)
        action.stop_server()
        action.send_sys("rm "+ server, 1)
        action.send_sys("mv /tmp/"+port+"/minecraft_server.jar "+ server, 1)
        action.start_server()
        return "Updated server!"

def temphax(chatlog):

    #extract target
    who = chatlog
    who = who[28:]
    who = who.split("> !temphax")[-1]
    who = who.replace("\n", "")

    #if no target notify
    if who == "":
        action.say("Need a target!", 0)
        return "No target"
    #else hax target and add to templist
    else:
        who = who.split(" ")[-1]
        action.send("gamemode 1 " + who, 0)
        action.say(who+" is now haxed for this session.", 0)
        #templist here
        dbtemphax.add(who)
        return who

def temphax_check(name):
    #ask mysql if name exists in the temphax list
    result = dbtemphax.check(name)
    if not result:
        #user was not temphaxed, do nothing.
        pass
    else:
        #threading this, takes some time
        #making name global, somewhat temp
        global tempname
        tempname = name
        haxThread = unhaxThread(2)
        haxThread.start()

def temphax_unhax(name):
    action.say("[Warning] " + name + " is NOT authed for this session!", 4)
    action.say(name + " - You will be un-haxed!", 3)
    action.say(name + " - You have 10 seconds to get to safety!", 5)
    action.say(name + " - You have 5 seconds to get to safety!", 5)
    status = action.send("gamemode 0 "+ name, 0)
    if "Can't find user" in status:
        action.say(name+" left during de-hax, temphax-list was restored.", 0)
        #just gonna print something here for now, should return and logg instead
        print "TEMPHAX: "+name+" left during unhax, and list was untouched."
    else:
        action.say(name + " was un-haxed", 0.1)
        dbtemphax.remove(name)
        #just gonna print something here for now, should return and logg instead
        print "TEMPHAX: unhaxed "+name

def played(name):
    amount = mysql.played(name)
    action.say(name +" has played "+amount["hours"]+" hours and "+amount["minutes"]+" minutes on this server.", 0)

def world(name, chatlog, mcpath):

    #extract realmname
    realm = chatlog
    realm = realm[28:]
    realm = realm.split("> !world")[-1]
    realm = realm.replace("\n", "")
    realm = realm.replace(" ", "")

    #if no realm send all available
    if realm == "":
        all_worlds = dbworld.get_all_worlds()
        action.say("Available worlds: ", 0.5)
        for w in all_worlds:
            action.say("§a"+w, 0.2)

    else:

        #Check if the choosen realm exists
        if dbworld.check_exist(realm):

            #Check if the choosen realm is active
            if dbworld.check_active(realm):

                #start activation of the new realm
                action.say("Loading module [ §6Armageddon§5 ]", 2)
                action.say("§c!! Experimental feature !!", 2)
                action.say("§fThe world "+realm+" is being activated..", 4)

                #load folder of new world from MYSQL
                world_path = dbworld.get_world(realm)
                change_world(world_path, mcpath)

                #Activate new realm in database
                dbworld.set_active(realm)

                #return the realm for logging purpose
                return realm

            else:
                action.say("The world "+realm+" is already active", 0)

        else:
            action.say("The world "+realm+" does not exist.", 0)


#this is the function that changes worlds
def change_world(new_world, path):

    print " <<<  changing realm to folder: "+new_world+" >>>"

    #real and tempfile
    properties = path + "server.properties"
    mc_out = "/tmp/tempsett.txt"

    #open them
    mc_settings = open(properties, "r")
    mc_out = open(mc_out, "w")

    # loop through the test file line by line
    # and write only the lines back out that do
    # not contain the search string
    search = "level-name="
    for line in mc_settings:
        if search not in line:
            mc_out.write(line)
        else:
            action.say("§e[Warning] §fServer going down for realm-change in 10 seconds", 5)
            action.say("§e[Warning] §fServer going down for realm-change in 5 seconds.", 5)
            action.say("\"Now, I am become Death, the destroyer of worlds.\"", 1)
            action.stop_server()
            mc_out.write("level-name="+new_world+"\n")
            action.send_sys("rm " + properties, 0)
            action.send_sys("mv /tmp/tempsett.txt " + properties, 0)
            time.sleep(1)
            action.start_server()

    # close the file handles
    mc_settings.close()
    mc_out.close()


#this is beeing called every 5 minutes for playtime tracking
def playtime():
    try:
        #check who's online
        online = action.send("list", 0.1)
        online = online.split("There are ")[-1]
        online = online[5:]
        online = online.split("players online:")[-1]
        online = online.split()
        if not online:
            pass
            #print "NO USERS ONLINE"
        else:
            for user in online:
                mysql.playtime(user)

        #Return OK
        return True
    except:
        print "Failed to send RCON data and reconnect. Server down? stopping timetrack."

        #Return false, will result in timetrack-module shutdown.
        return False
            
# this is beeing called when server goes down at the night, for achivement
def late():
    #check who's online
    online = action.send("list", 0.1)
    online = online.split("There are ")[-1]
    online = online[5:]
    online = online.split("players online:")[-1]
    online = online.replace(',','')
    online = online.split()
    if not online:
        pass
        #print "NO USERS ONLINE"
    else:
        for user in online:
            achi.late_gamer(user)

#this thread runs "temphax-unhaxing" so MM can function normal during this process.
class unhaxThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        global tempname
        temphax_unhax(tempname)






