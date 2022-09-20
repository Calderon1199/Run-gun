import pygame
from settings import *
from support import import_folder
from random import choice, randint
from tiles import StaticTile


class Nite:
	def __init__(self):
		self.nite = pygame.image.load('images/overworld/nite.png').convert()
		self.nite = pygame.transform.scale(self.nite,(screen_width,screen_height))

	def draw(self,surface):
		for row in range(vertical_tile_number):
			y = row * tile_size
			surface.blit(self.nite,(0,0))
class Sky:
	def __init__(self,horizon):

		self.sky = pygame.image.load('images/mountain/sky.png').convert()
		# self.mt1 = pygame.image.load('../images/mountain/rocks_1.png').convert()
		# self.mt2 = pygame.image.load('../images/mountain/rocks_2.png').convert_alpha()
		self.horizon = horizon

	#STRETCH BACKGROUND
		self.sky = pygame.transform.scale(self.sky,(screen_width,screen_height))
		# self.mt1 = pygame.transform.scale(self.mt1,(screen_width,screen_height))
		# self.mt2 = pygame.transform.scale(self.mt2,(screen_width,screen_height))


	def draw(self,surface):
		for row in range(vertical_tile_number):
			y = row * tile_size
			surface.blit(self.sky,(0,0))
			# surface.blit(self.mt1,(0,0))
			# surface.blit(self.mt2,(0,0))

class Clouds:
	def __init__(self,horizon,level_width,cloud_number):
		cloud_surf_list = import_folder('images/clouds')
		min_x = -screen_width
		max_x = level_width + screen_width
		min_y = -400
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list)
			x = randint(min_x, max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)