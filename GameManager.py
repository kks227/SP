import random
from collections import defaultdict
from xml.etree.ElementTree import parse

from Screen import *
from Player import *
from Enemy import *
from Terrain import *
from Attack import *
from DamageText import *
from ImagePack import *

import pygame
from pygame.locals import *



class GameManager:
	def __init__(self):
		# initial processing
		pygame.init()
		self.screen = Screen(640, 480)
		ImagePack.setScreen(self.screen)
		self.FPS = 60
		self.fpsClock = pygame.time.Clock()
		self.step = 0

		# global variables
		self.keys = [False, False] # key input check



		# image loading
		ImagePack.getFiles('__dummy', 'Etc/__dummy')
		ImagePack.getFiles('__rect', 'Etc/__rect')

		for i in range(10):
			ImagePack.getFiles('text_'+str(i), 'Text/text_'+str(i))

		ImagePack.getFiles('p_superbounce', 'Players/superbounce', 2)
		ImagePack.getFiles('p_superbounce_face', 'Players/superbounce_face', 2)

		ImagePack.getFiles('e_minislime', 'Enemies/minislime', 9)
		ImagePack.getFiles('e_minislime_walk', 'Enemies/minislime_walk', 8)
		ImagePack.getFiles('e_minislime_die', 'Enemies/minislime_die', 6)

		ImagePack.getFiles('t___dummy', 'Terrains/__dummy')
		ImagePack.getFiles('t_solid0', 'Terrains/solid0')
		ImagePack.getFiles('t_foothold0', 'Terrains/foothold0')

		

		DamageText.loadImages()



		# get enemy data from xml file
		self.enemyStamp = []
		self.enemyId = defaultdict(list)
		self.initEnemyData()



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
		self.damageText = []

	def initEnemyData(self):
		cnt = 0
		# get root node
		root = parse("Enemy.xml").getroot()
		for tag in root.getiterator("enemy"):
			# get name especially
			name = tag.find("name").text
			stamp = Enemy(0, 0, name)

			# get data
			stamp.eid = cnt
			stamp.lv = int(tag.find("lv").text)
			stamp.sort = tag.find("sort").text # species(machine, ghost, animal, ...)
			#stamp.type
			stamp.boss = bool(int(tag.find("boss").text))
			stamp.move = int(tag.find("move").text)
			stamp.maxHP = stamp.HP = int(tag.find("hp").text)
			stamp.maxMP = stamp.MP = int(tag.find("mp").text)
			stamp.ATK = int(tag.find("atk").text)
			stamp.DEF = int(tag.find("def").text)
			stamp.MATK = int(tag.find("matk").text)
			stamp.MDEF = int(tag.find("mdef").text)
			stamp.SPD = int(tag.find("speed").text)
			stamp.JMP = int(tag.find("jump").text)
			stamp.KB = int(tag.find("kb").text)
			stamp.EXP = int(tag.find("exp").text)
			stamp.GOLD = int(tag.find("gold").text)
			#stamp.drop
			stamp.imgFrame = int(tag.find("imgframe").text)
			stamp.rect.size = (int(tag.find("width").text), int(tag.find("height").text))
			#stamp.skill

			# append to list and dict
			self.enemyStamp.append(stamp)
			self.enemyId[name] = cnt
			cnt += 1



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
		# draw damage texts
		for dt in self.damageText:
			dt.draw()

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
		self.player.update(self.attacksAlly, self.attacksEnemy, self.damageText)

		for enemy in self.enemies:
			enemy.update(self.player, self.attacksAlly, self.attacksEnemy, self.damageText)

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
		for dt in self.damageText:
			dt.update()

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
		self.damageText[:] = [dt for dt in self.damageText if dt.remain > 0]



		if self.step % 60 == 0 and len(self.enemies) < 10:
			self.makeEnemy(0, random.randrange(200, 400), 100)



		self.step += 1

	def makeEnemy(self, eid, x, y):
		# check invalid eid value
		if eid < 0 or eid >= len(self.enemyStamp):
			print "invalid index"
			return

		newEnemy = self.enemyStamp[eid].stampCopy() #copy.copy(self.enemyStamp[eid])
		newEnemy.setCoord(x, y)
		self.enemies.append(newEnemy)