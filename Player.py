from Sprite import *
from Attack import *
from ImagePack import *

import pygame
from pygame.locals import *



# player: superclass
class Player(Sprite):
	def __init__(self, x=0, y=0):
		# set member variables
		self.initGenerals(x, y)
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, x, y):
		super(Player, self).initGenerals(x, y)
		self.rect = Rect((x, y), (32, 24))
		self.actFrame = 0
		# default values
		self.speed = 5
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 10

	def initProperties(self):
		self.prefix = '__dummy'



	def draw(self):
		ImagePack.drawBottomCenter(self.rect, self.imgList[''], self.step, 4)



	def update(self, attacksAlly, attacksEnemy):
		super(Player, self).update()

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

	def updateKeyEvent(self, attacksAlly, attacksEnemy):
		# get pressed keys information
		keys = pygame.key.get_pressed()

		# if both keys of direction are released, set moving speed as 0
		if not keys[K_LEFT] and not keys[K_RIGHT]:
			self.xspeed = 0

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
					self.xspeed = -1
				# move to right
				elif event.key == K_RIGHT:
					self.xspeed = 1
				# jump
				elif event.key == K_z:
					# only possible when it is on ground
					if self.status == statusEnum.GROUND:
						self.status = statusEnum.JUMPED
						self.yspeed = -self.jumpPower
				# attack
				elif event.key == K_a:
					attacksAlly.append(Attack_Normal(self, self.rect.x, self.rect.y))
			# key up
			if event.type == pygame.KEYUP:
				# stop moving to left
				if event.key == K_LEFT:
					if keys[K_RIGHT]:
						self.xspeed = 1
					else:
						self.xspeed = 0
				# stop moving to right
				elif event.key == K_RIGHT:
					if keys[K_LEFT]:
						self.xspeed = -1
					else:
						self.xspeed = 0

	def updatePostorder(self):
		super(Player, self).updatePostorder()
		# when it doesn't stand on any terrains, go into falling status
		if self.collideTerrain[0] is None:
			self.status = statusEnum.AIR



# superbounce:
class Player_Superbounce(Player):
	def initProperties(self):
		# variables
		self.speed = 5
		self.gravity = 0.3 # accelerating vertical speed by gravity
		self.jumpPower = 10
		self.prefix = 'p_superbounce'