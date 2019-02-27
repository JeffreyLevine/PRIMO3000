""" accepts keyboard input and sends commands to Pololu Maestro controller """
import time, math, logging, struct, sys

import maestro
#Servo
Pololu = maestro.Controller(ttyStr='/dev/ttyAMA0')

pos_dict = { 'l': 4000, 'm': 6000, 'h': 8000 } #l = low, m = mid, h = high
Servos = ['m', 'm', 'm', 'm'] # start with 4, latter add cmd arg to set #
#servo0 high = 1 low = q servo1 high = 2 low = w ...

def opositeKey (key):
	""" takes key as pygame, returns oposing pygame key """
	ko = { K_1: K_q, K_q: K_1,
	 K_2: K_w, K_w: K_2,
	 K_3: K_e, K_e: K_3,
	 K_4: K_r, K_r: K_4 } #!!!need to fill this out!!!
	return ko[key]


def keyToServo (key):
	""" takes key as pygame, returns servo and position """
	kd = { K_1: [0, 'h'], K_q: [0, 'l'],
	 K_2: [1, 'h'], K_w: [1, 'l'],
	 K_3: [2, 'h'], K_e: [2, 'l'],
	 K_4: [3, 'h'], K_r: [3, 'l'] } #!!!need to fill this out!!!
	return kd[key][0], kd[key][1] #servo, position

import pygame
from pygame.locals import *
#Initialise PyGame
pygame.init()
logging.debug ("PyGame started")
clock = pygame.time.Clock()
clock.tick(30)

#Initialise screen.
flags = DOUBLEBUF | HWACCEL
size = [640, 320]
screen = pygame.display.set_mode(size, flags)
screen.fill(0x222222) #grey
screen.set_alpha(None)

print("Start Playing")

while True:
	# Main program loop.
	for event in pygame.event.get():
		if event.type == QUIT: # or (event.type == KEYUP and event.key == K_ESCAPE):
			print "Exiting...."
			pygame.quit()
			sys.exit()   # end program.
		elif event.type == KEYUP: #release
			s, p = keyToServo(event.key)
			if Servos[s] != 'm': #only care if the servo is high or low
				if not(pygame.key.get_pressed()[opositeKey(event.key)]): #need to check state of oposing key
					Pololu.setTarget(s, pos_dict['m']) #send command
					Servos[s] = 'm' #save
					print("KEY UP", s)
		elif event.type == KEYDOWN: #press
			s, p = keyToServo(event.key)
			if Servos[s] == 'm': #only moves on KEYDOWN from middle position
				Pololu.setTarget(s, pos_dict[p]) #send command
				Servos[s] = p #save
				print(" KEY DOWN", s, p)
			#there is no elif because striker will not move
	pygame.display.update()
	clock.tick(30) #30fps
				
