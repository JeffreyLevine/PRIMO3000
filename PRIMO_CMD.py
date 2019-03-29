#!/usr/bin/python

'''
right now position is an integer, will be replacing this with a dictonary
'''

import threading, time, sys
import maestro

delays = {
 'short':   .05,
 'mid':     .1,
 'long':    .25,
 'longest': .5
}

class Player():
	def __init__(self):
		self._strike_delay = 0.1
		self._Pololu = maestro.Controller() #servo controller use default tty
		self._maestrolock = threading.Lock() #lock for around the serial port
	def go(self, servo, pos):
		""" servo goto position, wait, return to middle """
		t = threading.Thread(target=task, args=(servo, pos))
		t.start()
	@classmethod
	def wait(duration): #str containing delay
		time.sleep(delays[duration])
	def _task(self, servo, pos):
		with self._maestrolock: #get Lock
			self._Pololu.setTarget(servo, pos)
			print(servo, pos)
		time.sleep(self._strike_delay)
		with self._maestrolock: #get Lock
			self._Pololu.setTarget(servo, 6000) #middle

#*******************************************************************
#demo using 3 servos

PRIMO = Player()

PRIMO.go(0, 6000)
PRIMO.go(1, 6000)
PRIMO.go(2, 6000)
#everyone to middle
PRIMO.wait('longest')
PRIMO.go(0, 4000)
PRIMO.wait('short')
PRIMO.go(1, 4000)
PRIMO.wait('short')
PRIMO.go(2, 4000)
PRIMO.wait('short')
PRIMO.go(0, 4000)
PRIMO.wait('longest')
PRIMO.go(2, 4000)
PRIMO.wait('short')
PRIMO.go(1, 4000)
