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
from colors import *
from entities import *
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

		# debug
		numButtons = joystick.get_numbuttons()
		print joystick.get_name()
		print numButtons

		# Player Object
		self.obj = Square(0, 0, r=rgb[0], g=rgb[1], b=rgb[2], radius=radius)
		DRAW.objects.append(self.obj)

	def __str__(self):
		return self.js.get_name()

"""
THREADS
"""

def dac_thread():
	global PLAYERS, DRAW

	debug()

	while True:
		try:
			ps = PointStream()
			DRAW = ps

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

	p1 = Player(pygame.joystick.Joystick(0),
			rgb = COLOR_PINK)


	PLAYERS.append(p1)

	numButtons = p1.js.get_numbuttons() # XXX NO!

	while True:
		e = pygame.event.get()

		for p in PLAYERS:

			# Joysticks 
			lVert = p.js.get_axis(1)
			lHori= p.js.get_axis(0)
			rVert = p.js.get_axis(4)
			rHori= p.js.get_axis(3)

			if abs(rVert) > 0.2:
				print "ADD VEL1"
				y = p.obj.y
				y += -1 * int(rVert * SIMPLE_TRANSLATION_SPD)
				if MIN_Y < y < MAX_Y:
					p.obj.y = y

			if abs(rHori) > 0.2:
				print "ADD VEL2"
				x = p.obj.x
				x += -1 * int(rHori * SIMPLE_TRANSLATION_SPD)
				if MIN_X < x < MAX_X:
					p.obj.x = x

			# Player rotation
			t = math.atan2(lVert, lHori)
			p.obj.theta = t

			# Firing the weapon
			trigger = False if p.js.get_axis(5) in [0.0, -1.0] else True

			if trigger:
				ang = p.obj.theta + math.pi
				b = Bullet(p.obj.x, p.obj.y, rgb=COLOR_YELLOW, shotAngle=ang)
				DRAW.objects.append(b)

		time.sleep(0.02) # Keep this thread from hogging CPU


NUM_ENEMIES = 0 # XXX: MOve to game state object... 

def game_thread():
	global DRAW, NUM_ENEMIES

	def spawn_enemy():
		x = random.randint(ENEMY_SPAWN_MIN_X, ENEMY_SPAWN_MAX_X)
		y = random.randint(ENEMY_SPAWN_MIN_Y, ENEMY_SPAWN_MAX_Y)
		xVel = random.randint(ENEMY_SPAWN_MIN_X_VEL, ENEMY_SPAWN_MAX_X_VEL)
		yVel = random.randint(ENEMY_SPAWN_MIN_X_VEL, ENEMY_SPAWN_MAX_X_VEL)

		e = Enemy(x, y, r=CMAX, g=CMAX, b=CMAX, radius=1200)
		e.velX = xVel
		e.velY = yVel

		DRAW.objects.append(e)
		NUM_ENEMIES+=1

	while True:
		print "GameThread objects: %d" % len(DRAW.objects)
		try:

			"""
			Game Events
			"""
			if random.randint(0, 5) == 0 and NUM_ENEMIES <= 10:
				print "NEW ENEMY"
				spawn_enemy()

			"""
			Handle Onscreen Objects
			"""
			for i in range(len(DRAW.objects)):
				obj = DRAW.objects[i]

				# PLAYER
				if type(obj) == Square:
					continue

				# BULLETS
				elif type(obj) == Bullet:
					x = obj.x
					y = obj.y
					x += BULLET_SPEED * math.cos(obj.theta)
					y += BULLET_SPEED * math.sin(obj.theta)
					if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y :
						obj.destroy = True
						continue
					obj.x = x
					obj.y = y

				elif type(obj) == Enemy:
					pass
					x = obj.x
					y = obj.y
					x += obj.velX
					y += obj.velY
					if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y :
						obj.destroy = True
						continue
					obj.x = x
					obj.y = y


			time.sleep(0.02)

		except:
			print "GAME EXCEPTION"*100
			#restart_game()
			time.sleep(0.02)

thread.start_new_thread(dac_thread, ())
thread.start_new_thread(game_thread, ())
thread.start_new_thread(joystick_thread, ())

"""
UNUSED STUFF
"""

def restart_game():
	global DRAW
	#DRAW.objects = DRAW.objects[0:1]
	for i in range(len(DRAW.objects)):
		if i == 0:
			continue
		DRAW.objects.pop(i)
	for obj in DRAW.objects:
		obj.x = 0
		obj.y = 0

def debug():
	#b = Bullet(1000, 1000, r=CMAX, g=CMAX)
	#DRAW.objects.append(b) 
	pass


while True:
	time.sleep(200)


