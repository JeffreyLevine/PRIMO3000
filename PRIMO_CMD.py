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

DOWN_POSITION = 5400
HOME_POSITION = DOWN_POSITION + 500

class Player():
	def __init__(self):
		self._strike_delay = 0.05
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

#********************************************************************
#better way to treat delays like music timing
#need to incorporate this into the Player class
t0 = time.time()
go(0, HOME_POSITION)
go(1, HOME_POSITION)
time.sleep(.1)

#everyone to middle
for i in range(30):
	bpm = 150.0
	MINUTE = 60.0
	beat = MINUTE / bpm
	measure = beat * 4.0
	sixteenth = measure / 16
	
	strike = lambda servo: go(servo, DOWN_POSITION)
	
	# Measure 1!
	strike(1)
	time.sleep(2 * sixteenth)
	strike(1)
	time.sleep(2 * sixteenth)
	strike(0)
	time.sleep(2 * sixteenth)
	strike(1)
	time.sleep(1 * sixteenth)
	strike(1)
	time.sleep(2 * sixteenth)
	strike(1)
	time.sleep(1 * sixteenth)
	strike(1)
	time.sleep(2 * sixteenth)
	strike(0)
	time.sleep(2 * sixteenth)
	strike(0)
	time.sleep(2 * sixteenth)
