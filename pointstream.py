"""
PointStream -- The main galvo multiple object drawing algorithm.
			   This code is responsible for drawing multiple objects.
			   It will need to be improved for efficiency.

	FIXME/NOTE: The documentation / variable names are a bit out of date.
				"Ball" means object.
"""

import math
import random
import itertools
import sys
import thread
import time
import pygame

# GLOBALS 
from globalvals import *

class PointStream(object):
	def __init__(self):
		self.called = False
		self.stream = self.produce()

		# A list of all the objects to draw
		# XXX: For now, add and remove manually. 
		self.objects = []

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

			for b in self.objects:
				b.cacheFirstPt()

			# Objects to destroy at end of loop
			destroy = []

			# Draw all the objects... 
			for i in range(len(self.objects)):
				curBall = self.objects[i]
				nextBall = self.objects[(i+1)%len(self.objects)]

				# Cull the object if it is marked destroy
				if curBall.destroy:
					destroy.append(i)
					continue

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
			for b in self.objects:
				b.drawn = False

			# Items to destroy
			destroy.sort()
			destroy.reverse()
			for i in destroy:
				self.objects.pop(i)

	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d

