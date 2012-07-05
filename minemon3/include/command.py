import action
import random

#### Random vars ####
sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]

#### Actual commands ####

def sheen():
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
