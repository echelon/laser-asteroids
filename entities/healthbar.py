"""
Player's health bar
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

class HealthBar(Entity):

	HEALTH_MAX = SHIP_HEALTH_MAX

	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0, radius = 1200):
		super(HealthBar, self).__init__(x, y, r, g, b)
		self.radius = radius
		self.drawn = False

		self.pauseFirst = True
		self.pauseLast = True

		self.skipDraw = False

		self.health = HealthBar.HEALTH_MAX

	def subtract(self, health):
		self.health = max(self.health - health, 0)

	def produce(self):
		"""
		Generate the points of the circle.
		"""
		r, g, b = (0, 0, 0)

		# Generate points
		full = self.radius/2

		hPerc = self.health/float(HealthBar.HEALTH_MAX)
		ihPerc = 1.0 - hPerc
		green = full * hPerc
		red = full * (1.0 - hPerc)

		print hPerc, green, red

		pts = []
		pts.append({'x': full, 'y': full})
		pts.append({'x': -full*2 + full*3*ihPerc, 'y': full})

		# RED
		pts.append({'x': full - full*3, 'y': full})
		pts.append({'x': -full*2, 'y': full})
		#pts.append({'x': -full*2, 'y': full})
		#pts.append({'x': -full*2, 'y': full})

		# Translate points
		for pt in pts:
			pt['x'] += self.x
			pt['y'] += self.y

		r = 0 if not self.r else int(self.r / LASER_POWER_DENOM)
		g = 0 if not self.g or LASER_POWER_DENOM > 4 else self.g
		b = 0 if not self.b else int(self.b / LASER_POWER_DENOM)

		def make_line(pt1, pt2, steps=200, r=r, g=g, b=b):
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

		# GREEN
		for p in make_line(pts[0], pts[1], HEALTHBAR_EDGE_SAMPLE_PTS):
			break
		for i in range(int(round(HEALTHBAR_VERTEX_SAMPLE_PTS/2.0))):
			yield p
		for p in make_line(pts[0], pts[1], HEALTHBAR_EDGE_SAMPLE_PTS):
			yield p
		for i in range(HEALTHBAR_VERTEX_SAMPLE_PTS):
			yield p
		for p in make_line(pts[1], pts[0], HEALTHBAR_EDGE_SAMPLE_PTS):
			self.lastPt = p # KEEP BOTH
			yield p
		for i in range(int(round(HEALTHBAR_VERTEX_SAMPLE_PTS/2.0))):
			self.lastPt = p # KEEP BOTH
			yield p

		# BLANK
		#for p in make_line(pts[0], pts[1], HEALTHBAR_EDGE_SAMPLE_PTS*2, r=0, g=0, b=0):
		#	yield p

		# RED
		if red:
			for p in make_line(pts[2], pts[3], HEALTHBAR_EDGE_SAMPLE_PTS, r=CMAX, g=0, b=0):
				break
			for i in range(int(round(HEALTHBAR_VERTEX_SAMPLE_PTS/2.0))):
				yield p
			for p in make_line(pts[2], pts[3], HEALTHBAR_EDGE_SAMPLE_PTS, r=CMAX, g=0, b=0):
				yield p
			for i in range(HEALTHBAR_VERTEX_SAMPLE_PTS):
				yield p
			for p in make_line(pts[3], pts[2], HEALTHBAR_EDGE_SAMPLE_PTS, r=CMAX, g=0, b=0):
				self.lastPt = p # KEEP BOTH
				yield p
			for i in range(int(round(HEALTHBAR_VERTEX_SAMPLE_PTS/2.0))):
				self.lastPt = p # KEEP BOTH
				yield p





		self.drawn = True

