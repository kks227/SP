from Sprite import *
from ImagePack import *

import pygame
from pygame.locals import *



# terrain: superclass
class Terrain:
	def __init__(self, x, y, imgName='t___dummy'):
		self.imgList = ImagePack.img[imgName]
		self.rect = Rect((x, y), (48, 48))
		# set property member variables
		self.initProperties()
		self.prevRect = self.rect

	def initProperties(self):
		# up, down, left, right
		self.block = [True]*4



	def draw(self):
		ImagePack.draw(self.rect, self.imgList)



	def update(self):
		self.prevRect = self.rect.copy()

	def vertiCollision(self, obj):
		# persist standing on ground
		if self.block[0] and obj.status == statusEnum.GROUND and self.rect.colliderect(obj.rect.move(0, 1)):
			obj.collideTerrain[0] = self
		# collision checking
		if self.rect.colliderect(obj.rect) and not self.prevRect.colliderect(obj.prevRect):
			# up: landing
			if self.block[0] and obj.status == statusEnum.AIR and obj.prevRect.bottom <= self.prevRect.top:
				obj.status = statusEnum.GROUND
				obj.rect.bottom = self.rect.top
				obj.yspeed = 0
				obj.collideTerrain[0] = self
			# down
			if self.block[1] and obj.prevRect.top >= self.prevRect.bottom:
				obj.rect.top = self.rect.bottom
				obj.yspeed *= -1
				obj.collideTerrain[1] = self

	def horiCollision(self, obj):
		# collision checking
		if self.rect.colliderect(obj.rect) and not self.prevRect.colliderect(obj.prevRect):
			# left
			if self.block[2] and obj.prevRect.right <= self.prevRect.left:
				obj.rect.right = self.rect.left
				obj.collideTerrain[2] = self
			# right
			if self.block[3] and obj.prevRect.left >= self.prevRect.right:
				obj.rect.left = self.rect.right
				obj.collideTerrain[3] = self



# solid: not passable on every side
class Terrain_Solid(Terrain):
	def initProperties(self):
		# up, down, left, right
		self.block = [True]*4

# foothold: only passable on upward
class Terrain_Foothold(Terrain):
	def initProperties(self):
		# up, down, left, right
		self.block = [True, False, False, False]