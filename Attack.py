import math
import random
import weakref

from Sprite import *
from ImagePack import *
from Tool import *

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
		self.active = False if ready > 0 else True # status that gives damage
		self.expire = False
		self.remainFrame = self.ready if ready > 0 else act
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

		self.setTargetDirectly(oppo)
		return True

	def setTargetDirectly(self, oppo):
		self.targetNum -= 1
		self.target.append(weakref.ref(oppo))



# one frame attack
class Attack_Normal(Attack):
	def initProperties(self, x, y):
		self.rect.center = (x, y)
		self.name = '__rect'



class Attack_ChainMagic(Attack): # must be ally's
	def initProperties(self, x, y):
		self.rect.center = (x, y)
		# values
		self.maxDist = 200
		self.xflag = False # to right if true, otherwise to left
		# constants
		self.marginWidth = 12
		self.outerWidth = 4
		self.innerWidth = 2
		self.interval = 2
		# color constants
		self.outerColor = (255, 201, 14)
		self.innerColor = (255, 242, 0)
		# variables will be used
		self.intervalFrame = 0
		self.points = [self.rect.center]
		self.scratch = [[], []]

	def draw(self):
		self.drawChainMagic(self.outerWidth, self.outerColor, self.scratch[0], 2)
		self.drawChainMagic(self.innerWidth, self.innerColor, self.scratch[1], 1)

	def drawChainMagic(self, width, color, chain, cWidth):
		# draw lines
		if len(self.points) > 1:
			pygame.draw.lines(ImagePack.screen.canvas, color, False, self.points, width)
		# draw circles
		for p in self.points:
			pygame.draw.circle(ImagePack.screen.canvas, color, p, width*2)
		# draw random scratch lines
		if len(chain) > 1:
			pygame.draw.lines(ImagePack.screen.canvas, color, False, chain, cWidth)

	def update(self, oppos, damageText):
		super(Attack, self).update()
	#	print oppos
		if self.intervalFrame == 0:
			self.intervalFrame = self.interval
			# collision check
			self.checkCollision(oppos, damageText)

			# renew drawings
			for li in range(2):
				self.scratch[li][:] = []
				self.scratch[li].append(self.rect.center)
				for i in range(1, len(self.points)):
					p1 = list(self.points[i-1])
					p2 = list(self.points[i])
					t = 0
					sign = 1
					d = listSub(p2, p1)
					n = listNorm([-d[1], d[0]])
					while True:
						t += random.uniform(0.03, 0.10)
						if t >= 1:
							t = 1
							self.scratch[li].append(p2)
							break

						h = random.randrange(self.outerWidth*1.5, self.marginWidth)
						self.scratch[li].append(listAdd(listAdd(p1, listCoeff(d, t)), listCoeff(n, sign*h)))
						# renew
						sign *= -1

		else:
			self.intervalFrame -= 1

	def checkCollision(self, oppos, damageText):
		# not active or already has full targets
		if not self.active or self.expire or self.target == 0:
			return

		# find nearest and on forward enemy
		p1 = self.points[-1]
		newTarget = None
		minDist = self.maxDist
		for e in oppos:
			# pass if it is already dead
			if e.dead:
				continue
			# pass if it is already targeted 
			conFlag = False
			for t in self.target:
				if t() is not None and id(t()) == id(e):
					conFlag = True
					break
			if conFlag:
				continue

			p2 = e.rect.center
			# pass if it is not on forward
			if (self.xflag and p1[0] >= p2[0]) or (not self.xflag and p1[0] <= p2[0]):
				continue
			dist = math.hypot(p1[0]-p2[0], p1[1]-p2[1])
			if dist < minDist:
				minDist = dist
				newTarget = e

		# nearest enemy as set target
		if newTarget is not None:
			self.setTargetDirectly(newTarget)
			newTarget.setAttacked(self, damageText)
			self.points.append(newTarget.rect.center)