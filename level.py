import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, screen_height
from tiles import Tile, StaticTile, Coin
from enemy import Enemy
from decoration import Sky, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
	def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
		#SETUP
		self.display_surface = surface
		self.world_shift = -2
		self.current_x = None

		#SOUNDS
		self.coin_sound = pygame.mixer.Sound('audio/effects/coin.wav')
		self.explode_sound = pygame.mixer.Sound('audio/effects/explode.wav')

		#OVERWORLD
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		#PLAYER
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout,change_health)

		#UI
		self.change_coins = change_coins

		#DUST
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		#EXPLODE
		self.explosion_sprites = pygame.sprite.Group()

		#TERRAIN SETUP
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		#TREES
		tree_layout = import_csv_layout(level_data['tree'])
		self.tree_sprites = self.create_tile_group(tree_layout,'tree')

		#MUSHROOMS
		mushrooms_layout = import_csv_layout(level_data['mushrooms'])
		self.mushrooms_sprites = self.create_tile_group(mushrooms_layout,'mushrooms')

		#ROCKS
		rocks_layout = import_csv_layout(level_data['rocks'])
		self.rocks_sprites = self.create_tile_group(rocks_layout,'rocks')

		#WATER
		#ROCKS
		water_layout = import_csv_layout(level_data['water'])
		self.water_sprites = self.create_tile_group(water_layout,'water')

		#COINS
		coins_layout = import_csv_layout(level_data['coins'])
		self.coins_sprites = self.create_tile_group(coins_layout,'coins')

		#ENEMY
		enemies_layout = import_csv_layout(level_data['enemies'])
		self.enemies_sprites = self.create_tile_group(enemies_layout,'enemies')

		#CONSTRICT
		constrict_layout = import_csv_layout(level_data['constrict'])
		self.constrict_sprites = self.create_tile_group(constrict_layout,'constrict')

		#decoration
		self.sky_bg = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.clouds = Clouds(-300,level_width,10)



	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('images/terrain/Tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					if type == 'tree':
						tree_tile_list = import_cut_graphics('images/terrain/Tileset.png')
						tile_surface = tree_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'mushrooms':
						mushrooms_tile_list = import_cut_graphics('images/terrain/Tileset.png')
						tile_surface = mushrooms_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'rocks':
						rocks_tile_list = import_cut_graphics('images/terrain/Tileset.png')
						tile_surface = rocks_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'water':
						water_tile_list = import_cut_graphics('images/terrain/Tileset.png')
						tile_surface = water_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'coins':
						if val == '0': sprite = Coin(tile_size,x,y,'images/coins/gold',2)
						if val == '1': sprite = Coin(tile_size,x,y,'images/coins/silver',1)

					if type == 'enemies':
						sprite = Enemy(tile_size,x,y)

					if type == 'constrict':
						sprite = Tile(tile_size,x,y)

					sprite_group.add(sprite)

		return sprite_group

	def player_setup(self,layout,change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y= row_index * tile_size
				if val == '97':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
					self.player.add(sprite)
				if val == '98':
					flag_surface = pygame.image.load('images/player/finish_flag.png').convert_alpha()
					sprite = StaticTile(tile_size,x,y,flag_surface)
					self.goal.add(sprite)



	def enemy_collision_reversal(self):
		for enemy in self.enemies_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constrict_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)


	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.collision_rect.x += player.direction.x * player.speed

		for sprite in self.terrain_sprites.sprites():
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0:
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.terrain_sprites.sprites():
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0:
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 4
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -4
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 4

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)	
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.create_overworld(self.current_level, 0)


	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			self.create_overworld(self.current_level, self.new_max_level)

	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coins_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			for coin in collided_coins:
				self.change_coins(coin.value)

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemies_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.explode_sound.play()
					self.player.sprite.direction.y = -16
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
				else:
					self.player.sprite.get_damage()



	def run(self):
		#RUN LEVEL

		#DECORATION
		self.sky_bg.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)

		#WATER
		self.water_sprites.update(self.world_shift)
		self.water_sprites.draw(self.display_surface)
		
		#DUST
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)
		
		#TERRAIN
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)


		#TREES
		self.tree_sprites.update(self.world_shift)
		self.tree_sprites.draw(self.display_surface)

		#MUSHROOMS
		self.mushrooms_sprites.update(self.world_shift)
		self.mushrooms_sprites.draw(self.display_surface)

		#ROCKS
		self.rocks_sprites.update(self.world_shift)
		self.rocks_sprites.draw(self.display_surface)

		#ENEMY
		self.enemies_sprites.update(self.world_shift)
		self.constrict_sprites.update(self.world_shift)
		self.enemy_collision_reversal()
		self.enemies_sprites.draw(self.display_surface)

		#EXPLODE
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)
		
		#COINS
		self.coins_sprites.update(self.world_shift)
		self.coins_sprites.draw(self.display_surface)


		#PLAYER
		self.player.update()
		self.horizontal_movement_collision()

		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()

		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()



