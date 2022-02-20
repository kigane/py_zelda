import pygame, sys, os
from settings import *
from level import Level

class Game:
	def __init__(self):
		  
		#* general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) # pygame.display.get_surface()
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock() #* 用于控制帧率

		self.level = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS) #* 保证while循环每秒执行不超过FPS次

if __name__ == '__main__':
	os.chdir("C:\workspace\py_zelda\code")
	game = Game()
	game.run()