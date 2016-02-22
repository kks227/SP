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
#	DEAD
statusEnum = enum('GROUND', 'JUMPED', 'AIR', 'LADDER', 'CLIMB', 'ACT', 'DEAD')



# sprite: superclass
class Sprite(object):
	def __init__(self, x=0, y=0):
		# set member variables
		self.initGenerals(x, y)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y):
		self.xspeed = 0 # 0: not moving, 1: to right, -1: to left
		self.yspeed = 0
		self.collideTerrain = [None]*4
		self.status = statusEnum.AIR
		self.step = 0
		self.rect = Rect((x, y), (32, 24))
		# variables that have default values
		# those can be set on initProperties functions
		self.speed = 1
		self.gravity = 0 # accelerating vertical speed by gravity
		self.jumpPower = 0
		self.prefix = '__dummy' # common perfix of image names
		self.imgName = []
		self.imgName.append('')
		self.imgList = defaultdict(list)

	def initProperties(self):
		pass

	def initDependencies(self):
		self.prevRect = self.rect
		for key in self.imgName:
			if key == '':
				self.imgList[key] = ImagePack.img[self.prefix]
			else:
				self.imgList[key] = ImagePack.img[self.prefix + '_' + key]



	def draw(self):
		ImagePack.draw(self.rect, self.imgList[''])



	def update(self):
		# sprite horizontal moving
		self.rect.x += self.xspeed * self.speed
		# sprite vertical moving by gravity
		self.rect.y += self.yspeed

	def updatePreorder(self):
		self.prevRect = self.rect.copy()
		self.collideTerrain = [None]*4

	def updatePostorder(self):
		self.step += 1