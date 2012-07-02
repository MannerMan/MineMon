import action
import random

#### Random vars ####
sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]

#### Actual commands ####

def sheen():
    win = random.randint(0, 11)
    bro = (sheenstuff[win])
    action.say(bro, 0)

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