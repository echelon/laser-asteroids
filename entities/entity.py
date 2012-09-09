"""
ENTITY BASE CLASS
	* Handles collision detection
	* Handles x, y, z, velocity, color
	* Handles blanking, deallocation, etc.

	(And by 'handles', I mean 'marks' and then passes off to
	 the PointStream instance.)
"""

# STDLIB
import math
import random
import itertools
import sys
import thread
import time
import pygame

# GLOBALS 
from globalvals import *

# XXX - added rotation, velX, velY
class Entity(object):

	# Static object counter. 
	ID_COUNTER = 0

	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0):

		# Positioning stuff
		self.x = x
		self.y = y
		self.xVel = 0.0
		self.yVel = 0.0
		self.rotation = 0.0

		# Drawing specifics 
		self.r = r
		self.g = g
		self.b = b
		self.doBlanking = True # object should get blanking? 
		self.skipDraw = False

		# Collision and deallocation
		self.collides = True
		self.collisionRadius = 1000
		self.destroy = False
		#self.offscreen = False

		# Cached first and last points. 
		# (Part of the PointStream algo.)
		self.firstPt = (0, 0, 0, 0, 0)
		self.lastPt = (0, 0, 0, 0, 0)

		# Id handling
		self.entityId = Entity.ID_COUNTER
		Entity.ID_COUNTER+=1

	def produce(self):
		self.lastPt = (0, 0, 0, 0, 0)
		return self.lastPt

	def cacheFirstPt(self):
		"""
		I need to cache the first point generated so that I can
		slowly advance the galvos to the next object without starting
		drawing.
		"""
		for x in self.produce():
			self.firstPt = x
			break


	def checkCollide(self, other):
		"""
		Determine if two objects collide.
		"""
		rad = other.collisionRadius + self.collisionRadius
		hyp = math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
		return (hyp < rad)

