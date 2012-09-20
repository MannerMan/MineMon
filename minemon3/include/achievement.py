import database
import time

mysql = database.achi()

def late_gamer(name):
    #check if user has achi already:
    if mysql.check_achi(name, 1):
        pass
        #do nothing, user has achi
    else:
        mysql.earn_achi(name, 1)
        #else, give user the achi

    
    
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

    
    
    