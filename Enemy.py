import math
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
		self.knockback = False
		self.dead = False
		self.expireStep = 60
		self.imgName.append('walk')
		self.imgName.append('die')

		# default values
		self.HP = 1
		self.speed = 2
		self.kbDamage = 0
		# default values that will be barely changed
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 5
		self.kbFrame = 30 # knock back frame
		self.imgFrame = 10
		self.deathFrame = 10

	def initProperties(self):
		self.prefix = '__dummy'

	def initDependencies(self):
		super(Enemy, self).initDependencies()
		self.maxHP = self.HP



	def draw(self):
		if not self.dead:
			if not self.knockback:
				imgStr = 'walk' if self.xspeed != 0 else ''
				ImagePack.drawBottomCenterFlip(self.rect, self.imgList[imgStr], self.xflip, False, self.step, self.imgFrame)
			else:
				ImagePack.drawBottomCenterFlip(self.rect, self.imgList['die'], self.xflip, False, 0, 1)
		else:
			alpha = 1.0 - 1.0 * self.step / self.expireStep
			ImagePack.drawBottomCenterAlphaFlip(self.rect, self.imgList['die'], alpha, self.xflip, False, self.step, self.deathFrame)



	def update(self, player, attacksAlly, attacksEnemy):
		super(Enemy, self).update()

		# knockback status
		if self.knockback:
			# end of status
			if self.step >= self.kbFrame:
				self.knockback = False
				self.step = 0
				self.moveStep = 0
			# knockback
			else:
				kbSign = -1 if self.xflip else 1
				kbAbs = round(math.pow(0.813, self.step)*7.5)
				if kbAbs < 0:
					kbAbs = 0
			#	print kbAbs, self.xspeed
				self.rect.x += kbSign * kbAbs
		# randomly choose directions
		elif self.moveStep > 0:
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
		if self.dead:
			return

		for aa in attacksAlly:
			if self.rect.colliderect(aa.rect) and aa.setTarget(self):
				# reduce HP
				self.HP -= aa.ATK
				# dead!!
				if self.HP <= 0:
					self.HP = 0
					self.knockback = False
					self.dead = True
					self.step = 0
					self.xspeed = 0
				# knockback
				elif aa.ATK >= self.kbDamage:
					self.knockback = True
					self.step = 0
					self.xspeed = 0
					self.moveStep = 0
					self.xflip = True if self.rect.centerx < aa.rect.centerx else False

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
		self.HP = 5
		self.speed = 1
		self.prefix = 'e_minislime'
		self.imgFrame = 10
		self.rect.size = (25, 19)