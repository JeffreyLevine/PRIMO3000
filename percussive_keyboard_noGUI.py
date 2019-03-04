#!/usr/bin/python

import sys, termios, tty, os, time
import maestro

class Player:
	""" accepts commands via keyboard then can indicate holding key by color white to black """
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
		self._Pololu = maestro.Controller(ttyStr = ser_port) #servo controller
		#self._Pololu = maestro.Controller() #servo controller
		for i in range(18): #initial position
			self._Pololu.setSpeed(i, 0)
			self._Pololu.setTarget(i, self._pos_dict['m'])

	def getch(): #!!!! need key down and up :( !!!!
		""" get next pressed key """
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno()) #multiple key down is a problem
			ch = sys.stdin.read(1) #this only gives key down :(
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	def pmcl(self):
		""" loop to receive keystrokes """
		while True: #main program loop
			#get
			pressed = getch()
			#move
			self._Pololu.setTarget(self._key_convert[pressed][0], self._pos_dict[self._key_convert[pressed][1]])
			time.sleep(.05)
			self._Pololu.setTarget(i, self._pos_dict['m'])

if __name__ == '__main__':
	music = Player('/dev/ttyACM0')
	music.pmcl()
