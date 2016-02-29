import math
import random
#import copy

from Sprite import *
from DamageText import *
from ImagePack import *

import pygame
from pygame.locals import *



# enemy: superclass
class Enemy(Sprite):
	def __init__(self, x=0, y=0, name='__dummy'):
		# set member variables
		self.initGenerals(x, y, name)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y, name):
		super(Enemy, self).initGenerals(x, y, name)
		# coordinate and mask(vulnerable area) size
		self.rect = Rect((x, y), (32, 32)) # width, height default values

		# general variables
		self.moveStep = 0
		self.knockback = False # is it knock-back status?
		self.dead = False
		self.expireStep = 60
		self.hit = False # is it hit?
		self.imgName.append('walk')
		self.imgName.append('die')

		# default values
		self.eid = 0 # enemy id
		self.lv = 1
		self.sort = 'unknown'
		self.type = []
		self.boss = False # is a boss enemy?
		self.move = 0 # 0: normal, 1: flying, 2: swimming
		self.maxHP = self.HP = 1
		self.maxMP = self.MP = 0
		self.ATK = 1 # attack point
		self.DEF = 0 # defense point
		self.MATK = 0 # magic attack point
		self.MDEF = 0 # magic defense point
		self.SPD = 2
		self.JMP = 0 # jump power(when it is 0, it doesn't fall from cliff, otherwise generally 5)
		self.KB = 0 # minimal damage that knock backs this enemy
		self.EXP = 1 # experience point drops
		self.GOLD = 1 # gold drops
		self.drop = [] # item drops
		self.pskill = [] # passive skill
		self.askill = [] # active skill
		self.imgFrame = 10 # animation speed (the number of same frames)

		# default values that will be barely changed
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.kbFrame = 30 # knock back frame
		self.deathFrame = 10

	def initDependencies(self, name=''):
		super(Enemy, self).initDependencies('e_')

	def stampCopy(self):
		result = Enemy(self.rect.x, self.rect.y, self.name)
		result.eid = self.eid
		result.lv = self.lv
		result.sort = self.sort
		result.type = self.type[:]
		result.boss = self.boss
		result.move = self.move
		result.maxHP = result.HP = self.maxHP
		result.maxMP = result.MP = self.maxMP
		result.ATK = self.ATK
		result.DEF = self.DEF
		result.MATK = self.MATK
		result.MDEF = self.MDEF
		result.SPD = self.SPD
		result.JMP = self.JMP
		result.KB = self.KB
		result.EXP = self.EXP
		result.GOLD = self.GOLD
		result.drop = self.drop[:]
		result.pskill = self.pskill[:]
		result.askill = self.askill[:]
		result.imgFrame = self.imgFrame
		result.gravity = self.gravity
		result.kbFrame = self.kbFrame
		result.deathFrame = self.deathFrame
		result.imgName = self.imgName[:]
		result.imgList = self.imgList.copy()
		return result



	def draw(self):
		if not self.dead:
			if not self.knockback:
				imgStr = 'walk' if self.xspeed != 0 else ''
				ImagePack.drawBottomCenterFlip(self.rect, self.imgList[imgStr], self.xflip, False, self.step, self.imgFrame)
			else:
				ImagePack.drawBottomCenterFlip(self.rect, self.imgList['die'], self.xflip, False, 0, 1)

			# draw health bar if it is attacked
			if self.hit:
				# border
				borderRect = Rect((0, self.rect.bottom+5), (52, 7))
				borderRect.centerx = self.rect.centerx
				pygame.draw.rect(ImagePack.screen.canvas, 0, borderRect)
				# inner bar
				bw = float(self.HP) / self.maxHP * 50
				if bw > 0:
					bgRect = borderRect.copy()
					bgRect.x += 1
					bgRect.w = bw
					bgRect.y += 1
					bgRect.h -= 2
					coffset = float(self.HP) / self.maxHP * 255 # 255 * (1 - (float(self.HP)/self.maxHP)**2)
					pygame.draw.rect(ImagePack.screen.canvas, (255-coffset, coffset, 0), bgRect)

		# death: getting transparent
		else:
			alpha = 1.0 - 1.0 * self.step / self.expireStep
			ImagePack.drawBottomCenterAlphaFlip(self.rect, self.imgList['die'], alpha, self.xflip, False, self.step, self.deathFrame)



	def update(self, player, attacksAlly, attacksEnemy, damageText):
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
			self.updateAttacked(attacksAlly, damageText)

	def updateAttacked(self, attacksAlly, damageText):
		if self.dead:
			return

		for aa in attacksAlly:
			if self.rect.colliderect(aa.rect) and aa.setTarget(self):
				# set attacked flag
				self.hit = True
				# reduce HP
				self.HP -= aa.ATK
				# make damage text
				damageText.append(DamageText(self.rect.centerx, self.rect.y, aa.ATK, DamageText.colorEnemy))

				# dead!!
				if self.HP <= 0:
					self.HP = 0
					self.knockback = False
					self.dead = True
					self.step = 0
					self.xspeed = 0
				# knockback
				elif aa.ATK >= self.KB:
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