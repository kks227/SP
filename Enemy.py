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
		self.rect = Rect((x, y), (32, 24))
		self.dead = False
		self.expireStep = 60
		self.imgName.append('walk')
		self.imgName.append('die')
		# default values
		self.speed = 2
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 5
		self.imgFrame = 10
		self.deathFrame = 10

	def initProperties(self):
		self.prefix = '__dummy'



	def draw(self):
		if not self.dead:
			imgStr = 'walk' if self.xspeed != 0 else ''
			ImagePack.drawBottomCenterFlip(self.rect, self.imgList[imgStr], self.xflip, False, self.step, self.imgFrame)
		else:
			alpha = 1.0 - 1.0 * self.step / self.expireStep
			ImagePack.drawBottomCenterAlphaFlip(self.rect, self.imgList['die'], alpha, self.xflip, False, self.step, self.deathFrame)



	def update(self, attacksAlly, attacksEnemy):
		super(Enemy, self).update()

		# randomly choose directions
		if self.moveStep > 0:
			self.moveStep -= 1
		elif not self.dead:
			self.moveStep = random.randrange(30, 301)
			self.xspeed = random.randrange(0, 3) - 1
			if self.xspeed == 1:
				self.xflip = True
			elif self.xspeed == -1:
				self.xflip = False

		# vertical moving (jump, gravity)
		if self.status == statusEnum.JUMPED:
			self.status = statusEnum.AIR
			self.yspeed += self.gravity
		elif self.status == statusEnum.AIR:
			# on air
			#if self.rect.bottom < self.screen.height:
			self.yspeed += self.gravity
		elif self.status == statusEnum.GROUND:
			pass

		if not self.dead:
			self.updateAttacked(attacksAlly)

	def updateAttacked(self, attacksAlly):
		if not self.dead:
			for aa in attacksAlly:
				if self.rect.colliderect(aa.rect) and aa.setTarget(self):
					self.dead = True
					self.xspeed = 0
					self.step = 0

	def updatePostorder(self):
		super(Enemy, self).updatePostorder()
		# when it doesn't stand on any terrains, go into falling status
		if self.collideTerrain[0] is None:
			self.status = statusEnum.AIR



	def isExpired(self):
		return self.dead and self.step >= self.expireStep



# minislime:
class Enemy_Minislime(Enemy):
	def initProperties(self):
		self.speed = 1
		self.prefix = 'e_minislime'
		self.imgFrame = 10
		self.rect.size = (25, 19)