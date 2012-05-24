# import needed modules:

from socket import *        # get sockets, for well, sockets
import string                # string functions
import time                    # for sleep(1) function
import os

# define global variables

HOST = '0.0.0.0'                # Symbolic name meaning the local host
PORT = 4008                # Arbitrary non-privileged server
endl = "\r\n"            # standard terminal line ending

userlist = []            # list of connected users
done = 0                # set to 1 to shut this down

kAskName = 0            # some constants used to flag
kWaitName = 1            #    the state of each user
kOK = 2


# class to store info about connected users

class User:
    def __init__(self):
        self.name = ""
        self.addr = ""
        self.conn = None
        self.step = kAskName

    def Idle(self):
        if self.step == kAskName: self.AskName()

    def AskName(self):
        self.conn.send("Name? ")
        self.step = kWaitName

    def HandleMsg(self, msg):
        print "Handling chat: ",msg
        global userlist

        # if waiting for name, record it
        if self.step == kWaitName:
            # try to trap garb initiall sent by some telnets:
            if len(msg) < 2 or msg=="#": return
            print "Setting name to: ",msg
            self.name = msg
            self.step = kOK
            #self.conn.send("Hello, "+self.name)
            broadcast(self.name+" has connected.")
            return

        # check for commands
        if msg == "quit":
            broadcast(self.name+" has quit.\n")
            self.conn.close()
            userlist.remove(self)
            return

        # otherwise, broadcast msg
        print "sending chat"
        os.system("screen -S mc_hax -p 0 -X stuff \"`printf \"say "+ self.name +": " + msg + " \r\"`\";")
        print "sent mc msg"
        broadcast( self.name+": "+msg )
        print "chat sent"

# routine to check for incoming connections

def pollNewConn():
    try:
        conn, addr = s.accept()
    except:
        return None
    print "Connection from", addr
    conn.setblocking(0)
    user = User();
    user.conn = conn
    user.addr = addr
    return user


# routine to broadcast a message to all connected users

def broadcast(msg):
    for u in userlist:
        u.conn.send(msg)


# MAIN PROGRAM


# set up the server

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.setblocking(0)
s.listen(4)
print "Waiting for connection(s)..."

# loop until done, handling connections and incoming messages

def start():
    global done
    while not done:
        time.sleep(0.1)        # sleep to reduce processor usage
        u = pollNewConn()    # check for incoming connections
        if u:
            userlist.append(u)
            print len(userlist),"connection(s)"

        for u in userlist:    # check all connected users
            u.Idle()
            try:
                data = u.conn.recv(1024)
                #data = filter(lambda x: x>=' ' and x<='z', data)
                #data = string.strip(data)
                if data:
                    print "From",u.name,': ['+data+']'
                    u.HandleMsg(data)
                    if data == "shutdown": done=1
            except:
                pass

for u in userlist:
    u.conn.close()