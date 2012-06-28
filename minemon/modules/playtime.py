# -*- coding: utf-8 -*-
import socket
import select
import struct
import re
import _mysql

class database():
    def connect(self):
        self.db=_mysql.connect(host="ip_here",user="mmuser",passwd="pw",db="minemon")
        self.db.set_character_set('utf8')
        
    def query(self, que):
        self.db.query(que)
        return self.db.store_result()
database = database()
database.connect()

def db_check(user):
    #cleanup user string
    user = user.replace(',','')
    r=database.query("""SELECT m.user, m.playtime, m.id FROM played_1666 m WHERE m.user = """ + "\'"+user+"\'")
    news_item = r.fetch_row(0, 1)
    if not news_item:
        print "nonexist, inserting new user"
        q=database.query("""INSERT INTO `minemon`.`played_1666` (`user`, `id`, `playtime`) VALUES ('"""+user+"""', NULL, '00:05:00');""")
    else:
        print "user exists, adding 5 min!"
        u=database.query("""UPDATE `minemon`.`played_1666` SET `playtime` = ADDTIME( `playtime`, '00:05:00' ) WHERE `played_1666`.`user` ='"""+user+"""';""") 

def extrct(online):
    troll = online.split()

    #try:
    troll.remove("Connected")
    troll.remove("players:")
    for user in troll:
        db_check(user)
    #except:
    #    print "no users"

class MCRcon:
    def __init__(self, host, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.send_real(3, password)
    
    def close(self):
        self.s.close()
    
    def send(self, command):
        return self.send_real(2, command)
    
    def send_real(self, out_type, out_data):
        #Send the data
        buff = struct.pack('<iii', 
            10+len(out_data),
            0,
            out_type) + out_data + "\x00\x00"
        self.s.send(buff)
        
        #Receive a response
        in_data = ''
        ready = True
        while ready:
            #Receive an item
            tmp_len, tmp_req_id, tmp_type = struct.unpack('<iii', self.s.recv(12))
            tmp_data = self.s.recv(tmp_len-8) #-8 because we've already read the 2nd and 3rd integer fields

            #Error checking
            if tmp_data[-2:] != '\x00\x00':
                raise Exception('protocol failure', 'non-null pad bytes')
            tmp_data = tmp_data[:-2]
            
            #if tmp_type != out_type:
            #    raise Exception('protocol failure', 'type mis-match', tmp_type, out_type)
           
            if tmp_req_id == -1:
                raise Exception('auth failure')
           
            m = re.match('^Error executing: %s \((.*)\)$' % out_data, tmp_data)
            if m:
                raise Exception('command failure', m.group(1))
            
            #Append
            in_data += tmp_data
            

            #Check if more data ready...
            ready = select.select([self.s], [], [], 0)[0]
            
            if out_type == 2:
                extrct(in_data)
        
        return in_data
    