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
RED = (255, 0, 0)
BLUE = (0, 0, 255)
black_surf = pygame.Surface((30, 30))
black_surf.fill(BLACK)
white_surf = pygame.Surface((30, 30))
white_surf.fill(WHITE)

# 1是可以通过 0是不可以通过
matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('pathfinding_snowfield')
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

# varibles setup
game_active = True

# class setup
# class = Class()
class Pathfinder: # pathfinder 在这里是一个功能, 这个类的作用就是管理这个功能的代码
    def __init__(self,matrix):

        # setup
        self.matrix = matrix
        self.grid = Grid(matrix = matrix)
        # self.select_surf = pygame.image.load('selection.png').convert_alpha()
        self.select_surf_1 = pygame.Surface((30, 30))
        self.select_surf_1.fill(BLUE)
        self.select_surf_2 = pygame.Surface((26, 26))
        self.select_surf_2.fill(WHITE)

        # pathfinding
        self.path = []
        self.path_enemy_1 = []

        # player
        self.player = pygame.sprite.GroupSingle(player(self.empty_path))
        # self.player = player(self.empty_path)

        # enemy
        self.enemy_group = pygame.sprite.Group()
        self.enemy_1 = Enemy(self.empty_path, (825+1, 75))
        self.enemy_2 = Enemy(self.empty_path, (75+1, 825))
        self.enemy_3 = Enemy(self.empty_path, (825+1, 825))
        self.enemy_group.add(self.enemy_1, self.enemy_2, self.enemy_3)


    def empty_path(self):
        self.path = []

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row =  mouse_pos[1] // 30
        col =  mouse_pos[0] // 30
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect_1 = pygame.Rect((col * 30,row * 30),(30,30))
            rect_2 = pygame.Rect((col * 30+2,row * 30+2),(26,26))
            screen.blit(self.select_surf_1,rect_1)
            screen.blit(self.select_surf_2,rect_2)

    def create_path(self): # 第一个功能, 按下鼠标后开始执行
        # start
        start_x, start_y = self.player.sprite.get_coord() # 获得player位置对应处的矩阵索引
        start = self.grid.node(start_x,start_y)

        # end
        mouse_pos = pygame.mouse.get_pos()
        end_x,end_y =  mouse_pos[0] // 30, mouse_pos[1] // 30   # 和上面获得player位置的带马基本相同
        end = self.grid.node(end_x,end_y) 

        # path
        if start_x != end_x or start_y != end_y:
            finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
            self.path,_ = finder.find_path(start,end,self.grid)
            self.grid.cleanup()
            self.player.sprite.set_path(self.path)  # 将生成的path传入player

    def create_path_enemy(self): # 第一个功能, 按下鼠标后开始执行
        print(self.enemy_group.sprites())
        for enemy in self.enemy_group.sprites():
            # start
            start_x, start_y = enemy.get_coord() # 获得player位置对应处的矩阵索引
            start = self.grid.node(start_x,start_y)

            # end
            # mouse_pos = pygame.mouse.get_pos()
            # debug(self.rect.x, info_name='player.rect.x', y =30)
            # end_x, end_y = self.player.pos[0]//30, self.player.pos[1]//30
            end_x, end_y = self.player.sprite.get_coord()
            # end_x,end_y =  mouse_pos[0] // 30, mouse_pos[1] // 30   # 和上面获得player位置的带马基本相同
            end = self.grid.node(end_x,end_y) 

            # path
            if start_x != end_x or start_y != end_y:
                finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
                self.path_enemy,_ = finder.find_path(start,end,self.grid)
                self.grid.cleanup()
                enemy.set_path(self.path_enemy)  # 将生成的path传入enemy

    def update(self, dt):
        self.draw_active_cell()

        # player updating and drawing
        self.player.update(dt)
        self.player.draw(screen)
        self.enemy_group.update(dt)
        self.enemy_group.draw(screen)

class player(pygame.sprite.Sprite):
    def __init__(self,empty_path):

        # basic
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center = (46,45))

        # movement 
        self.pos = self.rect.center
        self.speed = 400
        self.direction = pygame.math.Vector2(0,0)
        self.old_rect = self.rect.copy()

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

    def reposition_player(self):
        if self.path == []:
            row =  self.pos[1] // 30
            col =  self.pos[0] // 30
            self.rect.center = (col*30+15, row*30+15)
        else:
            # print('not repositioned')
            self.rect.center = self.pos

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point[0] * 30) + 15
                y = (point[1] * 30) + 15
                points.append((x,y))
                pygame.draw.circle(screen, BLUE,(x, y), 5)
            pygame.draw.lines(screen, BLUE,False,points,5)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.check_collisions()
        self.reposition_player()
        self.draw_path()
        # debug(self.rect.x, info_name='player.rect.x', y =30)
        # debug(self.path, y = 50, info_name='self.path')
        self.old_rect = self.rect.copy() 

class Enemy(pygame.sprite.Sprite):
    def __init__(self,empty_path, enemy_start_position):

        # basic
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = enemy_start_position)

        # movement
        self.pos = self.rect.center
        self.speed = 350
        self.direction = pygame.math.Vector2(0,0)
        self.old_rect = self.rect.copy()

        # path 
        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path

    def get_coord(self):
        col = self.rect.centerx // 30
        row = self.rect.centery // 30
        return (col, row)

    def set_path(self, path):
        self.path = path
        self.create_collsion_rects()
        self.get_direction()

    def create_collsion_rects(self):
        if self.path:
            self.collision_rects = []
            for points in self.path:
                x = (points[0]*30)+15
                y = (points[1]*30)+15
                rect = pygame.Rect((x-2, y-2), (4,4))
                self.collision_rects.append(rect)

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
        self.pos += self.direction * self.speed * dt
        self.check_collisions()
        self.rect.center = self.pos
        self.old_rect = self.rect.copy() 

# functions ------------------------------------------------------------------------------------------------- #
def draw_background(matrix, white_surf, black_surf):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:  # 不可以通过, 涂黑
                screen.blit(black_surf, (col*30, row*30))
            if matrix[row][col] != 0:  # 可以通过, 涂白
                screen.blit(white_surf, (col*30, row*30))

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

            if event.type == enemy_timer:
                pathfinder.create_path_enemy()

        if game_active:
            screen.fill(WHITE)
            draw_background(matrix, white_surf, black_surf)
            pathfinder.update(dt)

        pygame.display.update()


if __name__ == "__main__":
    main()
