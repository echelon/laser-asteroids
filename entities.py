
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

		# TODO
		self.rotation = 0.0
		self.velX = 0.0
		self.velY = 0.0

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

		self.theta = 0

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

		x1 = ed
		y1 = ed
		x2 = -ed
		y2 = ed
		x3 = -ed
		y3 = -ed
		x4 = ed
		y4 = -ed

		pts = []
		pts.append({'x': x1, 'y': y1})
		pts.append({'x': x2, 'y': y2})
		pts.append({'x': x3, 'y': y3})
		pts.append({'x': x4, 'y': y4})

		# Rotate points
		for p in pts:
			x = p['x']
			y = p['y']
			p['x'] = x*math.cos(self.theta) - y*math.sin(self.theta)
			p['y'] = y*math.cos(self.theta) + x*math.sin(self.theta)

		# Translate points
		for pt in pts:
			pt['x'] += self.x
			pt['y'] += self.y

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

		for p in make_line(pts[0], pts[1], SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pts[1], pts[2], SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pts[2], pts[3], SQUARE_EDGE_SAMPLE_PTS):
			yield p

		for p in make_line(pts[3], pts[0], SQUARE_EDGE_SAMPLE_PTS):
			self.lastPt = p
			yield p

		self.drawn = True

if __name__ == '__main__':
	print "Testing entities.py"

	a = Ball()
	a.produce()
	b = Square()

