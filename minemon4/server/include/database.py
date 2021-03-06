# -*- coding: utf-8 -*-
import socket
import select
import struct
import re
import _mysql
dbinfo = ''

### startup load
def load(mmclients):
    global dbinfo
    global myconn
    dbinfo = mmclients
    myconn = {}
    for n in dbinfo:
        db=_mysql.connect('localhost', 'root', 'examplepw')
        myconn[n] = db 
    #print myconn['mmtest']

### Database connection ###
def settings(myhost, myuser, mypass):
    global dbhost
    global user
    global passwd
    global db
    dbhost = myhost
    user = myuser
    passwd = mypass
    reconnect()
    
    
def reconnect():
    global data
    data.connect()
    global mydb
    mydb = data

class database():
    def connect(self):

        self.db=_mysql.connect(dbhost,user,passwd)
        self.db.set_character_set('utf8')
        print "connected to mysql"
        
    def query(self, server, que):
        print "DEBUG: Executing query: "+que+" in DB: "+server
        myconn[server].query(que)
        return myconn[server].store_result()

    def query_old(self, que):
        #try:
        self.db.query(que)
        return self.db.store_result()
        """
        except:
            print "Unable to reach MYSQL, reconnecting"
            reconnect()
            
            print "trying query again"
            self.db.query(que)
            return self.db.store_result()
        """

data = database()

### Some basic database functions
def get_name_id(name, clientid):
    nameid = mydb.query(clientid, "SELECT u.id FROM "+dbinfo[clientid]['schema']+".users u WHERE u.name ='"+name+"'")
    nameid = nameid.fetch_row(0, 1)
    try:
        nameid = nameid[0]["id"]
        return nameid
    except:
        #if nameid cannot be extracted, return "0" as nameid
        print "ERROR: Could not get nameid for name: " + str(name) + " - Returning nameid 0"
        nameid = '0'
        return nameid

### Queries ###
class db_queries():
    def login(self, name, version, clientid):
        
        #check if user exists
        mysqldata=mydb.query(clientid, "SELECT m.name, m.played, m.id FROM "+dbinfo[clientid]['schema']+".users m WHERE m.name = '"+name+"'")
        user = mysqldata.fetch_row(0, 1)
        
        #if not, add user
        if not user:
            print "Adding new user to database"
            mydb.query(clientid, "INSERT INTO "+dbinfo[clientid]['schema']+".users (name, id, played, online, last_online, version, logins) VALUES ('"+name+"', NULL, '00:00:00', '1',CURRENT_TIMESTAMP,'"+version+"', '1');")
            
        #if they do exist, update online and last_online
        else:
            #print "DEBUG: updating user "+name+" to online and last_online"
            mydb.query(clientid, "UPDATE "+dbinfo[clientid]['schema']+".users u SET last_online = CURRENT_TIMESTAMP, online = '1', logins = logins + '1' WHERE u.name ='"+name+"';")

    def logout(self, name, clientid):
        #print "DEBUG: Setting user "+name+" as offline"
        mydb.query(clientid, "UPDATE "+dbinfo[clientid]['schema']+".users u SET online = '0' WHERE u.name ='"+name+"';")

