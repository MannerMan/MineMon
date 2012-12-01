import database
import time
import action


mysql = database.achi()

def late_gamer(name):
    #check if user has achi already:
    if mysql.check_achi(name, 1):
        pass
        #do nothing, user has achi
    else:
        #else, give user the achi
        uname, aname, adesc = mysql.earn_achi(name, 1)
        action.say(uname+" earned the achivement "+aname, 0.1)
        action.say("\""+adesc+"\"", 0.1)
        

    
    
    time.sleep(0.2)

def loyal_cust(name):
    #check if user has achi already:
    if mysql.check_achi(name, 2):
        pass
        #do nothing, user has achi
    else:
        eightable = mysql.loyal(name)
        #run query to see if logins == 100
        if eightable:
            mysql.earn_achi(name, 2)
        else:
            pass

    
    
    