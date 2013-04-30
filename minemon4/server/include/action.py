import time
import xmlrpclib
import logger

log_xmlrpc = logger.log_xmlrpc()

mmclient = {}

### startup load
def load(mmclients):
	global mmclient
  	for clientid in mmclients:
  		mmclient[clientid]=xmlrpclib.ServerProxy("http://"+mmclients[clientid]['ip']+":"+mmclients[clientid]['port'])

def say(msg, wait, clientid):
	mmclient[clientid].say(msg)

	#Log the request
	log_xmlrpc.sent("say", [clientid, msg], clientid)

	time.sleep(wait)