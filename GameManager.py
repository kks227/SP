import random

from Screen import *
from Player import *
from Enemy import *
from Terrain import *
from Attack import *
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
		self.step = 0

		# global variables
		self.keys = [False, False] # key input check



		# image loading
		ImagePack.getFiles('__dummy', 'Etc/__dummy')
		ImagePack.getFiles('__rect', 'Etc/__rect')

		ImagePack.getFiles('p_superbounce', 'Players/superbounce', 2)

		ImagePack.getFiles('e_minislime', 'Enemies/minislime', 9)
		ImagePack.getFiles('e_minislime_walk', 'Enemies/minislime_walk', 8)
		ImagePack.getFiles('e_minislime_die', 'Enemies/minislime_die', 6)

		ImagePack.getFiles('t___dummy', 'Terrains/__dummy')
		ImagePack.getFiles('t_solid0', 'Terrains/solid0')
		ImagePack.getFiles('t_foothold0', 'Terrains/foothold0')

		ImagePack.setScreen(self.screen)



		# add objects
		self.player = Player_Superbounce(70, 100)

		self.terrains = []
		for x in range(0, 640, 50):
			self.terrains.append(Terrain(x, 450, 't_solid0'))
		self.terrains.append(Terrain(0, 400, 't_solid0'))
		self.terrains.append(Terrain(600, 400, 't_solid0'))
		for x in range(150, 500, 50):
			self.terrains.append(Terrain_Foothold(x, 300, 't_foothold0'))

		self.enemies = []
	#	self.enemies.append(Enemy_Minislime(400, 100))

		self.attacksAlly = []
		self.attacksEnemy = []



	def draw(self):
		# draw background (default)
		self.screen.draw()
		# draw player
		self.player.draw()
		# draw blocks
		for obj in self.terrains:
			obj.draw()
		# draw enemies
		for enemy in self.enemies:
			enemy.draw()
		# draw attacks
		for aa in self.attacksAlly:
			aa.draw()

		# draw updating
		pygame.display.update()



	def update(self):
		# FPS setting
		self.fpsClock.tick(self.FPS)

		# preorder update functions
		self.player.updatePreorder()

		for enemy in self.enemies:
			enemy.updatePreorder()

		for atkA in self.attacksAlly:
			atkA.updatePreorder()
		for atkE in self.attacksEnemy:
			atkE.updatePreorder()

		# update functions
		self.player.update(self.attacksAlly, self.attacksEnemy)

		for enemy in self.enemies:
			enemy.update(self.attacksAlly, self.attacksEnemy)

		for obj in self.terrains:
			obj.update()
			# must be checked horizontally first
			# otherwise player can jump on side of vertical terrains(bug)
			obj.horiCollision(self.player)
			obj.vertiCollision(self.player)
			for ene in self.enemies:
				obj.horiCollision(ene)
				obj.vertiCollision(ene)

		# update attacks
		for atkA in self.attacksAlly:
			atkA.update()
		for atkE in self.attacksEnemy:
			atkE.update()

		# postorder update functions
		self.player.updatePostorder()

		for enemy in self.enemies:
			enemy.updatePostorder()

		for atkA in self.attacksAlly:
			atkA.updatePostorder()
		for atkE in self.attacksEnemy:
			atkE.updatePostorder()

		self.enemies[:] = [enemy for enemy in self.enemies if not enemy.isExpired()]
		self.attacksAlly[:] = [atkA for atkA in self.attacksAlly if not atkA.expire]
		self.attacksEnemy[:] = [atkE for atkE in self.attacksEnemy if not atkE.expire]



		if self.step % 60 == 0 and len(self.enemies) < 10:
			self.enemies.append(Enemy_Minislime(random.randrange(200, 400), 100))



		self.step += 1

	#	print len(self.attacksAlly)