from ImagePack import *

import pygame
from pygame.locals import *



class DamageText:
	# general colors
	colorEnemy = (35, 56, 151)
	colorAlly = (132, 62, 57)
	colorRecovery = (181, 230, 29)

	# other static values
	img = []
	remain = 60
	tw = 18
	tw1 = 14
	th = 24
	vib = 2



	@staticmethod
	def loadImages():
		for i in range(10):
			DamageText.img.append(ImagePack.img['text_'+str(i)])



	def __init__(self, cx, cy, val=1, color=(255, 255, 255)):
		self.val = int(val)
		self.color = color
		self.remain = DamageText.remain

		self.w = 0
		while True:
			self.w += DamageText.tw1 if val%10 == 1 else DamageText.tw
			self.w -= DamageText.vib
			val /= 10
			if val <= 0:
				break
		self.w += DamageText.vib
		self.h = DamageText.th + DamageText.vib
		self.x = cx - self.w/2
		self.y = cy - self.h/2



	def draw(self):
		if self.remain > 0:
			alpha = float(self.remain) / DamageText.remain
			x = self.x
			y = self.y
			flag = False
			val = str(self.val)
			for c in val:
				d = int(c)
				w = DamageText.tw1 if d==1 else DamageText.tw
				h = DamageText.th
				do = DrawOption(Rect((x, y), (w, h)), DamageText.img[d])
				do.alpha = alpha
				do.blend = self.color
				ImagePack.draw(do)
				x += w - DamageText.vib
				y += (-1 if flag else 1) * DamageText.vib
				flag = not flag



	def update(self):
		if self.remain > 0:
			self.remain -= 1
			self.y -= self.remain/20