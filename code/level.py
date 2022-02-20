from random import choice
import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utils import (
	import_csv_layout,
	import_folder
)


class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		#* sprite group setup 类似 Layer
		# 会在屏幕上显示的 Sprite
		self.visible_sprites = YSortGroup()
		# 会被用于计算碰撞的 Sprite
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()


	def create_map(self):
		layouts = {
			'boundary': import_csv_layout("../map/map_FloorBlocks.csv"),
			'grass': import_csv_layout("../map/map_Grass.csv"),
			'object': import_csv_layout("../map/map_LargeObjects.csv"),
		}

		graphics = {
			'grass': import_folder("../graphics/grass"),
			'object': import_folder("../graphics/objects"),
		}

		for style, layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							random_grass_img = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_img)
						if style == 'object':
							object_img = graphics['object'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_img)

		self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)
		

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.direction)


class YSortGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.dispaly_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()
		self.half_size = pygame.math.Vector2(self.dispaly_surface.get_size())
		self.half_size = self.half_size / 2

		self.floor_surf = pygame.image.load("../graphics/tilemap/ground.png")
		self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

	
	def custom_draw(self, player):
		#* calc offset 将Player放到屏幕中间需要的移动量
		self.offset = self.half_size - player.rect.center

		self.dispaly_surface.blit(
			self.floor_surf, self.floor_rect.topleft + self.offset)
		#* 决定渲染顺序
		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft + self.offset
			self.dispaly_surface.blit(sprite.image, offset_pos)
		