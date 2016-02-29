from collections import defaultdict

import pygame
from pygame.locals import *



# terrain: superclass
class ImagePack:
	img = defaultdict(list)
	screen = None
	commonPath = "Resources/Images/"

	# get a list of filenames, then make a list of image and store it statically
	@staticmethod
	def getFiles(imgName, fileName, cnt=0):
		imgList = []
		if cnt == 0:
			imgList.append(pygame.image.load(ImagePack.commonPath + fileName + ".png").convert_alpha())
		else:
			for i in range(cnt):
				imgList.append(pygame.image.load(ImagePack.commonPath + fileName + str(i+1) + ".png").convert_alpha())
		ImagePack.img[imgName] = imgList

	# set screen variable statically
	@staticmethod
	def setScreen(screen):
		ImagePack.screen = screen



	# draw funntions
	@staticmethod
	def drawGeneral(rect, imgList, alpha, xflip, yflip, scale, rotate, blend, frame, fspeed):
		# animation speed
		if fspeed > 0:
			frame = (frame + fspeed - 1) / fspeed
		frame %= len(imgList)

		img = imgList[frame].copy()

		# alpha
		if alpha < 1:
			img.fill((255, 255, 255, int(alpha*255)), None, pygame.BLEND_RGBA_MULT)
		# blend
		if blend is not None:
		#	img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
			img.fill(blend[0:3]+(0,), None, pygame.BLEND_RGBA_ADD)
		# flip
		img = pygame.transform.flip(img, xflip, yflip)
		# scale
		if scale is not None:
			img = pygame.transform.scale(img, scale)
		# rotate
		if rotate != 0:
			img = pygame.transform.rotate(img, rotate)

		# finally blit
		ImagePack.screen.canvas.blit(img, rect.topleft)

	@staticmethod
	def draw(rect, imgList, frame=0, fspeed=0):
		ImagePack.drawGeneral(rect, imgList, 1, False, False, None, 0, None, frame, fspeed)

	@staticmethod
	def drawBottomCenter(rect, imgList, frame=0, fspeed=0):
		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx
		ImagePack.drawGeneral(drawRect, imgList, 1, False, False, None, 0, None, frame, fspeed)

	@staticmethod
	def drawAlpha(rect, imgList, alpha, frame=0, fspeed=0):
		ImagePack.drawGeneral(rect, imgList, alpha, False, False, None, 0, None, frame, fspeed)

	@staticmethod
	def drawBottomCenterAlpha(rect, imgList, alpha, frame=0, fspeed=0):
		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx
		ImagePack.drawGeneral(drawRect, imgList, alpha, False, False, None, 0, None, frame, fspeed)

	@staticmethod
	def drawFlip(rect, imgList, xflip, yflip, frame=0, fspeed=0):
		ImagePack.drawGeneral(rect, imgList, 1, xflip, yflip, None, 0, None, frame, fspeed)

	@staticmethod
	def drawBottomCenterFlip(rect, imgList, xflip, yflip, frame=0, fspeed=0):
		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx
		ImagePack.drawGeneral(drawRect, imgList, 1, xflip, yflip, None, 0, None, frame, fspeed)

	@staticmethod
	def drawAlphaScale(rect, imgList, alpha, xflip, yflip, frame=0, fspeed=0):
		ImagePack.drawGeneral(rect, imgList, alpha, xflip, yflip, None, 0, None, frame, fspeed)

	@staticmethod
	def drawBottomCenterAlphaFlip(rect, imgList, alpha, xflip, yflip, frame=0, fspeed=0):
		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx
		ImagePack.drawGeneral(drawRect, imgList, alpha, xflip, yflip, None, 0, None, frame, fspeed)

	@staticmethod
	def drawAlphaBlend(rect, imgList, alpha, blend, frame=0, fspeed=0):
		ImagePack.drawGeneral(rect, imgList, alpha, False, False, None, 0, blend, frame, fspeed)

	@staticmethod
	def drawBottomCenterAlphaBlend(rect, imgList, alpha, blend, frame=0, fspeed=0):
		drawRect = imgList[0].get_rect()
		drawRect.bottom = rect.bottom
		drawRect.centerx = rect.centerx
		ImagePack.drawGeneral(drawRect, imgList, alpha, False, False, None, 0, blend, frame, fspeed)