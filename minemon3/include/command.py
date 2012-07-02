import action
import random

#### Random vars ####
sheenstuff = ["Winning", "Bi-winning", "Win Win everywhere", "Your face will melt off!", "Whats not to love?", "Epic Winning!", "Win here, win there, win everywhere!", "Absolute victory!", "That's how I roll", "No pants? - Winning!", "Duuh, WINNING! WINNING!", "The only thing Im addicted to right now is winning."]

#### Actual commands ####

def sheen():
    win = random.randint(0, 11)
    bro = (sheenstuff[win])
    action.say(bro, 0)

