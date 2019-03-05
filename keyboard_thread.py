#!/usr/bin/python

import sys, termios, tty, os, time, threading
import maestro

"""
Player generates Note threads on keypress
There is safety to prevent pressing high and low strike keys simultaneously
"""

class Note(threading.Thread):
	def __init__(self, controller, servo, pos, mid):
		""" servo as int (0-17), pos as int """
		threading.Thread.__init__(self)
		self._c = controller
		self._s = servo
		self._p = pos
		self._m = mid
	def run(self):
		self._c.pos = (self._s, self._p) #property
		with self._c.maestro_lock: #get Lock
			self._c.goto_pos(self._s, self._p) #strike
		time.sleep(.05)
		with self._c.maestro_lock: #get Lock
			self._c.goto_pos(self._s, self._m)
		self._c.pos = (self._s, self._m) #back to middle

class Player:
	""" accepts commands via keyboard then generates thread to handle servo command """
	def __init__(self, ser_port):
		self._pos_dict = { 'l': 4000, 'm': 6000, 'h': 8000 } #l = low, m = mid, h = high
		self._key_convert = { #{key: [servo, position]}
		 #termios tty
		 '1': [0, 'h'], 'q': [0, 'l'], 
		 '2': [1, 'h'], 'w': [1, 'l'],
		 '3': [2, 'h'], 'e': [2, 'l'],
		 '4': [3, 'h'], 'r': [3, 'l'],
		 '5': [4, 'h'], 't': [4, 'l'],
		 '6': [5, 'h'], 'y': [5, 'l'],
		 '7': [6, 'h'], 'u': [6, 'l'],
		 '8': [7, 'h'], 'i': [7, 'l'],
		 '9': [8, 'h'], 'o': [8, 'l'],
		 '0': [9, 'h'], 'p': [9, 'l'],
		 'a': [10, 'h'], 'z': [10, 'l'],
		 's': [11, 'h'], 'x': [11, 'l'],
		 'd': [12, 'h'], 'c': [12, 'l'],
		 'f': [13, 'h'], 'v': [13, 'l'],
		 'g': [14, 'h'], 'b': [14, 'l'],
		 'h': [15, 'h'], 'n': [15, 'l'],
		 'j': [16, 'h'], 'm': [16, 'l'],
		 'k': [17, 'h'], ',': [17, 'l'] }
		self._Servos = ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'] #current commanded state
		self._Pololu = maestro.Controller(ttyStr = ser_port) #servo controller
		#self._Pololu = maestro.Controller() #servo controller
		self.maestro_lock = threading.Lock() #lock around the serial port
		for i in range(18): #initial position
			self._Pololu.setSpeed(i, 0)
			self._Pololu.setTarget(i, self._pos_dict['m'])

	def getch(self):
		""" get next pressed key """
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno()) #multiple key down is a problem
			ch = sys.stdin.read(1) #this only gives key down
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	#this allows Note to modify Servos positions
	def set_pos(servo, pos):
		self._Servos[servo] = pos
	def get_pos(servo):
		return self._Servos[servo]
	pos = property(fget=get_pos, fset=set_pos)
	
	def goto_pos(self, servo, pos):
		""" maestro.setTarget wrapper """
		self._Pololu.setTarget(servo, pos)

	def pmcl(self):
		""" loop to receive keystrokes """
		while True: #main program loop
			pressed = self.getch() #get
			if pressed == '`': # you cannot print anything or this will fail
				sys.exit()
			servo = self._key_convert[pressed][0]
			pos = self._pos_dict[self._key_convert[pressed][1]]
			if self._Servos[servo] == 'm': #verify servo in 'm'
				task = Note(self, servo, pos, self._pos_dict['m']) #create
				task.start() #run

if __name__ == '__main__':
	music = Player('/dev/ttyACM0') #this is just for testing, default is usually correct
	music.pmcl()
