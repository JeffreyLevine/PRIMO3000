#!/usr/bin/python

'''
threaded percusive music player
'''

import threading, time, sys
import maestro

class Player():
	def __init__(self, num_servos, up, down, home, delay=0.05, bpm=150):
		self.num_servos = num_servos
		self._strike_delay = delay
		self.up = up
		self.down = down
		self.home = home
		self.bpm = bpm
		self.beat = 60.0 / self.bpm
		self.measure = self.beat * 4.0
		self.sixteenth = self.measure / 16

		self._Pololu = maestro.Controller() #servo controller use default tty
		self._maestrolock = threading.Lock() #lock for around the serial port
		for i in range(self.num_servos): #start at home
			self.go(i, self.home)
	def go(self, servo, pos):
		""" servo goto position, wait, return to middle """
		t = threading.Thread(target=self._task, args=(servo, pos))
		t.start()
	def strike(self, servo):
		""" will drive hammer down then back to middle """
		self.go(servo, self.down)
	def back_strike(self, servo):
		""" will lift hammer up then back to middle """
		self.go(servo, self.up)
	def delay(self, parts):
		""" how many sixteenths to wait """
		time.sleep(self.sixteenth * parts)
	def _task(self, servo, pos):
		"""  used internally to generate servo commands """
		with self._maestrolock: #get Lock
			self._Pololu.setTarget(servo, pos)
			#print(servo, pos) #only used for debugging
		time.sleep(self._strike_delay)
		with self._maestrolock: #get Lock
			self._Pololu.setTarget(servo, self.home) #middle

#*********************EXAMPLE**************************************
if __name__ == '__main__':
	B = Player(2, 8000, 5900, 5400, 0.05, 150)

	t0 = time.time()
	for i in range(30):
		# 1 Measure != 1 Second
		B.strike(1)
		B.delay(2)
		B.strike(1)
		B.delay(2)
		B.strike(0)
		B.delay(2)
		B.strike(1)
		B.delay(1)
		B.strike(1)
		B.delay(2)
		B.strike(1)
		B.delay(1)
		B.strike(1)
		B.delay(2)
		B.strike(0)
		B.delay(2)
		B.strike(0)
		B.delay(2)
	t1 = time.time()

	dt = t1 - t0
	print(dt)
