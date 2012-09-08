#!/usr/bin/env python

# STDLIB
import math
import random
import itertools
import sys
import thread
import time

# PYGAME
import pygame

# MY CODES
from daclib import dac
from daclib.common import *
from globalvals import *
from entities import Entity, Square
from pointstream import PointStream

"""
Main Program
"""

DRAW = None # Will be the global PointStream

class Player(object):
	"""
	Player (conflated)
		- Contain joystick ref
		- Contain visual object
	"""
	def __init__(self, joystick, radius=BALL_RADIUS, rgb=(CMAX, CMAX, CMAX)):
		self.js = joystick
		self.score = 0
		self.pid = 0

		# Joystick
		joystick.init()

		# Laser
		self.obj = Square(0, 0, r=rgb[0], g=rgb[1], b=rgb[2], radius=radius)

		print self.obj
		print self.obj
		print self.obj
		print self.obj
		print self.obj
		print self.obj
		print self.obj

		DRAW.objects.append(self.obj)

		print joystick.get_name()

		numButtons = joystick.get_numbuttons()
		print numButtons


	def __str__(self):
		return self.js.get_name()

"""
THREADS
"""

def dac_thread():
	global PLAYERS, DRAW

	ps = PointStream()
	DRAW = ps

	while True:
		try:
			d = dac.DAC(dac.find_first_dac())
			d.play_stream(ps)

		except Exception as e:

			import sys, traceback
			print '\n---------------------'
			print 'Exception: %s' % e
			print '- - - - - - - - - - -'
			traceback.print_tb(sys.exc_info()[2])
			print "\n"
			pass

			# In case we went off edge, recenter. 
			# XXX: This is just laziness
			for p in PLAYERS:
				p.obj.x = 0
				p.obj.y = 0

def joystick_thread():
	"""Manage the joysticks with PyGame"""
	global PLAYERS

	pygame.joystick.init()
	pygame.display.init()
	
	if not pygame.joystick.get_count():
		print "No Joystick detected!"
		sys.exit()

	p1 = Player(pygame.joystick.Joystick(0))
	#p2 = Player(pygame.joystick.Joystick(1))

	PLAYERS.append(p1)
	#PLAYERS.append(p2)

	numButtons = p1.js.get_numbuttons() # XXX NO!

	while True:
		e = pygame.event.get()

		for p in PLAYERS:

			vel1 = p.js.get_axis(1) # Left joystick
			vel2 = p.js.get_axis(0)

			print "Velocities: %f, %f" % (vel1, vel2)

			if abs(vel1) > 0.2:
				print "ADD VEL1"
				y = p.obj.y
				y += -1 * int(vel1 * SIMPLE_TRANSLATION_SPD)
				if MIN_Y < y < MAX_Y:
					p.obj.y = y

			if abs(vel2) > 0.2:
				print "ADD VEL2"
				x = p.obj.x
				x += -1 * int(vel2 * SIMPLE_TRANSLATION_SPD)
				if MIN_X < x < MAX_X:
					p.obj.x = x

		time.sleep(0.02) # Keep this thread from hogging CPU

thread.start_new_thread(joystick_thread, ())
thread.start_new_thread(dac_thread, ())

while True:
	time.sleep(200)


