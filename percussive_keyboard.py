#!/usr/bin/python

""" accepts commands via keyboard then indicates holding key by color white to black """
""" not sure how pythonic wrapping the dict lookup in a function is """
""" there may be a better way to do the nested for loops """
import sys
import maestro
import pygame
from pygame.locals import *

class Player:
	def __init__(self, ser_port):
		self.pos_dict = { 'l': 4000, 'm': 6000, 'h': 8000 } #l = low, m = mid, h = high
		self.Servos = ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm']
		#servo0 high = 1 low = q servo1 high = 2 low = w ...
		self.key_color_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
		#servo controller
		self.Pololu = maestro.Controller(ttyStr=ser_port) #set to default on real hardware
		#initialise pygame
		pygame.init()
		self.clock = pygame.time.Clock()
		self.clock.tick(30)
		#initialise screen
		flags = DOUBLEBUF | HWACCEL
		size = [500, 200]
		self.screen = pygame.display.set_mode(size, flags)
		self.screen.fill(0x222222) #grey
		self.screen.set_alpha(None)
		pygame.display.set_caption("Keyboard Servo Player") #title
	def opositeKey (self, key):
		""" takes key as pygame, returns oposing pygame key """
		ko = { K_1: K_q, K_q: K_1,
			   K_2: K_w, K_w: K_2,
			   K_3: K_e, K_e: K_3,
			   K_4: K_r, K_r: K_4,
			   K_5: K_t, K_t: K_5,
			   K_6: K_y, K_y: K_6,
			   K_7: K_u, K_u: K_7,
			   K_8: K_i, K_i: K_8,
			   K_9: K_o, K_o: K_9,
			   K_0: K_p, K_p: K_0,
			   K_a: K_z, K_z: K_a,
			   K_s: K_x, K_x: K_s,
			   K_d: K_c, K_c: K_d,
			   K_f: K_v, K_v: K_f,
			   K_g: K_b, K_b: K_g,
			   K_h: K_n, K_n: K_h,
			   K_j: K_m, K_m: K_j,
			   K_k: K_COMMA, K_COMMA: K_k }
		if ko.has_key(key):
			return ko[key] #oposite
		else:
			return -1
	def keyToServo (self, key):
		""" takes key as pygame, returns servo and position """
		kd = { K_1: [0, 'h'], K_q: [0, 'l'],
			   K_2: [1, 'h'], K_w: [1, 'l'],
			   K_3: [2, 'h'], K_e: [2, 'l'],
			   K_4: [3, 'h'], K_r: [3, 'l'],
			   K_5: [4, 'h'], K_t: [4, 'l'],
			   K_6: [5, 'h'], K_y: [5, 'l'],
			   K_7: [6, 'h'], K_u: [6, 'l'],
			   K_8: [7, 'h'], K_i: [7, 'l'],
			   K_9: [8, 'h'], K_o: [8, 'l'],
			   K_0: [9, 'h'], K_p: [9, 'l'],
			   K_a: [10, 'h'], K_z: [10, 'l'],
			   K_s: [11, 'h'], K_x: [11, 'l'],
			   K_d: [12, 'h'], K_c: [12, 'l'],
			   K_f: [13, 'h'], K_v: [13, 'l'],
			   K_g: [14, 'h'], K_b: [14, 'l'],
			   K_h: [15, 'h'], K_n: [15, 'l'],
			   K_j: [16, 'h'], K_m: [16, 'l'],
			   K_k: [17, 'h'], K_COMMA: [17, 'l'] }
		if kd.has_key(key):
			return kd[key][0], kd[key][1] #servo, position
		else:
			return -1, -1
	def keyToMatrix (self, key):
		""" takes key as pygame, returns row and col """
		km = { K_1: [0,0], K_2: [0,1], K_3: [0,2], K_4: [0,3],
			   K_5: [0,4], K_6: [0,5], K_7: [0,6], K_8: [0,7],
			   K_9: [0,8], K_0: [0,9], K_q: [1,0], K_w: [1,1],
			   K_e: [1,2], K_r: [1,3], K_t: [1,4], K_y: [1,5],
			   K_u: [1,6], K_i: [1,7], K_o: [1,8], K_p: [1,9],
			   K_a: [2,0], K_s: [2,1], K_d: [2,2], K_f: [2,3],
			   K_g: [2,4], K_h: [2,5], K_j: [2,6], K_k: [2,7],
			   K_z: [3,0], K_x: [3,1], K_c: [3,2], K_v: [3,3],
			   K_b: [3,4], K_n: [3,5], K_m: [3,6], K_COMMA: [3,7] }
		if km.has_key(key):
			return km[key][0], km[key][1] #row, col
		else:
			return -1, -1
	def pmdl(self):
		""" loop to receive keystrokes then send command and update screen """
		while True: #main program loop
			for event in pygame.event.get(): #event loop
				if event.type == QUIT: # or (event.type == KEYUP and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				elif event.type == KEYUP: #release
					s, p = self.keyToServo(event.key)
					if s >= 0 and p >= 0:
						if self.Servos[s] != 'm': #only care if the servo is high or low
							#get_pressed returns an array containing over 100 keys
							if not(pygame.key.get_pressed()[self.opositeKey(event.key)]): #need to check state of oposing key
								self.Pololu.setTarget(s, self.pos_dict['m']) #send command
								self.Servos[s] = 'm' #save
								r, c = self.keyToMatrix(event.key)
								if r >= 0 and c >= 0:
									self.key_color_matrix[r][c] = 0
				elif event.type == KEYDOWN: #press
					s, p = self.keyToServo(event.key)
					if s >= 0 and p >= 0:
						if self.Servos[s] == 'm': #only moves on KEYDOWN from middle position
							self.Pololu.setTarget(s, self.pos_dict[p]) #send command
							self.Servos[s] = p #save
							r, c = self.keyToMatrix(event.key)
							if r >= 0 and c >= 0:
								self.key_color_matrix[r][c] = 255
						#there is no elif because striker will not move
			for r in range(4): #create new screen
				for c in range(10):
					color = (self.key_color_matrix[r][c], self.key_color_matrix[r][c], self.key_color_matrix[r][c])
					rect = (c*50, r*50, 50, 50)
					self.screen.fill(color, rect)
					if self.key_color_matrix[r][c] > 9: #reduce color to black
						self.key_color_matrix[r][c] -= 10
			color = (128, 32, 32)
			rect = (400 , 100, 100, 100)
			self.screen.fill(color, rect) #fill out space that has no corresponding key 
			pygame.display.update() #screen changes on monitor
			self.clock.tick(30) #30fps				

if __name__ == '__main__':
	music = Player('/dev/ttyAMA0')
	music.pmdl()
