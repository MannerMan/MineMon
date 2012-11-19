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
    
def check_enabled_command(command):
    #this function checks if the command being run by the user is enabled for the active world

    #Get command id
    command_id = get_command_id(command)

    #Get current world
    worldb = world()
    active_world = worldb.get_current()
    active_world_id = worldb.get_world_id(active_world)

    enabled = mydb.query("SELECT e.enabled FROM enabled_commands e WHERE e.world_id ='"+active_world_id+"' AND e.command_id ='"+command_id+"'" )
    enabled = enabled.fetch_row(0, 1)
    enabled = enabled[0]["enabled"]
    if enabled == "1":
        #print "command: "+command+" is enabled for world "+active_world
        return True
    else:
        #print "command: "+command+" is NOT enabled for world "+active_world
        return False

def check_command_op(command):
    #This function checks if a specific command needs operator status to be ran.

    #Get command id
    command_id = get_command_id(command)

    #Get current world
    worldb = world()
    active_world = worldb.get_current()
    active_world_id = worldb.get_world_id(active_world)

    op = mydb.query("SELECT e.op FROM enabled_commands e WHERE e.world_id ='"+active_world_id+"' AND e.command_id ='"+command_id+"'" )
    op = op.fetch_row(0, 1)
    op = op[0]["op"]
    if op == "0":
        return False
    else:
        return True

def get_changelog():
    changes = mydb.query("SELECT v.changes FROM version v WHERE v.current = '1'")
    changes = changes.fetch_row(0, 1)
    return changes


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
    
    def load_help(self, command):
        help = mydb.query("SELECT c.desc, c.syntax FROM commands c WHERE c.name=\""+command+"\";")
        help = help.fetch_row(0, 1)

        if not help:
            return False
        else:
            return help[0]

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
        
class world():
    def __init__(self):
        #nothing
        pass

    def check_exist(self, realm):
        world_exist = mydb.query("SELECT * from worlds w where w.world_name ='"+realm+"';")
        world_exist = world_exist.fetch_row(0, 1)

        if world_exist:
            return True
        else:
            return False

    def check_active(self, realm):
        world_active = mydb.query("SELECT w.active from worlds w where w.world_name ='"+realm+"';")
        world_active = world_active.fetch_row(0, 1)
        world_active = world_active[0]["active"]

        if world_active == '0':
            return True
        else:
            return False

    def get_world(self, realm):
        world_path = mydb.query("SELECT w.path from worlds w where w.world_name ='"+realm+"';")
        world_path = world_path.fetch_row(0, 1)
        world_path = world_path[0]["path"]
        return world_path

    def get_current(self):
        world_current = mydb.query("SELECT w.world_name from worlds w where w.active ='1';")
        world_current = world_current.fetch_row(0, 1)
        world_current = world_current[0]["world_name"]
        return world_current

    def get_world_id(self, realm):
        world_id = mydb.query("SELECT w.id from worlds w where w.world_name ='"+realm+"';")
        world_id = world_id.fetch_row(0, 1)
        world_id = world_id[0]["id"]
        return world_id

    def set_active(self, realm):
        #inactivate current
        mydb.query("UPDATE worlds w SET w.active = 0 WHERE w.active = 1")

        #activate new
        mydb.query("UPDATE worlds w SET w.active = 1, w.used = w.used + 1, w.timestamp = CURRENT_TIMESTAMP WHERE w.world_name ='"+realm+"'")

    def get_all_worlds(self):
        all_worlds = mydb.query("SELECT w.world_name from worlds w")
        all_worlds = all_worlds.fetch_row(0, 1)
        alles = []
        for world in all_worlds:
             alles.append(world["world_name"])

        return alles

class gateway():

    def __init__(self):
        pass

    def add(self, playername, gwname, mode, x, y, z):
        #get current world
        worldb = world()
        active_world = worldb.get_current()
        world_id = worldb.get_world_id(active_world)

        #get user
        user_id = get_name_id(playername)

        mydb.query("INSERT INTO gateways (name, user_id, world_id, type, x, y, z) VALUES ('"+gwname+"', "+user_id+", "+world_id+", '"+mode+"', '"+x+"', '"+y+"', '"+z+"')")

        print "added: "+playername, gwname, mode, x, y, z

    def list_priv(self, playername):
        #get user
        user_id = get_name_id(playername)

        prigws = mydb.query("SELECT g.name FROM gateways g WHERE g.user_id = '"+user_id+"' AND g.type = 'private'")
        prigws = prigws.fetch_row(0, 1)
        return prigws

    def list_pub(self):
        pubgws = mydb.query("SELECT g.name FROM gateways g WHERE g.type = 'public'")
        pubgws = pubgws.fetch_row(0, 1)
        return pubgws

    def exist(self, playername, gwname, mode):
        #get user
        user_id = get_name_id(playername)

        if mode == "private":
            tp_point = mydb.query("SELECT g.id FROM gateways g WHERE g.type = 'private' AND g.user_id = '"+user_id+"' AND g.name = '"+gwname+"'")
            tp_point = tp_point.fetch_row(0, 1)
            return tp_point
        else:
            tp_point = mydb.query("SELECT g.id FROM gateways g WHERE g.type = 'public' AND g.name = '"+gwname+"'")
            tp_point = tp_point.fetch_row(0, 1)
            return tp_point

    def owner(self, playername, gwname):
        #get user
        user_id = get_name_id(playername)

        own = mydb.query("SELECT g.id FROM gateways g WHERE g.type = 'public' AND g.user_id ='"+user_id+"' AND g.name = '"+gwname+"'")
        own = own.fetch_row(0, 1)
        return own

    def get_coords(self, playername, gwname, mode):
        #get user
        user_id = get_name_id(playername)

        if mode == "private":
            coords = mydb.query("SELECT g.x, g.y, g.z FROM gateways g WHERE g.type = '"+mode+"' AND g.user_id = '"+user_id+"' AND g.name = '"+gwname+"'")
            coords = coords.fetch_row(0, 1)
            return coords[0]
        else:
            coords = mydb.query("SELECT g.x, g.y, g.z FROM gateways g WHERE g.type = '"+mode+"' AND g.name = '"+gwname+"'")
            coords = coords.fetch_row(0, 1)
            return coords[0]

    def update_used(self, playername, gwname, mode):
        #get user
        user_id = get_name_id(playername)

        mydb.query("UPDATE gateways g SET g.used = g.used + 1 WHERE g.type = '"+mode+"' AND g.user_id = '"+user_id+"' AND g.name = '"+gwname+"'")

    def delete(self, playername, gwname, mode):
        #get user
        user_id = get_name_id(playername)

        mydb.query("DELETE FROM gateways WHERE user_id = '"+user_id+"' AND name = '"+gwname+"' AND type = '"+mode+"'")
            
    