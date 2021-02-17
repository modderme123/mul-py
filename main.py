import pygame
from language_processing import *
from sprites import *
pygame.init()


width = 800
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MUL")
clock = pygame.time.Clock()


background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
screen.blit(background, (0, 0))

levels = [
[
    "www    w",
    "w ww wGw", 
    "w U  www"
],
[
    "      ww", 
    "U    E G", 
    "      ww"
],
[
    "     ww",
    ""
]
]


level = 0
current_map = [list(row) for row in levels[level]]


letter_to_sprite_map = {
    "w": Wall,
    "U": You,
    "G": Goal,
    " ": None,
}

tile_size = 90
sprite_scale = 90

def draw_board(level):
    # Changes level to be sprites instead of the objects
    new_board = [[[] for i in range(len(row))] for row in level]
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if letter_to_sprite_map[char] != None:
                new_board[y][x] = addSprite(level,char,x,y)
            else:
                new_board[y][x] = None
    return new_board

def addSprite(level,char,x,y):
    if char == "w":
        up = (level[y-1][x] if y!=0 else "?")
        left = (level[y][x-1] if x!=0 else "?")
        down = (level[y+1][x] if y!=len(level)-1 else "?")
        right = (level[y][x+1] if x!=len(level[0])-1 else "?")
        sprite = letter_to_sprite_map[char](screen, sprites, sprite_scale,[up,left,down,right])
    else:
        sprite = letter_to_sprite_map[char](screen, sprites, sprite_scale)
    sprites.add(sprite)
    sprite.draw_sprite(x*tile_size, y*tile_size)
    return sprite


sprites = pygame.sprite.Group()

flag = True



player = None
sprite_map = draw_board(current_map)
for row in sprite_map:
    for obj in row:
        if type(obj) == You:
            player = obj

print(player)

def move_player(dsquare_x, dsquare_y, map):
    flag = True
    for row_num, row in enumerate(map):
        for col_num, sqr in enumerate(row):
            if type(obj) == You:
                if map[row_num+dsquare_y][col_num+dsquare_x] == None:
                    player = map[row_num][col_num]
                    map[row_num+dsquare_y][col_num+dsquare_x] = player
                    map[row_num][col_num] = None
                    player.move(dsquare_y*tile_size, dsquare_x*tile_size)
                flag = False
                break
        if not flag:
            break

while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_player(1, 0, sprite_map)
            elif event.key == pygame.K_LEFT:
                move_player(-1, 0, sprite_map)
            elif event.key == pygame.K_UP:
                move_player(0, -1, sprite_map)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1, sprite_map)


    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
