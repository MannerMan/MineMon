# -*- coding: utf-8 -*-
import socket
import select
import struct
import re
import time
import smtplib
from email.mime.text import MIMEText
import os
import sys


def load(mail, pw, sendto, screen):
    print screen
    global scrn
    global gmail
    global gpw
    global rcvr

    scrn = screen
    gmail = mail
    gpw = pw
    rcvr = sendto

def mail(mailmsg):
    msg = MIMEText(mailmsg)
    msg['Subject'] = 'MineMon problemreport'
    msg['From'] = "MineMon3"
    msg['Reply-to'] = "donotreply"
    msg['To'] = "Admin"

    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    #fix config-settings here.
    server.login(gmail,gpw)
    server.sendmail(gmail,rcvr,msg.as_string())
    server.close()

def connect(host, port, pwd):
    global r
    global rhost
    global rport
    global rpwd

    rhost = host
    rport = port
    rpwd = pwd
    r = MCRcon(host, int(port), pwd)

def say(msg, wait):
    r.send("say "+msg)
    time.sleep(int(wait))

def send(command, wait):
    status = r.send(command)
    time.sleep(wait)
    return status

def load_op(mcpath):
    opath = mcpath + 'ops.txt'
    opfile = open(opath, 'r')
    ops = opfile.read()
    return ops
    #print ops

def send_sys(command, time):
    if time == 0:
        execute = command
    else:
        execute = command + " ; sleep " + str(time)
    try:
        os.system(execute)
    except:
        print "Exection of "+execute+" failed."

def send_task(task, time):
    os.system("screen -S "+ scrn +" -p 0 -X stuff \"`printf \""+ task +" \r\"`\"; sleep "+ str(time))

def stop_server():
    send_task("stop", 5)

def start_server():
    time.sleep(2)
    send_task("java -Xmx700M -Xms700M -jar minecraft_server.jar nogui", 0)

class MCRcon:
    def __init__(self, host, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.send_real(3, password)

    def close(self):
        self.s.close()

    def send(self, command):
	try:
            return self.send_real(2, command)
	except:
	    connect(rhost, rport, rpwd)
	    time.sleep(1)
	    return self.send_real(2, command)

    def send_real(self, out_type, out_data):
        #Send the data
        buff = struct.pack('<iii',
            10+len(out_data),
            0,
            out_type) + out_data + "\x00\x00"
        try:
            self.s.send(buff)
        except:
            print "ERROR: COULD NOT SEND RCON DATA!"
    	    #SKRIV RECONNECT here
            #worx need doin

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
                pass
                #extrct(in_data)

        return in_data