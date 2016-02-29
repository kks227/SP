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
		self.initProperties()
		self.initDependencies()

	def initGenerals(self, parent, x, y, ATK, w, h, target, ready, act):
		super(Attack, self).initGenerals(x, y)
		self.rect = Rect((x, y), (w, h))
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
		self.prefix = '__rect'
		# default values that will be barely changed

	def initProperties(self):
		pass



	def draw(self):
		if self.imgFrame > 0:
			ImagePack.draw(self.rect, self.imgList[''], self.step, self.imgFrame)



	def update(self):
		super(Attack, self).update()

	def updatePostorder(self):
		super(Attack, self).updatePostorder()
		self.remainFrame -= 1
		if self.remainFrame <= 0:
			if self.active:
				self.expire = True
			else:
				self.remainFrame = self.act
				self.active = True



	def setTarget(self, enemy):
		if self.targetNum <= 0:
			return False

		for e in self.target:
			if e() is not None and id(e()) == id(enemy):
				return False

		self.targetNum -= 1
		self.target.append(weakref.ref(enemy))
		return True



# one frame attack
class Attack_Normal(Attack):
	def initProperties(self):
		self.prefix = '__rect'