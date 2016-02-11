from collections import defaultdict

import pygame
from pygame.locals import *



# terrain: superclass
class ImagePack:
	imgs = defaultdict(list)
	screen = None
	commonPath = "Resources/Images/"

	# get a list of filenames, then make a list of image and store it statically
	@staticmethod
	def getFiles(imgName, subPath, fileNames):
		imgList = []
		for fname in fileNames:
			imgList.append(pygame.image.load(ImagePack.commonPath + subPath + fname + ".png"))
		ImagePack.imgs[imgName] = imgList

	# set screen variable statically
	@staticmethod
	def setScreen(screen):
		ImagePack.screen = screen

	@staticmethod
	def draw(rect, imgList, frame=0, fspeed=0):
		if fspeed > 0:
			frame = (frame + fspeed - 1) / fspeed
		frame %= len(ImagePack.imgs[imgName])
		ImagePack.screen.canvas.blit(ImagePack.imgs[imgName][frame], rect.topleft)

	@staticmethod
	def drawBottomCenter(rect, imgList, frame=0, fspeed=0):
		drawRect = ImagePack.imgs[imgName][0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx

		if fspeed > 0:
			frame = (frame + fspeed - 1) / fspeed
		frame %= len(ImagePack.imgs[imgName])
		ImagePack.screen.canvas.blit(ImagePack.imgs[imgName][frame], drawRect.topleft)