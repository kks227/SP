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
	def draw(option):
		# animation speed
		if option.fspeed > 0:
			option.frame = (option.frame + option.fspeed - 1) / option.fspeed
		if option.loop:
			option.frame %= len(option.imgList)
		else:
			option.frame = min(option.frame, len(option.imgList)-1)

		img = option.imgList[option.frame].copy()

		# draw bottom center
		if option.bottomCenter:
			newRect = option.imgList[0].get_rect()
			newRect.bottom = option.rect.bottom
			newRect.centerx = option.rect.centerx
			option.rect = newRect
		# alpha
		if option.alpha < 1:
			img.fill((255, 255, 255, int(option.alpha*255)), None, pygame.BLEND_RGBA_MULT)
		# blend
		if option.blend is not None:
		#	img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
			img.fill(option.blend[0:3]+(0,), None, pygame.BLEND_RGBA_ADD)
		# flip
		if option.xflip or option.yflip:
			img = pygame.transform.flip(img, option.xflip, option.yflip)
		# scale
		if option.scale is not None:
			img = pygame.transform.scale(img, option.scale)
		# rotate
		if option.rotate != 0:
			img = pygame.transform.rotate(img, option.rotate)

		# finally blit
		ImagePack.screen.canvas.blit(img, option.rect.topleft)



class DrawOption:
	#(rect, imgList, alpha, xflip, yflip, scale, rotate, blend, frame, fspeed):
	def __init__(self, rect, imgList, frame=0, fspeed=0):
		self.rect = rect # essential value: coordinate
		self.imgList = imgList # essential value: image list
		self.bottomCenter = False # set balance as bottom center
		self.loop = True # does it loop?
		self.alpha = 1 # opacity(0: fully transparent, 1: fully opaque)
		self.xflip = False
		self.yflip = False
		self.scale = None # scale Rect
		self.rotate = 0
		self.blend = None
		self.frame = frame # current step value
		self.fspeed = fspeed # animation speed