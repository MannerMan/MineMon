import time
import xmlrpclib

proxy = {'mmuser':xmlrpclib.ServerProxy("http://localhost:7090"), 'mm_2011':xmlrpclib.ServerProxy("http://localhost:7091")}

def say(msg, wait, server):
	proxy[server].say("["+server+"] Say:" +msg)
	time.sleep(wait)