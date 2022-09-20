import pygame

class UI:
	def __init__(self,surface):
		
		#SETUP
		self.display_surface = surface

		#HEALTH
		self.health_bar = pygame.image.load('images/ui/health.png').convert_alpha()
		self.health_bar = pygame.transform.scale(self.health_bar,(220,20))
		self.health_bar_topleft = (39,23)
		self.bar_max_width = 200
		self.bar_height = 13

		#COINS
		self.coin = pygame.image.load('images/ui/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (20,50))
		self.font = pygame.font.Font('images/ui/ARCADE.ttf',30)

		#CLOCK
		self.clock = pygame.image.load('images/ui/clock.png').convert_alpha()
		self.clock_rect = self.clock.get_rect(topleft = (20,90))
		self.font = pygame.font.Font('images/ui/ARCADE.ttf',30)



	def show_health(self,current,full):
		self.display_surface.blit(self.health_bar,(20,20))
		current_health_ratio = current / full
		current_bar_width = self.bar_max_width *current_health_ratio
		health_bar_rect = pygame.Rect((self.health_bar_topleft),(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#0bf446',health_bar_rect)

	def show_coins(self,amount):
		self.display_surface.blit(self.coin,self.coin_rect)
		coin_amount_surf = self.font.render(str(amount),True,'black')
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 6,self.coin_rect.centery + 7))
		self.display_surface.blit(coin_amount_surf,coin_amount_rect)

	def show_score(self):
		self.display_surface.blit(self.clock,self.clock_rect)


