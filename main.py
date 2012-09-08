#!/usr/bin/env python

"""
A simple game of Pong with PS3 controllers.

	PS3 Mappings
	------------
	Axis 0	- Left horiontal (-1 is up, 1 is down)
	Axis 1	- Left vertical
	Axis 2	- Right horizontal 
	Axis 3	- Right vertical 

	Button 4	- Up
	Button 5	- Right
	Button 6	- Down
	Button 7	- Left

	Button 12	- Triangle
	Button 13	- Circle
	Button 14	- X
	Button 15	- Square 

	Button 16	- PS Button

Use qtsixa to pair controllers, then sixad to start the bluetooth 
daemon.
"""

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

class PointStream(object):
	def __init__(self):
		self.called = False
		self.stream = self.produce()

	def produce(self):
		"""
		This infinite loop functions as an infinite point generator.
		It generates points for both balls as well as the "blanking"
		that must occur between them.
		"""
		while True: 

			# Generate and cache the first points of the objects.
			# Necessary in order to slow down galvo tracking from 
			# ball-to-ball as we move to the next object. 

			for b in balls:
				b.cacheFirstPt()

			# Draw all the balls... 
			for i in range(len(balls)):
				curBall = balls[i]
				nextBall = balls[(i+1)%len(balls)]

				# Draw the ball
				if not curBall.drawn:
					yield curBall.firstPt # This was cached upfront
					for x in curBall.produce():
						yield x

				# Paint last pt for smoothness
				# XXX: Remove?
				for x in xrange(BLANK_SAMPLE_PTS):
					yield curBall.firstPt

				# Paint empty for smoothness
				# XXX: Remove? 
				for x in xrange(BLANK_SAMPLE_PTS):
					yield (curBall.lastPt[0], curBall.lastPt[1], 0, 0, 0)

				# Now, track to the next object. 
				lastX = curBall.lastPt[0]
				lastY = curBall.lastPt[1]
				xDiff = curBall.lastPt[0] - nextBall.firstPt[0]
				yDiff = curBall.lastPt[1] - nextBall.firstPt[1]
				mv = BLANK_SAMPLE_PTS
				for i in xrange(mv): 
					percent = i/float(mv)
					xb = int(lastX - xDiff*percent)
					yb = int(lastY - yDiff*percent)
					# If we want to 'see' the tracking path. 
					if SHOW_BLANKING_PATH: # FIXME: Rename 'tracking'
						yield (xb, yb, 0, CMAX, 0)
					else:
						yield (xb, yb, 0, 0, 0)

			# Reset ball state (nasty hack for point caching)
			for b in balls:
				b.drawn = False



	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d

"""
Main Program
"""

ps = PointStream()

def dac_thread():
	global PLAYERS

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

		balls.append(self.obj)

		print joystick.get_name()

		numButtons = joystick.get_numbuttons()
		print numButtons


	def __str__(self):
		return self.js.get_name()

"""
Global objects
"""
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
	time.sleep(20)


