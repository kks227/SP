import pygame
from pygame.locals import *

class Screen:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.canvas = pygame.display.set_mode((width, height))

	def draw(self):
		# fill background with default color
		self.canvas.fill(0)