import action
import random
import os
import filecmp
import sys
import time

#### Actual commands ####

def sheen():
    sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]
    win = random.randint(0, 11)
    bro = (sheenstuff[win])
    action.say(bro, 0)

def login(chatlog):

    #get nick
    name = chatlog
    name = name[27:]
    bort = ' '
    name = name.split(bort, 1)[0]

    #Choose greeting
    hello = ["Welcome ", "Greetings ", "Hai ", "Hai thar ", "Oh hai ", "Hello "]
    greetnum = random.randint(0,5)
    hail = (hello[greetnum])

    #check who's online
    online = action.send("list", 0.1)
    online = online.split("Connected players: ")[-1]
    online = online.split(name, 1)[0] #remove playername from online
    if online == "":
        online = "None. "
    online = online[:-2]

    #greet and return nick
    action.say(hail + name + "! Online: " + online, 0)
    return name

def logout(chatlog):

    #get nick
    name = chatlog
    name = name[27:]
    bort = ' '
    name = name.split(bort, 1)[0]

    #say goodbye & return nick for logg
    action.say("Goodbye " + name + " !", 0)
    return name

def hax(name):
    action.send("gamemode " + name + " 1", 0)

def unhax(name):
    action.send("gamemode " + name + " 0", 0)

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

def help(url):
    action.say("See full commandlist at: "+url, 0)

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
        action.send("xp " + name + " 5000", 0.2)

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
    action.send("tell " + name + " Do _NOT_ leave empty trains on the rail!", 0)

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

def mail(name, chatlog):
        issue = chatlog
        issue = issue[28:]
        issue = issue.split("> !report")[-1]
        issue = issue.replace("\n", "")
        issue = "[ "+name+" ] "+issue
        action.mail(issue)
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
            if "False" in line:
                action.say("[Warning] Turning monsters ON!", 2)
                action.say("[Warning] Monsters will appear in the next night cycle.", 3)
                action.stop_server()
                mc_out.write("spawn-monsters=True\n")
                return "ON"
            if "True" in line:
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

    #remove any old leftovers
    action.send_sys("rm /tmp/"+port+"/minecraft_server.jar", 1)

    #download latest version
    action.send_sys("wget -b --directory-prefix=/tmp/"+port+"/ https://s3.amazonaws.com/MinecraftDownload/launcher/minecraft_server.jar", 5)
    action.say("Done, comparing versions..", 0.5)
    server = path + "minecraft_server.jar"

    #compare with current
    compare = filecmp.cmp('/tmp/'+port+'/minecraft_server.jar', server)

    #if no difference do nothing
    if compare == True:
        action.say("Latest version installed", 1)
        action.say("- Doing nothing.", 1)
        return "No update found"

    #else shutdown and update
    else:
        action.say("Versions does not match!", 3)
        action.say("Im going to try something crazy and update myself!", 4)
        action.say("Dont be mad if shit goes bad :3", 2)
        action.stop_server()
        action.send_sys("rm "+ server, 1)
        action.send_sys("mv /tmp/"+port+"/minecraft_server.jar "+ server, 1)
        action.start_server()
        return "Updated server!"















