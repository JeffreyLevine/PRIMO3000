#!/usr/bin/python

import sys, time, threading
import maestro
import pygame
from pygame.locals import *

strike_delay = 0.05 #time for striker to go from middle to extreme

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
			print(self._s, self._p)
		time.sleep(strike_delay)
		with self._c.maestro_lock: #get Lock
			self._c.goto_pos(self._s, self._m)
			self._c._Servos[self._s] = 'm' #back to middle

class Player:
	""" accepts commands via keyboard then can indicate holding key by color white to black """
	def __init__(self, ser_port):
		self._pos_dict = { 'l': 4500, 'm': 6750, 'h': 9000 } #l = low, m = mid, h = high
		self._key_convert = { #{key: [servo, position, opposite, row, col]}
		 K_1: [0, 'h', K_q, 0, 0], K_q: [0, 'l', K_1, 1, 0], 
		 K_2: [1, 'h', K_w, 0, 1], K_w: [1, 'l', K_2, 1, 1],
		 K_3: [2, 'h', K_e, 0, 2], K_e: [2, 'l', K_3, 1, 2],
		 K_4: [3, 'h', K_r, 0, 3], K_r: [3, 'l', K_4, 1, 3],
		 K_5: [4, 'h', K_t, 0, 4], K_t: [4, 'l', K_5, 1, 4],
		 K_6: [5, 'h', K_y, 0, 5], K_y: [5, 'l', K_6, 1, 5],
		 K_7: [6, 'h', K_u, 0, 6], K_u: [6, 'l', K_7, 1, 6],
		 K_8: [7, 'h', K_i, 0, 7], K_i: [7, 'l', K_8, 1, 7],
		 K_9: [8, 'h', K_o, 0, 8], K_o: [8, 'l', K_9, 1, 8],
		 K_0: [9, 'h', K_p, 0, 9], K_p: [9, 'l', K_0, 1, 9],
		 K_a: [10, 'h', K_z, 2, 0], K_z: [10, 'l', K_a, 3, 0],
		 K_s: [11, 'h', K_x, 2, 1], K_x: [11, 'l', K_s, 3, 1],
		 K_d: [12, 'h', K_c, 2, 2], K_c: [12, 'l', K_d, 3, 2],
		 K_f: [13, 'h', K_v, 2, 3], K_v: [13, 'l', K_f, 3, 3],
		 K_g: [14, 'h', K_b, 2, 4], K_b: [14, 'l', K_g, 3, 4],
		 K_h: [15, 'h', K_n, 2, 5], K_n: [15, 'l', K_h, 3, 5],
		 K_j: [16, 'h', K_m, 2, 6], K_m: [16, 'l', K_j, 3, 6],
		 K_k: [17, 'h', K_COMMA, 2, 7], K_COMMA: [17, 'l', K_k, 3, 7] }
		self._Servos = ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'] #current commanded state
		self._Pololu = maestro.Controller() #servo controller use default tty
		for i in range(18): #initial position
			self._Pololu.setSpeed(i, 0)
			self._Pololu.setTarget(i, self._pos_dict['m'])
		pygame.init() #initialize pygame
		self.screen = pygame.display.set_mode([300, 1], DOUBLEBUF | HWACCEL) #initialize screen
		self.screen.set_alpha(None)
		self.clock = pygame.time.Clock()
		self.clock.tick(60)
		pygame.display.set_caption("Keyboard Servo Player") #title
		self.maestro_lock = threading.Lock() #lock around the serial port

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
		""" loop to receive keystrokes then send command and update screen """
		while True: #main program loop
			for event in pygame.event.get(): #event loop
				if event.type == QUIT:
					print (self._Servos)
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN: #press
					if self._key_convert.has_key(event.key):
						s, p = self._key_convert[event.key][0:2]
						if self._Servos[s] == 'm': #only moves on KEYDOWN from middle position
							self._Servos[s] = p
							task = Note(self, s, self._pos_dict[p], self._pos_dict['m']) #create
							task.start() #run
					self.clock.tick(60)					


if __name__ == '__main__':
	music = Player('/dev/ttyACM0')
	music.pmcl()
