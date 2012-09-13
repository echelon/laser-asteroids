"""
Represent various videogame controllers

TODO: Various play schemes/configs
XXX: UNTESTED
"""

import re

def setup_controls(joystick):
	"""
	Joystick wrapper.
	"""
	if re.search('playstation', joystick.get_name(), re.I):
		return Ps3Controller(joystick)

	elif re.search('playstation', joystick.get_name(), re.I):
		return XboxController(joystick)

	return Controller(joystick)

class Controller(object):

	def __init__(self, joystick):
		"""Pass a PyGame joystick instance."""
		self.js = joystick

	def getLeftHori():
		return 0.0

	def getLeftVert():
		return 0.0

	def getRightHori():
		return 0.0

	def getRightVert():
		return 0.0

	def getLeftTrigger():
		return 0.0

	def getRightTrigger():
		return 0.0

class XboxController(Controller):

	def __init__(self, joystick):
		super(XboxController, self).__init__(joystick)

	def getLeftHori():
		return self.js.get_axis(0)

	def getLeftVert():
		return self.js.get_axis(1)

	def getRightHori():
		return self.js.get_axis(3)

	def getRightVert():
		return self.js.get_axis(4)

	def getLeftTrigger():
		# TODO: Verify
		self.js.get_axis(2)

	def getRightTrigger():
		# TODO: Verify
		return self.js.get_axis(5)

class Ps3Controller(Controller):

	def __init__(self, joystick):
		super(XboxController, self).__init__(joystick)

	def getLeftHori():
		return self.js.get_axis(0)

	def getLeftVert():
		return self.js.get_axis(1)

	def getRightHori():
		return self.js.get_axis(2)

	def getRightVert():
		return self.js.get_axis(3)

	def getLeftTrigger():
		# TODO: Verify
		self.js.get_axis(12)

	def getRightTrigger():
		# TODO: Verify
		return self.js.get_axis(13)

