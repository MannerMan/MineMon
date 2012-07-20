# -*- coding: utf-8 -*-
import socket
import select
import struct
import re
import _mysql

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
            mydb.query("""INSERT INTO `"""+db+"""`.`users` (`name`, `id`, `played`, `online`, `last_online`, `version`) VALUES ('"""+name+"""', NULL, '00:00:00', '1',CURRENT_TIMESTAMP,'"""+version+"');")
            
        #if they do exist, update online and last_online
        else:
            #print "DEBUG: updating user "+name+" to online and last_online"
            mydb.query("""UPDATE `"""+db+"""`.`users` SET `last_online` = CURRENT_TIMESTAMP, `online` = '1' WHERE `users`.`name` ='"""+name+"';")
            
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
            nameid = mydb.query("SELECT u.id FROM users u WHERE u.name ='"+name+"'")
            nameid = nameid.fetch_row(0, 1)
            nameid = nameid[0]["id"]
        
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
        nameid = mydb.query("SELECT u.id FROM users u WHERE u.name ='"+name+"'")
        nameid = nameid.fetch_row(0, 1)
        nameid = nameid[0]["id"]
        
        #get commandid
        commandid = mydb.query("SELECT c.id FROM commands c WHERE c.name ='"+command+"'")
        commandid = commandid.fetch_row(0, 1)
        commandid = commandid[0]["id"]
        
        #DEBUG
        #print "user "+ name +" with id "+nameid+" ran command "+command+" with id "+commandid
        
        #insert into stats_commands
        mydb.query("INSERT INTO stats_command (user_id, command_id) VALUES ('"+nameid+"', '"+commandid+"');")
        
    def raw(self, log):
        mydb.query("INSERT INTO raw_log (log) VALUES ('"+log+"');")
        
    def addopt(self, command, name, option):
        #get nameid
        nameid = mydb.query("SELECT u.id FROM users u WHERE u.name ='"+name+"'")
        nameid = nameid.fetch_row(0, 1)
        nameid = nameid[0]["id"]
        
        #get commandid
        commandid = mydb.query("SELECT c.id FROM commands c WHERE c.name ='"+command+"'")
        commandid = commandid.fetch_row(0, 1)
        commandid = commandid[0]["id"]
        
        #insert into stats_commands
        mydb.query("INSERT INTO stats_command (`user_id`, `command_id`, `option`) VALUES ('"+nameid+"', '"+commandid+"', '"+option+"');")
        
        
    def chat(self, name, msg):
        #get nameid
        nameid = mydb.query("SELECT u.id FROM users u WHERE u.name ='"+name+"'")
        nameid = nameid.fetch_row(0, 1)
        nameid = nameid[0]["id"]
        
        #insert chatmsg
        mydb.query("INSERT INTO chat_history (name_id, msg) VALUES('"+nameid+"','"+msg+"')")
    