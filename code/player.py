import os
import pygame 
from debug import debug
from utils import import_folder
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0, -26)
		self.state = "down"
		self.frame_index = 0
		self.anim_spd = 0.15
		# graphic set up
		self.import_player_assets()
		# move
		self.direction = pygame.math.Vector2()
		self.speed = 5
		# collision
		self.obstacle_sprites = obstacle_sprites
		# attack
		self.attacking = False
		self.atk_cooldown = 400
		self.atk_time = None

	def import_player_assets(self):
		chara_path = "../graphics/player"
		self.animations = {
			'up': [], 'down': [], 'left': [], 'right': [],
			'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
			'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
		}

		for anim in self.animations.keys():
			full_path = os.path.join(chara_path, anim)
			self.animations[anim] = import_folder(full_path)


	#* 处理输入信号
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
			self.state = 'up'
		elif keys[pygame.K_s]:
			self.direction.y = 1
			self.state = 'down'
		else:
			self.direction.y = 0

		if keys[pygame.K_a]:
			self.direction.x = -1
			self.state = 'left'
		elif keys[pygame.K_d]:
			self.direction.x = 1
			self.state = 'right'
		else:
			self.direction.x = 0

		if keys[pygame.K_j] and not self.attacking:
			self.attacking = True
			self.atk_time = pygame.time.get_ticks()
		if keys[pygame.K_k] and not self.attacking:
			self.attacking = True
			self.atk_time = pygame.time.get_ticks()


	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			self.chage_state('idle')

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			self.chage_state('attack')


	def chage_state(self, state: str):
		if '_' in self.state:
			self.state = self.state.split('_')[0]

		self.state = self.state + '_' + state


	#* 处理移动
	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		self.hitbox.centerx += self.direction.x * speed
		self.collision("horizontal")
		self.hitbox.centery += self.direction.y * speed
		self.collision("vertical")

		#* rect跟随 hitbox
		self.rect.center = self.hitbox.center

	#* 处理碰撞
	def collision(self, direction):
		if direction == "horizontal":
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					elif self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
		if direction == "vertical":
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					elif self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom


	def cooldowns(self):
		curr_time = pygame.time.get_ticks()  # ms

		if self.attacking and curr_time - self.atk_time >= self.atk_cooldown:
			self.attacking = False


	def animate(self):
		anim = self.animations[self.state]
		self.frame_index = (self.frame_index + self.anim_spd) % len(anim)
		self.image = anim[int(self.frame_index)]
		self.rect = self.image.get_rect(center=self.hitbox.center)


	#* 实际调用各种处理方法，会被Group调用
	def update(self):
		self.input()
		self.get_status()
		debug(self.state)
		self.move(self.speed)
		self.cooldowns()
		self.animate()


