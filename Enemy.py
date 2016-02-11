import random

from Sprite import *
from ImagePack import *

import pygame
from pygame.locals import *



# enemy: superclass
class Enemy(Sprite):
	def __init__(self, x=0, y=0):
		# set member variables
		self.initGenerals(x, y)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y):
		super(Enemy, self).initGenerals(x, y)
		self.moveStep = 0
		self.prevRect = Rect((x, y), (32, 24))
		self.rect = self.prevRect
		# default values
		self.speed = 2
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 5
		self.imgFrame = 2

	def initProperties(self):
		self.prefix = '__dummy'



	def draw(self):
		ImagePack.drawBottomCenter(self.rect, self.imgList[''], self.step, self.imgFrame)



	def update(self):
		super(Enemy, self).update()

		# randomly choose directions
		if self.moveStep > 0:
			self.moveStep -= 1
		else:
			self.moveStep = random.randrange(30, 301)
			self.movingXspeed = random.randrange(0, 3) - 1

		# vertical moving (jump, gravity)
		if self.status == statusEnum.JUMPED:
			self.status = statusEnum.AIR
			self.fallingYspeed += self.gravity
		elif self.status == statusEnum.AIR:
			# on air
			#if self.rect.bottom < self.screen.height:
			self.fallingYspeed += self.gravity
		elif self.status == statusEnum.GROUND:
			do_nothing = 0

	def updatePostorder(self):
		super(Enemy, self).updatePostorder()
		# when it doesn't stand on any terrains, go into falling status
		if self.collideTerrain[0] is None:
			self.status = statusEnum.AIR



# minislime:
class Enemy_Minislime(Enemy):
	def initProperties(self):
		self.speed = 1
		self.prefix = 'e_minislime'
		self.imgName.append('')
		self.imgFrame = 10