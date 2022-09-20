import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
	def __init__(self):
		#
		self.max_level = 0
		self.max_health = 100
		self.current_health = 100
		self.coins = 0

		#SOUNDS
		self.bg_music = pygame.mixer.Sound('audio/bg.wav')
		self.ow_music = pygame.mixer.Sound('audio/menu.wav')

		#OVERWORLD
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.ow_music.play(loops = -1)

		#UI
		self.ui = UI(screen)




	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		self.ow_music.stop()
		self.bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.ow_music.play(loops = -1)
		self.bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.current_health += amount

	def game_fin(self):
		if self.current_health <= 0:
			self.current_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			self.bg_music.stop()
			self.ow_music.play(loops = -1)

	def display_score(self):
		font = pygame.font.Font('images/ui/ARCADE.ttf',30)
		current_time = pygame.time.get_ticks() / 1000
		score_surf = font.render(f'{current_time}',True,'black')
		score_rect = score_surf.get_rect(midleft = (60,110))
		screen.blit(score_surf,score_rect)

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.current_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.ui.show_score()
			self.display_score()
			self.game_fin()



#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Rush & Jump')
clock = pygame.time.Clock()
game = Game()



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()



	game.run()

	pygame.display.update()
	clock.tick(60)