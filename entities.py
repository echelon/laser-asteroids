
import math
import random
import itertools
import sys

import thread
import time

import pygame

# GLOBALS 
from globalvals import *

class Entity(object):
	"""
	Just an attempt at an OO interface.
	Nothing really fancy yet. 
	"""
	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0):
		self.x = x
		self.y = y
		self.r = r
		self.g = g
		self.b = b

		# Cached first and last points. 
		self.firstPt = 0
		self.lastPt = 0

	def produce(self):
		self.lastPt = (0, 0, 0, 0, 0)
		return self.lastPt

	def cacheFirstPt(self):
		"""
		I need to cache the first point generated so that I can 
		slowly advance the galvos to the next object without starting 
		drawing. 
		"""
		# XXX/FIXME: This is a hack (should I be using generators?)
		for x in self.produce():
			self.firstPt = x
			break

if __name__ == '__main__':
	print "Testing entities.py"

	a = Ball()
	a.produce()
	b = Square()

