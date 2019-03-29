#!/usr/bin/python

'''
Creates servo commands and visualization accompanying key presses
From testing : 4 simultaneous keystrokes, can have 6-8 keys down at same time
'''

import sys
import maestro
import pygame
from pygame.locals import *

class Player:
	""" accepts commands via keyboard then can indicate holding key by color white to black """
	def __init__(self, ser_port, display = True):
		self._display = display
		self._pos_dict = { 'l': 4000, 'm': 6000, 'h': 8000 } #l = low, m = mid, h = high
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
		self._key_color_matrix = [ #current color on screen
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
		#self._Pololu = maestro.Controller(ttyStr = ser_port) #servo controller
		self._Pololu = maestro.Controller() #servo controller
		for i in range(18): #initial position
			self._Pololu.setSpeed(i, 0) #ensure max speed
			self._Pololu.setTarget(i, self._pos_dict['m']) #goto middle
		pygame.init() #initialize pygame
		if self._display == True:
			self.clock = pygame.time.Clock()
			self.clock.tick(60)
			self.screen = pygame.display.set_mode([500, 200], DOUBLEBUF | HWACCEL) #initialize screen
			self.screen.set_alpha(None)
		else:
			self.screen = pygame.display.set_mode([300, 1], DOUBLEBUF | HWACCEL) #initialize screen
			self.screen.set_alpha(None)
		pygame.display.set_caption("Keyboard Servo Player") #title
	def primo(self):
		""" loop to receive keystrokes then send command and update screen """
		while True: #main program loop
			for event in pygame.event.get(): #event loop
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYUP: #release
					if self._key_convert.has_key(event.key):
						s = self._key_convert[event.key][0]
						if self._Servos[s] != 'm': #only care if the servo is high or low
							#get_pressed returns an array containing over 100 keys
							if not(pygame.key.get_pressed()[self._key_convert[event.key][2]]): #need to check state of oposing key
								self._Pololu.setTarget(s, self._pos_dict['m']) #send command
								self._Servos[s] = 'm' #save position
								r, c = self._key_convert[event.key][3:]
								self._key_color_matrix[r][c] = 0
				elif event.type == KEYDOWN: #press
					if self._key_convert.has_key(event.key):
						s, p = self._key_convert[event.key][0:2]
						if self._Servos[s] == 'm': #only moves on KEYDOWN from middle position
							self._Pololu.setTarget(s, self._pos_dict[p]) #send command
							self._Servos[s] = p #save position
							r, c = self._key_convert[event.key][3:]
							self._key_color_matrix[r][c] = 255
			if self._display == True:
				for r in range(4): #setup new screen
					for c in range(10):
						color = (self._key_color_matrix[r][c], self._key_color_matrix[r][c], self._key_color_matrix[r][c])
						rect = (c*50, r*50, 50, 50)
						self.screen.fill(color, rect)
						if self._key_color_matrix[r][c] > 9: #reduce color to black
							self._key_color_matrix[r][c] -= 10
				self.screen.fill((184, 16, 16), (400 , 100, 100, 100)) #fill out space that has no corresponding key
				pygame.display.update() #screen changes on monitor
				self.clock.tick(60) #60fps makes servos more responsive

if __name__ == '__main__':
	if (len(sys.argv) > 1): #parse cmd line args
		if sys.argv[1] == 'hide':
			music = Player('/dev/ttyACM0', False)
		elif sys.argv[1] == 'help':
			print("'hide' disables the visualization of key presses")
			sys.exit()
		else:
			print("unknown argument(s)")
			sys.exit()
	else: #default is to show the light grid
		music = Player('/dev/ttyACM0',True)
	music.primo()
