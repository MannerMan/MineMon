# -*- coding: utf-8 -*-
import time
import threading
from threading import Thread
import command as command

class playtime(Thread):

 def __init__ (self):
    Thread.__init__(self)
    self.cont=True

    self.max_time=300
    self.time=0

 def incrementTime(self):
    self.time+=1
    self.time=self.time%self.max_time

 def myAction(self):
    status = command.playtime()
    if not status:
      self.stop()

 def run(self):
    while self.cont:

       if(self.time==0):
          self.myAction()

       self.incrementTime()

       time.sleep(1)

 def stop(self):
    try:
        self.cont=False
    except:
        print "UNABLE TO STOP CHAOS!!"