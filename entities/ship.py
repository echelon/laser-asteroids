"""
Player's ship
	TODO: DOC
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

# Base class
from entity import Entity

class Ship(Entity):

	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, rgb=None, radius = 1200):

		if rgb:
			r = rgb[0]
			g = rgb[1]
			b = rgb[2]

		super(Ship, self).__init__(x, y, r, g, b)
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

		# Generate points
		ed = self.radius/2

		pts = []
		pts.append({'x': ed, 'y': ed})
		pts.append({'x': -ed, 'y': ed})

		pts.append({'x': -ed-ed*2, 'y': 0})

		pts.append({'x': -ed, 'y': -ed})
		pts.append({'x': ed, 'y': -ed})

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

		r = 0 if not self.r else int(self.r / LASER_POWER_DENOM)
		g = 0 if not self.g or LASER_POWER_DENOM > 4 else self.g
		b = 0 if not self.b else int(self.b / LASER_POWER_DENOM)

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

		# DRAW THE SHAPE

		p = None # Save in scope

		for p in make_line(pts[0], pts[1], SHIP_EDGE_SAMPLE_PTS):
			break
		for i in range(int(round(SHIP_VERTEX_SAMPLE_PTS/2.0))):
			yield p
		for p in make_line(pts[0], pts[1], SHIP_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SHIP_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[1], pts[2], SHIP_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SHIP_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[2], pts[3], SHIP_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SHIP_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[3], pts[4], SHIP_EDGE_SAMPLE_PTS):
			yield p
		for i in range(SHIP_VERTEX_SAMPLE_PTS):
			yield p

		for p in make_line(pts[4], pts[0], SHIP_EDGE_SAMPLE_PTS):
			self.lastPt = p # KEEP BOTH
			yield p
		for i in range(int(round(SHIP_VERTEX_SAMPLE_PTS/2.0))):
			self.lastPt = p # KEEP BOTH
			yield p

		self.drawn = True

