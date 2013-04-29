import time
import xmlrpclib

mmclient = {}

### startup load
def load(mmclients):
	global mmclient
  	for clientid in mmclients:
  		mmclient[clientid]=xmlrpclib.ServerProxy("http://"+mmclients[clientid]['ip']+":"+mmclients[clientid]['port'])

def say(msg, wait, clientid):
	mmclient[clientid].say("Say:" +msg)
	time.sleep(wait)