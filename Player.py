import random
from collections import defaultdict

from Sprite import *
from Attack import *
from DamageText import *
from ImagePack import *

import pygame
from pygame.locals import *



# player: superclass
class Player(Sprite):
	invFrame = 60

	def __init__(self, x=0, y=0, name='__dummy'):
		# set member variables
		self.initGenerals(x, y, name)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y, name='__dummy'):
		super(Player, self).initGenerals(x, y, name)
		self.actFrame = 0
		self.imgName.append('face')
		self.facePivot = defaultdict(list)
		self.face = 0
		self.faceFrame = 0
		self.invFrame = 0
		# default values
		self.speed = 5
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 10

	def initDependencies(self, name=''):
		super(Player, self).initDependencies('p_')
		# set default face pivot tuples
		for key in self.imgName:
			if key not in self.facePivot:
				self.facePivot[key] = (0, 0)
		self.faceSize = self.imgList['face'][0].get_rect().size



	def draw(self):
		alpha = 1 if self.invFrame%4 < 2 else 0.5

		# draw body
		do = DrawOption(self.rect, self.imgList[''], self.step, 4)
		do.pivot = 2
		do.xflip = self.xflip
		do.alpha = alpha
		ImagePack.draw(do)

		# draw face
		faceRect = self.rect.copy()
		faceRect.size = self.faceSize
		xsign = -1 if self.xflip else 1
		faceRect.center = (self.rect.center[0]+xsign*self.facePivot[''][0], self.rect.center[1]+self.facePivot[''][1])
		do = DrawOption(faceRect, self.imgList['face'], self.face)
		do.pivot = 1
		do.xflip = self.xflip
		do.alpha = alpha
		ImagePack.draw(do)



	def update(self, enemies, attacksAlly, attacksEnemy, damageText):
		super(Player, self).update()

		if self.actFrame == 0:
			self.updateKeyEvent(attacksAlly, attacksEnemy)

		# player vertical moving (jump, gravity)
		if self.status == statusEnum.JUMPED:
			self.status = statusEnum.AIR
			self.yspeed += self.gravity
		elif self.status == statusEnum.AIR:
			# on air
			#if self.rect.bottom < self.screen.height:
			self.yspeed += self.gravity
		elif self.status == statusEnum.GROUND:
			do_nothing = 0

		if self.actFrame > 0:
			self.actFrame -= 1
		if self.faceFrame > 0:
			self.faceFrame -= 1
			if self.faceFrame == 0:
				self.face = 0
		if self.invFrame > 0:
			self.invFrame -= 1

	def updateKeyEvent(self, attacksAlly, attacksEnemy):
		# get pressed keys information
		keys = pygame.key.get_pressed()

		# if both keys of direction are released, set moving speed as 0
		if not keys[K_LEFT] and not keys[K_RIGHT]:
			self.xspeed = 0
		elif keys[K_LEFT] and self.xspeed == 0:
			self.xflip = False
			self.xspeed = -self.speed
		elif keys[K_RIGHT] and self.xspeed == 0:
			self.xflip = True
			self.xspeed = self.speed

		# event polling
		for event in pygame.event.get():
			# quit
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			# key down
			if event.type == pygame.KEYDOWN:
				# move to left
				if event.key == K_LEFT:
					self.xflip = False
					self.xspeed = -self.speed
				# move to right
				elif event.key == K_RIGHT:
					self.xflip = True
					self.xspeed = self.speed
				# jump
				elif event.key == K_z:
					# only possible when it is on ground
					if self.status == statusEnum.GROUND:
						self.status = statusEnum.JUMPED
						self.yspeed = -self.jumpPower
				# attack
				elif event.key == K_a:
					self.actFrame = 10
					self.xspeed = 0
					x = self.rect.centerx + (1 if self.xflip else -1)*20
					y = self.rect.centery
					attacksAlly.append(Attack_Normal(self, x, y, random.randrange(1, 4), 60, 30, 1, 5, 5))
				# test: special attack
				elif event.key == K_x:
					self.actFrame = 40
					self.xspeed = 0
					x = self.rect.centerx + (1 if self.xflip else -1)*20
					y = self.rect.centery
					newAttack = Attack_ChainMagic(self, x, y, 5000, 30, 30, 6, 0, 40)
					newAttack.xflag = self.xflip
					attacksAlly.append(newAttack)
			# key up
			if event.type == pygame.KEYUP:
				# stop moving to left
				if event.key == K_LEFT:
					if keys[K_RIGHT]:
						self.xflip = True
						self.xspeed = self.speed
					else:
						self.xspeed = 0
				# stop moving to right
				elif event.key == K_RIGHT:
					if keys[K_LEFT]:
						self.xflip = False
						self.xspeed = -self.speed
					else:
						self.xspeed = 0

	def updatePostorder(self):
		super(Player, self).updatePostorder()
		# when it doesn't stand on any terrains, go into falling status
		if self.collideTerrain[0] is None:
			self.status = statusEnum.AIR



	def setAttackedByEnemy(self, enemy, damageText):
		# set attacked
		self.invFrame = Player.invFrame
		self.face = 1
		self.faceFrame = Player.invFrame
		# reduce HP
	#	self.HP -= aa.ATK
		# make damage text
		damageText.append(DamageText(self.rect.centerx, self.rect.y, enemy.ATK, DamageText.colorAlly))



# superbounce:
class Player_Superbounce(Player):
	def initProperties(self):
		# variables
		self.speed = 5
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 10
		self.name = 'superbounce'
		self.rect.size = (32, 24)
		self.facePivot[''] = (-3, 4)