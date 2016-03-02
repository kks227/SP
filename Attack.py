import random
import weakref

from Sprite import *
from ImagePack import *

import pygame
from pygame.locals import *



# enemy: superclass
class Attack(Sprite):
	def __init__(self, parent, x, y, ATK=1, w=30, h=30, target=1, ready=1, act=1):
		# set member variables
		self.initGenerals(parent, x, y, ATK, w, h, target, ready, act)
		self.initProperties(x, y)
		self.initDependencies()

	def initGenerals(self, parent, x, y, ATK, w, h, target, ready, act):
		super(Attack, self).initGenerals(x, y, '__rect')
		self.rect.size = (w, h)
		self.parent = parent # whom makes this attack
		self.ready = ready # ready frames
		self.act = act # active frames
		self.active = False # status that gives damage
		self.expire = False
		self.remainFrame = self.ready
		self.target = []
		# default values
		self.ATK = ATK
		self.imgFrame = 1 # if imgFrame=0, it doesn't draw
		self.targetNum = target # maximum target
		self.ally = True
		# default values that will be barely changed

	def initProperties(self, x, y):
		pass



	def draw(self):
		if self.imgFrame > 0:
			ImagePack.draw(DrawOption(self.rect, self.imgList[''], self.step, self.imgFrame))



	def update(self, oppos, damageText):
		super(Attack, self).update()
		self.checkCollision(oppos, damageText)

	def checkCollision(self, oppos, damageText):
		# not active
		if not self.active or self.expire:
			return

		# ally's attack: opposite is an enemy
		if self.ally:
			for o in oppos:
				# pass if it is already dead
				if o.dead:
					continue
				# check and target
				if self.rect.colliderect(o.rect) and self.setTarget(o):
					o.setAttacked(self, damageText)

		# enemy's attack: opposite is an ally
		else:
			pass

	def updatePostorder(self):
		super(Attack, self).updatePostorder()
		self.remainFrame -= 1
		if self.remainFrame <= 0:
			if self.active:
				self.expire = True
			else:
				self.remainFrame = self.act
				self.active = True



	# return false when enemy is already targeted
	# otherwise return true and targets enemy
	def setTarget(self, oppo):
		if self.targetNum <= 0:
			return False

		for o in self.target:
			if o() is not None and id(o()) == id(oppo):
				return False

		self.targetNum -= 1
		self.target.append(weakref.ref(oppo))
		return True



# one frame attack
class Attack_Normal(Attack):
	def initProperties(self, x, y):
		self.rect.center = (x, y)
		self.name = '__rect'