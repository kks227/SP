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
	def getFiles(imgName, fileName, cnt=0):
		imgList = []
		if cnt == 0:
			imgList.append(pygame.image.load(ImagePack.commonPath + fileName + ".png"))
		else:
			for i in range(cnt):
				imgList.append(pygame.image.load(ImagePack.commonPath + fileName + str(i) + ".png"))
		ImagePack.imgs[imgName] = imgList

	# set screen variable statically
	@staticmethod
	def setScreen(screen):
		ImagePack.screen = screen

	@staticmethod
	def draw(rect, imgName, frame=0, fspeed=0):
		imgList = ImagePack.imgs[imgName]
		if fspeed > 0:
			frame = (frame + fspeed - 1) / fspeed
		frame %= len(imgList)
		ImagePack.screen.canvas.blit(imgList[frame], rect.topleft)

	@staticmethod
	def drawBottomCenter(rect, imgName, frame=0, fspeed=0):
		imgList = ImagePack.imgs[imgName]

		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx

		if fspeed > 0:
			frame = (frame + fspeed - 1) / fspeed
		frame %= len(imgList)
		ImagePack.screen.canvas.blit(imgList[frame], drawRect.topleft)