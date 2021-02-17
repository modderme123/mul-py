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
    "BBBBBBBB",
    "Bww    B",
    "B ww wGB", 
    "B U  wwB",
    "BBBBBBBB"
],
[
    "BBBBBBBBBB",
    "B      wwB", 
    "BU    E GB", 
    "B      wwB",
    "BBBBBBBBBB"
],
[
    "     ww",
    ""
]
]


level = 0
current_map = [list(row) for row in levels[level]]

map_height = len(current_map)
map_width = len(current_map[0])

letter_to_sprite_map = {
    "w": Wall,
    "U": You,
    "G": Goal,
    "B": Boundary,
    " ": None,
}

tile_size = 90
sprite_scale = 90

def draw_board(level):
    # Changes level to be sprites instead of the objects
    new_board = [[[] for i in range(len(row))] for row in level]
    for y, row in enumerate(level):
        print(y,row)
        for x, char in enumerate(row):
            if letter_to_sprite_map[char] != None:
                print(x,char)
                new_board[y][x] = addSprite(level,char,x,y)
            else:
                new_board[y][x] = None
    return new_board

def addSprite(level,char,x,y):
    if char == "w":
        print(x,y)
        up = (level[y-1][x] if y>0 else "?")
        left = (level[y][x-1] if x>0 else "?")
        down = (level[y+1][x] if y<map_height-1 else "?")
        right = (level[y][x+1] if x<map_width-1 else "?")
        sprite = letter_to_sprite_map[char](screen, sprites, sprite_scale,[up,left,down,right])
    else:
        sprite = letter_to_sprite_map[char](screen, sprites, sprite_scale)
    sprites.add(sprite)
    sprite.draw_sprite(x*tile_size, y*tile_size)
    return sprite


sprites = pygame.sprite.Group()
flag = True
gamemode = "Moving"
sprite_map = draw_board(current_map)

def empty(obj):
    return obj == None or "flat" in obj.attributes

def move_player(dsquare_x, dsquare_y, map):
    flag = True
    for row_num, row in enumerate(map):
        for col_num, sqr in enumerate(row):
            if type(sqr) == You:
                if (0 <= row_num+dsquare_y < map_height and 
                    0 <= col_num+dsquare_x < map_width and 
                    (empty(map[row_num+dsquare_y][col_num+dsquare_x]) or
                    ("pushable" in map[row_num+dsquare_y][col_num+dsquare_x].attributes and empty(map[row_num+2*dsquare_y][col_num+2*dsquare_x])))):
    
                    player = map[row_num][col_num]
                    map[row_num+dsquare_y][col_num+dsquare_x] = player
                    map[row_num][col_num] = None
                    player.move(dsquare_x*tile_size, dsquare_y*tile_size)
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
                if gamemode == "Moving":
                    move_player(1, 0, sprite_map)
            elif event.key == pygame.K_LEFT:
                if gamemode == "Moving":
                    move_player(-1, 0, sprite_map)
            elif event.key == pygame.K_UP:
                if gamemode == "Moving":
                    move_player(0, -1, sprite_map)
            elif event.key == pygame.K_DOWN:
                if gamemode == "Moving":
                    move_player(0, 1, sprite_map)
            elif event.key == pygame.K_RETURN:
                if gamemode == "Moving":
                    gamemode = "Typing"
                elif gamemode == "Typing":
                    gamemode = "Moving"


    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
