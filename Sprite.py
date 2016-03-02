from collections import defaultdict

from Tool import *
from ImagePack import *

import pygame
from pygame.locals import *



# status
#	GROUND
#	JUMPED: persists only 1 frame and turns into AIR status.
#	AIR
#	LADDER: on ladder, rope, etc. doesn't fall.
#	CLIMB: climbing terrains on sides.
#	ACT
statusEnum = enum('GROUND', 'JUMPED', 'AIR', 'LADDER', 'CLIMB', 'ACT')



# sprite: superclass
class Sprite(object):
	def __init__(self, x=0, y=0, name='__dummy'):
		# set member variables
		self.initGenerals(x, y, name)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y, name):
		self.xspeed = 0 # 0: not moving, 1: to right, -1: to left
		self.yspeed = 0
		self.collideTerrain = [None]*4
		self.status = statusEnum.AIR
		self.step = 0
		self.xadd = 0 # additional coordinate offset values
		self.yadd = 0
		# coordinate and mask(vulnerable area) size
		self.x = float(x)
		self.y = float(y)
		self.rect = Rect((x, y), (32, 32))
		self.xflip = False # False: leftward, True: rightward
		# variables that have default values
		# those can be set on initProperties functions
		self.gravity = 0 # accelerating vertical speed by gravity
		self.jumpPower = 0
		self.name = name # common perfix of image names
		self.imgName = []
		self.imgName.append('')
		self.imgList = defaultdict(list)

	def initProperties(self):
		pass

	def initDependencies(self, prefix=''):
		self.prevRect = self.rect
		for key in self.imgName:
			if key == '':
				self.imgList[key] = ImagePack.img[prefix + self.name]
			else:
				self.imgList[key] = ImagePack.img[prefix + self.name + '_' + key]

	def setCoord(self, x, y):
		self.rect.topleft = (x, y)



	def draw(self):
		ImagePack.draw(DrawOption(self.rect, self.imgList['']))



	def update(self):
		# sprite horizontal moving
		self.rect.x += self.xspeed + self.xadd
		# sprite vertical moving by gravity
		self.rect.y += self.yspeed + self.yadd

	def updatePreorder(self):
		self.prevRect = self.rect.copy()
		self.collideTerrain = [None]*4
		self.xadd = self.yadd = 0

	def updatePostorder(self):
		self.step += 1
		# renew rect's coordinate (float to int) (f*ck... why Rect doesn't apply float?)