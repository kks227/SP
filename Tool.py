import math

import pygame
from pygame.locals import *

def enum(*args):
	enums = dict(zip(args, range(len(args))))
	return type('Enum', (), enums)



# functions
def listAdd(v1, v2):
	return [x+y for x,y in zip(v1, v2)]

def listSub(v1, v2):
	return [x-y for x,y in zip(v1, v2)]

def listCoeff(v, c):
	return [c*x for x in v]

def listNorm(v):
	vSize = math.sqrt(sum(x**2 for x in v))
	if vSize == 0:
		vSize = 1
	return [float(x)/vSize for x in v]