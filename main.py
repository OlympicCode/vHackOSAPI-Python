#!/usr/bin/env python2.7
from network import Network
from utils import Utils
import sys
import os
try:
   import fcntl
except:
	pass

class run():
    def __init__(self, ut):
        network = Network(ut)

if __name__ == '__main__':
    ut = Utils()
    try:
       fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
       fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
    except:
    	pass
    while 1:
       main = run(ut)
