from Screen import *
from Player import *
from Enemy import *
from Terrain import *
from ImagePack import *

import pygame
from pygame.locals import *



class GameManager:
	def __init__(self):
		# initial processing
		pygame.init()
		self.screen = Screen(640, 480)
		self.FPS = 60
		self.fpsClock = pygame.time.Clock()

		# global variables
		self.keys = [False, False] # key input check

		# image loading
		self.player = Player_Superbounce(70, 100)

		self.terrains = []
		for x in range(0, 640, 50):
			self.terrains.append(Terrain(x, 450, 't_solid0'))
		self.terrains.append(Terrain(0, 400, 't_solid0'))
		self.terrains.append(Terrain(600, 400, 't_solid0'))
		for x in range(150, 500, 50):
			self.terrains.append(Terrain_Foothold(x, 300, 't_foothold0'))

		self.enemies = []
		self.enemies.append(Enemy_Minislime(400, 100))

		ImagePack.getFiles('__dummy', 'Etc/__dummy')

		ImagePack.getFiles('p_superbounce', 'Players/superbounce', 2)

		ImagePack.getFiles('e_minislime', 'Enemies/minislime')

		ImagePack.getFiles('t___dummy', 'Terrains/__dummy')
		ImagePack.getFiles('t_solid0', 'Terrains/solid0')
		ImagePack.getFiles('t_foothold0', 'Terrains/foothold0')

		ImagePack.setScreen(self.screen)







	def draw(self):
		# draw background (default)
		self.screen.draw()
		# draw player
		self.player.draw()
		# draw blocks
		for obj in self.terrains:
			obj.draw()
		# draw enemies
		for ene in self.enemies:
			ene.draw()

		# draw updating
		pygame.display.update()



	def update(self):
		# FPS setting
		self.fpsClock.tick(self.FPS)

		# preorder update functions
		self.player.updatePreorder()

		for ene in self.enemies:
			ene.updatePreorder()

		# update functions
		self.player.update()

		for ene in self.enemies:
			ene.update()

		for obj in self.terrains:
			obj.update()
			# must be checked horizontally first
			# otherwise player can jump on side of vertical terrains(bug)
			obj.horiCollision(self.player)
			obj.vertiCollision(self.player)
			for ene in self.enemies:
				obj.horiCollision(ene)
				obj.vertiCollision(ene)

		# postorder update functions
		self.player.updatePostorder()

		for ene in self.enemies:
			ene.updatePostorder()