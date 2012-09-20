# -*- coding: utf-8 -*-
import socket
import select
import struct
import re
import _mysql

def get_name_id(name):
    nameid = mydb.query("SELECT u.id FROM users u WHERE u.name ='"+name+"'")
    nameid = nameid.fetch_row(0, 1)
    nameid = nameid[0]["id"]
    return nameid

def get_command_id(command):
    commandid = mydb.query("SELECT c.id FROM commands c WHERE c.name ='"+command+"'")
    commandid = commandid.fetch_row(0, 1)
    commandid = commandid[0]["id"]
    return commandid
    

def settings(myhost, myuser, mypass, mydb):
    global dbhost
    global user
    global passwd
    global db
    dbhost = myhost
    user = myuser
    passwd = mypass
    db = mydb
    reconnect()
    
    
def reconnect():
    global data
    data.connect()
    global mydb
    mydb = data

class database():
    def connect(self):
        self.db=_mysql.connect(dbhost,user,passwd,db)
        self.db.set_character_set('utf8')
        print "connected to mysql"
        
    def query(self, que):
        try:
            self.db.query(que)
            return self.db.store_result()
        except:
            print "Unable to reach MYSQL, reconnecting"
            reconnect()
            
            print "trying query again"
            self.db.query(que)
            return self.db.store_result()

data = database()
    
class insert():
    
    def upd_version(self, name, version):
        mydb.query("""UPDATE `"""+db+"""`.`users` SET `version` = '"""+version+"""' WHERE `users`.`name` ='"""+name+"';")
    
    def version(self, name, version):
        versioncheck = mydb.query("""SELECT u.version FROM """+db+""".users u WHERE u.name = """ + "\'"+name+"\'")
        versioncheck = versioncheck.fetch_row(0, 1)
        versioncheck = versioncheck[0]["version"]
        if versioncheck == version:
            return False
        else:
            return True

    def login(self, name, version):
        
        #check if user exists
        mysqldata=mydb.query("""SELECT m.name, m.played, m.id FROM users m WHERE m.name = """ + "\'"+name+"\'")
        user = mysqldata.fetch_row(0, 1)
        
        #if not, add user
        if not user:
            print "Adding new user to database"
            mydb.query("""INSERT INTO `"""+db+"""`.`users` (`name`, `id`, `played`, `online`, `last_online`, `version`, `logins`) VALUES ('"""+name+"""', NULL, '00:00:00', '1',CURRENT_TIMESTAMP,'"""+version+"', '1');")
            
        #if they do exist, update online and last_online
        else:
            #print "DEBUG: updating user "+name+" to online and last_online"
            mydb.query("""UPDATE `"""+db+"""`.`users` SET `last_online` = CURRENT_TIMESTAMP, `online` = '1', `logins` = `logins` + '1' WHERE `users`.`name` ='"""+name+"';")
            
    def logout(self, name):
        #print "DEBUG: Setting user "+name+" as offline"
        mydb.query("""UPDATE `"""+db+"""`.`users` SET `online` = '0' WHERE `users`.`name` ='"""+name+"';")
        
    def playtime(self, name):
        #cleanup user string
        name = name.replace(',','')
        try:
            mydb.query("""UPDATE `"""+db+"""`.`users` SET `played` = ADDTIME( `played`, '00:05:00' ) WHERE `users`.`name` ='"""+name+"';")
        except:
            print "impossiblu to add playtime to user "+name
            
    def played(self, name):
        minutes = mydb.query("SELECT MINUTE((SELECT played from users where name = '"+name+"'))")
        minutes = minutes.fetch_row(0, 1)
        minutes = minutes[0]["MINUTE((SELECT played from users where name = '"+name+"'))"]

        hours = mydb.query("SELECT HOUR((SELECT played from users where name = '"+name+"'))")
        hours = hours.fetch_row(0, 1)
        hours = hours[0]["HOUR((SELECT played from users where name = '"+name+"'))"]
        return {'minutes':minutes, 'hours':hours}
    
    def report(self, name, msg):
        #if name = system just set id = 1 for now
        if name == "SYSTEM":
            nameid = "1"
        else:
            #get nameid
            nameid = get_name_id(name)
        
        mydb.query("INSERT INTO problemreport (user_id, report) VALUES ('"+nameid+"', '"+msg+"')")
            
class temphax():
    
    def add(self, name):
        mydb.query("""INSERT INTO `"""+db+"""`.`temphax` (`id`, `name`) VALUES (NULL, '"""+name+"');")
        
    def remove(self, name):
        mydb.query("DELETE FROM "+db+".temphax WHERE name ='"+name+"'")
    
    def check(self, name):
        namecheck = mydb.query("""SELECT t.id, t.name FROM """+db+""".temphax t WHERE t.name = """ + "\'"+name+"\'")
        result = namecheck.fetch_row(0, 1)
        return result
    
class log():
    def add(self, command, name):
        #get nameid
        nameid = get_name_id(name)
        
        #get commandid
        commandid = get_command_id(command)
        
        #DEBUG
        #print "user "+ name +" with id "+nameid+" ran command "+command+" with id "+commandid
        
        #insert into stats_commands
        mydb.query("INSERT INTO stats_command (user_id, command_id) VALUES ('"+nameid+"', '"+commandid+"');")
        
    def raw(self, log):
        mydb.query("INSERT INTO raw_log (log) VALUES ('"+log+"');")
        
    def addopt(self, command, name, option):
        #get nameid
        nameid = get_name_id(name)
        
        #get commandid
        commandid = get_command_id(command)
        
        #insert into stats_commands
        mydb.query("INSERT INTO stats_command (`user_id`, `command_id`, `option`) VALUES ('"+nameid+"', '"+commandid+"', '"+option+"');")
        
        
    def chat(self, name, msg):
        #get nameid
        nameid = get_name_id(name)
        
        #clean chat-msg from ' etc
        msg = _mysql.escape_string(msg)
        
        #insert chatmsg
        mydb.query("INSERT INTO chat_history (name_id, msg) VALUES('"+nameid+"','"+msg+"')")
        
class achi():
    def __init__(self):
        #nothing
        pass
    
    def check_achi(self, name, achi):
        nameid = get_name_id(name)
        
        gotachi = mydb.query("SELECT e.user_id, e.achi_id FROM earned_achi e WHERE e.user_id = '"+nameid+"' AND e.achi_id = '"+str(achi)+"';")
        gotachi = gotachi.fetch_row(0, 1)
        
        if gotachi:
            return True
        else:
            return False
        
    def earn_achi(self, name, achi):
        #insert achi to earned_achi
        nameid = get_name_id(name)
        mydb.query("INSERT INTO earned_achi (user_id, achi_id) VALUES('"+nameid+"','"+str(achi)+"');")
        
        #get name of achi
        achiname = mydb.query("SELECT a.name from Achivements a where a.id ='"+str(achi)+"';")
        achiname = achiname.fetch_row(0, 1)
        achiname = achiname[0]["name"]
        
        #get achidescr
        achidesc = mydb.query("SELECT a.desc from Achivements a where a.id ='"+str(achi)+"';")
        achidesc = achidesc.fetch_row(0, 1)
        achidesc = achidesc[0]["desc"]
        
        #hm..
        print "user "+name+" earnead achi: "+achiname
        print achidesc
        
        
    def loyal(self, name):
        nameid = get_name_id(name)
            
        canhas = mydb.query("SELECT u.logins FROM users u WHERE u.id ='"+nameid+"';")
        canhas = canhas.fetch_row(0, 1)
        canhas = canhas[0]["logins"]
        if canhas == "100":
            return True
        else:
            return False
        
        
            
    