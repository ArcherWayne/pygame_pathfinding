from urllib.parse import scheme_chars
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import pygame
import sys
import time
from debug import debug

# general setup --------------------------------------------------------------------------------------------- #
# color setup
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
black_surf = pygame.Surface((30, 30))
black_surf.fill(BLACK)
white_surf = pygame.Surface((30, 30))
white_surf.fill(WHITE)

# 1是可以通过 0是不可以通过
matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
     0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
     0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('pathfinding_snowfield')

# varibles setup
game_active = True

# class setup
# class = Class()
class Pathfinder: # pathfinder 在这里是一个功能, 这个类的作用就是管理这个功能的代码
	def __init__(self,matrix):

		# setup
		self.matrix = matrix
		self.grid = Grid(matrix = matrix)
		self.select_surf = pygame.image.load('selection.png').convert_alpha()

		# pathfinding
		self.path = []

		# Roomba
		self.roomba = pygame.sprite.GroupSingle(Roomba(self.empty_path))

	def empty_path(self):
		self.path = []

	def draw_active_cell(self):
		mouse_pos = pygame.mouse.get_pos()
		row =  mouse_pos[1] // 30
		col =  mouse_pos[0] // 30
		current_cell_value = self.matrix[row][col]
		if current_cell_value == 1:
			rect = pygame.Rect((col * 30,row * 30),(30,30))
			screen.blit(self.select_surf,rect)

	def create_path(self): # 第一个功能, 按下鼠标后开始执行

		# start
		start_x, start_y = self.roomba.sprite.get_coord()
		start = self.grid.node(start_x,start_y)

		# end
		mouse_pos = pygame.mouse.get_pos()
		end_x,end_y =  mouse_pos[0] // 30, mouse_pos[1] // 30  
		end = self.grid.node(end_x,end_y) 

		# path
		finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
		self.path,_ = finder.find_path(start,end,self.grid)
		self.grid.cleanup()
		self.roomba.sprite.set_path(self.path)  # 将生成的path传入roomba

	def draw_path(self):
		if self.path:
			points = []
			for point in self.path:
				x = (point[0] * 30) + 15
				y = (point[1] * 30) + 15
				points.append((x,y))
				pygame.draw.circle(screen, "#124542",(x, y), 5)
			pygame.draw.lines(screen,'#4a4a4a',False,points,5)

	def update(self, dt):
		self.draw_active_cell()
		self.draw_path()

		# roomba updating and drawing
		self.roomba.update(dt)
		self.roomba.draw(screen)

class Roomba(pygame.sprite.Sprite):
	def __init__(self,empty_path):

		# basic
		super().__init__()
		self.image = pygame.image.load('roomba.png').convert_alpha()
		self.rect = self.image.get_rect(center = (60,60))

		# movement 
		self.pos = self.rect.center
		self.speed = 400
		self.direction = pygame.math.Vector2(0,0)

		# path
		self.path = []
		self.collision_rects = []
		self.empty_path = empty_path

	def get_coord(self):
		col = self.rect.centerx // 30
		row = self.rect.centery // 30
		return (col,row)

	def set_path(self,path):
		self.path = path
		self.create_collision_rects()
		self.get_direction()

	def create_collision_rects(self): # 在每个转折点处创建一个
		if self.path:
			self.collision_rects = []
			for point in self.path: # 此处参考上面的draw_path方法
				x = (point[0] * 30) + 15
				y = (point[1] * 30) + 15
				rect = pygame.Rect((x - 2,y - 2),(4,4))
				self.collision_rects.append(rect) # rect是pygame中非常重要的一个概念, 首先每个surface...?

	def get_direction(self):
		if self.collision_rects:
			start = pygame.math.Vector2(self.pos)
			end = pygame.math.Vector2(self.collision_rects[0].center)
			self.direction = (end - start).normalize()
		else:
			self.direction = pygame.math.Vector2(0,0)
			self.path = []

	def check_collisions(self):
		if self.collision_rects:
			for rect in self.collision_rects:
				if rect.collidepoint(self.pos):
					del self.collision_rects[0]
					self.get_direction()
		else:
			self.empty_path()

	def update(self, dt):
		self.pos += self.direction * self.speed * dt # 了解到这个程序完全没有考虑到dt, 自己写的程序要有dt
		self.check_collisions()
		self.rect.center = self.pos

# functions ------------------------------------------------------------------------------------------------- #
def draw_background(matrix, white_surf, black_surf):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:  # 不可以通过, 涂黑
                screen.blit(black_surf, (row*30, col*30))
            if matrix[row][col] != 0:  # 可以通过, 涂白
                screen.blit(white_surf, (row*30, col*30))

# main ------------------------------------------------------------------------------------------------------ #

def main():
    last_time = time.time()
    pathfinder = Pathfinder(matrix)
    while True:

        # delta time    ------------------------------------------------------------------------------------- #
        dt = time.time() - last_time
        last_time = time.time()

        # event loop    ------------------------------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinder.create_path()

        if game_active:
            screen.fill(WHITE)
            draw_background(matrix, white_surf, black_surf)
            debug(pygame.mouse.get_pos(), info_name='mouse_pos')
            pathfinder.update(dt)

        pygame.display.update()


if __name__ == "__main__":
    main()
