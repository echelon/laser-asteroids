
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

class Square(Entity):
	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, radius = 1200):
		super(Square, self).__init__(x, y, r, g, b)
		self.radius = radius 
		self.drawn = False

		self.pauseFirst = True 
		self.pauseLast = True 

	def produce(self):
		"""
		Generate the points of the circle.
		"""
		r, g, b = (0, 0, 0)

		"""
		Figured it out! This is where the "tails" were coming from!
		We have to blank first with NO color. The lasers turn on before
		the galvos reach their destination. Duh. I had it figured in 
		reverse. 
		"""
		"""
		if self.pauseFirst:
			x = int(math.cos(0) * self.radius) + self.x
			y = int(math.sin(0) * self.radius) + self.y
			r = 0 if not self.r else int(CMAX / LASER_POWER_DENOM)
			g = 0 if not self.g or LASER_POWER_DENOM > 4 else CMAX
			b = 0 if not self.b else int(CMAX / LASER_POWER_DENOM)
			self.lastPt = (x, y, 0, 0, 0)
			for i in xrange(PAUSE_START_PTS):
				yield self.lastPt
		"""

		# Generate points
		ed = self.radius/2

		x1 = self.x + ed
		y1 = self.y + ed
		x2 = self.x - ed
		y2 = self.y + ed
		x3 = self.x - ed
		y3 = self.y - ed
		x4 = self.x + ed
		y4 = self.y - ed

		pt1 = {'x': x1, 'y': y1}
		pt2 = {'x': x2, 'y': y2}
		pt3 = {'x': x3, 'y': y3}
		pt4 = {'x': x4, 'y': y4}

		r = 0 if not self.r else int(CMAX / LASER_POWER_DENOM)
		g = 0 if not self.g or LASER_POWER_DENOM > 4 else CMAX
		b = 0 if not self.b else int(CMAX / LASER_POWER_DENOM)

		def make_line(pt1, pt2, steps=200):
			xdiff = pt1['x'] - pt2['x']
			ydiff = pt1['y'] - pt2['y']
			line = []
			for i in xrange(0, steps, 1):
				j = float(i)/steps
				x = pt1['x'] - (xdiff * j)
				y = pt1['y'] - (ydiff * j)
				line.append((x, y, r, g, b)) # XXX FIX COLORS
			return line

		for p in make_line(pt1, pt2, SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pt2, pt3, SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pt3, pt4, SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pt4, pt1, SQUARE_EDGE_SAMPLE_PTS):
			self.lastPt = p
			yield p



		"""
		for i in xrange(BALL_SAMPLE_PTS):
			i = 2 * math.pi * float(i) / BALL_SAMPLE_PTS * CIRCLE_ROTATIONS 
			x = int(math.cos(i) * self.radius) + self.x
			y = int(math.sin(i) * self.radius) + self.y

			r = 0 if not self.r else int(CMAX / LASER_POWER_DENOM)
			g = 0 if not self.g or LASER_POWER_DENOM > 4 else CMAX
			b = 0 if not self.b else int(CMAX / LASER_POWER_DENOM)

			self.lastPt = (x, y, r, g, b)
			yield self.lastPt
		"""


		"""
		if self.pauseLast:
			# XXX: Crude hack for broken edge
			for i in xrange(PAUSE_END_PTS): 
				yield (self.firstPt[0], self.firstPt[1], r, g, b)

			for i in xrange(PAUSE_END_PTS):
				yield self.firstPt

		"""
		self.drawn = True

# TODO: Rename circle
class Ball(Entity):
	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, radius = 1200):
		super(Ball, self).__init__(x, y, r, g, b)
		self.radius = radius
		self.drawn = False

		self.pauseFirst = True 
		self.pauseLast = True 

		print "CREATED BALL"*1000

	def produce(self):
		"""
		Generate the points of the circle.
		"""
		r, g, b = (0, 0, 0)

		"""
		Figured it out! This is where the "tails" were coming from!
		We have to blank first with NO color. The lasers turn on before
		the galvos reach their destination. Duh. I had it figured in 
		reverse. 
		"""
		if self.pauseFirst:
			x = int(math.cos(0) * self.radius) + self.x
			y = int(math.sin(0) * self.radius) + self.y
			r = 0 if not self.r else int(CMAX / LASER_POWER_DENOM)
			g = 0 if not self.g or LASER_POWER_DENOM > 4 else CMAX
			b = 0 if not self.b else int(CMAX / LASER_POWER_DENOM)
			self.lastPt = (x, y, 0, 0, 0)
			for i in xrange(PAUSE_START_PTS):
				yield self.lastPt

		for i in xrange(BALL_SAMPLE_PTS):
			i = 2 * math.pi * float(i) / BALL_SAMPLE_PTS * CIRCLE_ROTATIONS 
			x = int(math.cos(i) * self.radius) + self.x
			y = int(math.sin(i) * self.radius) + self.y

			r = 0 if not self.r else int(CMAX / LASER_POWER_DENOM)
			g = 0 if not self.g or LASER_POWER_DENOM > 4 else CMAX
			b = 0 if not self.b else int(CMAX / LASER_POWER_DENOM)

			self.lastPt = (x, y, r, g, b)
			yield self.lastPt

		if self.pauseLast:
			# XXX: Crude hack for broken edge
			for i in xrange(PAUSE_END_PTS): 
				yield (self.firstPt[0], self.firstPt[1], r, g, b)

			for i in xrange(PAUSE_END_PTS):
				yield self.firstPt

		self.drawn = True

if __name__ == '__main__':
	print "Testing entities.py"

	a = Ball()
	a.produce()
	b = Square()

