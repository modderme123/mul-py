import pygame
from language_processing import *
from sprites import *
pygame.init()
from levels import *

width = 1000
height = 800
tile_size = 90

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MUL")
clock = pygame.time.Clock()


background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
screen.blit(background, (0, 0))


level = 0
current_map = [list(row) for row in levels[level]]

map_height = len(current_map)
map_width = len(current_map[0])
mapoffset = [(width-(map_width*tile_size))/2,(height-(map_height*tile_size))/2]

letter_to_sprite_map = {
    "w": Wall,
    "U": You,
    "G": Goal,
    "R": Rock,
    " ": None,
    "1": Sign1,
    "2": Sign2,
    "(": NPC_Green,#NPC_Red,
    ")": NPC_Green,#NPC_Orange,
    "[": NPC_Green,#NPC_Yellow,
    "]": NPC_Green,
    "{": NPC_Green,#NPC_Blue,
    "}": NPC_Green,#NPC_Purple
}


sprites = pygame.sprite.Group()
flag = True

def next_level():
    global level,current_map,map_width,map_height,mapoffset,gamemode,typedphrase,cursorlocation, sprites,sprite_map
    level +=1 
    level %= len(levels)
    current_map = [list(row) for row in levels[level]]
    map_height = len(current_map)
    map_width = len(current_map[0])
    mapoffset = [(width-(map_width*tile_size))/2,(height-(map_height*tile_size))/2]

    gamemode = "Moving"
    typedphrase = []
    cursorlocation = 0
    
    sprites = pygame.sprite.Group()
    sprite_map = draw_board(current_map)

def restart_level():
    global level,current_map,map_width,map_height,mapoffset,gamemode,typedphrase,cursorlocation, sprites,sprite_map
    current_map = [list(row) for row in levels[level]]
    map_height = len(current_map)
    map_width = len(current_map[0])
    mapoffset = [(width-(map_width*tile_size))/2,(height-(map_height*tile_size))/2]

    gamemode = "Moving"
    typedphrase = []
    cursorlocation = 0
    
    sprites = pygame.sprite.Group()
    sprite_map = draw_board(current_map)

def draw_board(level):
    # Changes level to be sprites instead of the objects
    new_board = [[[] for i in range(len(row))] for row in level]
    for y, row in enumerate(level):
        #print(y,row)
        for x, char in enumerate(row):
            if letter_to_sprite_map[char] != None:
                #print(x,char)
                new_board[y][x] = addSprite(level,char,x,y)
            else:
                new_board[y][x] = None
    return new_board


def addSprite(level,char,x,y):
    if char == "w":
        #print(x,y)
        up = (level[y-1][x] if y>0 else "?")
        right = (level[y][x+1] if x<map_width-1 else "?")
        down = (level[y+1][x] if y<map_height-1 else "?")
        left = (level[y][x-1] if x>0 else "?")
        sprite = letter_to_sprite_map[char](screen, sprites, tile_size,[up,right,down,left])
    elif char == "G":
        sprite = letter_to_sprite_map[char](screen, sprites, tile_size, next_level)
    else:
        sprite = letter_to_sprite_map[char](screen, sprites, tile_size)
    sprites.add(sprite)
    sprite.draw_sprite((x*tile_size)+mapoffset[0], (y*tile_size)+mapoffset[1])
    return sprite

def empty(obj):
    return obj == None or "flat" in obj.attributes

def move_person(dsquare_x, dsquare_y, map, person):
    flag = True
    map_height = len(current_map)
    map_width = len(current_map[0])
    # For entities who can only appear once. 
    # Person is something like You, Green, etc.
    for row_num, row in enumerate(map):
        for col_num, sqr in enumerate(row):
            if type(sqr) == person:
                if (0 <= row_num+dsquare_y < map_height and 
                    0 <= col_num+dsquare_x < map_width and 
                    (empty(map[row_num+dsquare_y][col_num+dsquare_x]) or
                    ("pushable" in map[row_num+dsquare_y][col_num+dsquare_x].attributes and empty(map[row_num+2*dsquare_y][col_num+2*dsquare_x])))):
    
                    entity = map[row_num][col_num]
                    tostandon = None
                    if map[row_num+dsquare_y][col_num+dsquare_x] is not None:
                        if "flat" in map[row_num+dsquare_y][col_num+dsquare_x].attributes:
                            tostandon = map[row_num+dsquare_y][col_num+dsquare_x]
                        elif "pushable" in map[row_num+dsquare_y][col_num+dsquare_x].attributes:
                            map[row_num+dsquare_y][col_num+dsquare_x].move(dsquare_x*tile_size, dsquare_y*tile_size)
                            tostandon = map[row_num+dsquare_y][col_num+dsquare_x].stop_standing()
                            if map[row_num+2*dsquare_y][col_num+2*dsquare_x] is not None: # must be flat
                                map[row_num+dsquare_y][col_num+dsquare_x].start_standing(map[row_num+2*dsquare_y][col_num+2*dsquare_x])
                            map[row_num+2*dsquare_y][col_num+2*dsquare_x] = map[row_num+dsquare_y][col_num+dsquare_x]
                    map[row_num+dsquare_y][col_num+dsquare_x] = entity
                    map[row_num][col_num] = entity.stop_standing()
                    entity.start_standing(tostandon)
                    entity.move(dsquare_x*tile_size, dsquare_y*tile_size)
                flag = False
                break
        if not flag:
            break


set_move_person(move_person) #TODO: make this not bad (move move_person into language processing)

### Player Typing ###
gamemode = "Moving"
typedphrase = []
cursorlocation = 0

legitcharacters = {} # fill with characters that are relevant to the language e.g. {pygame.K_a : "a"}
sprite_map = draw_board(current_map)

while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if gamemode == "Moving":
                    move_person(1, 0, sprite_map, You)
                elif gamemode == "Typing":
                    cursorlocation += 1
                    if cursorlocation>len(typedphrase):
                        cursorlocation = len(typedphrase)
            elif event.key == pygame.K_LEFT:
                if gamemode == "Moving":
                    move_person(-1, 0, sprite_map, You)
                elif gamemode == "Typing":
                    cursorlocation -= 1
                    if cursorlocation<0:
                        cursorlocation = 0
            elif event.key == pygame.K_UP:
                if gamemode == "Moving":
                    move_person(0, -1, sprite_map, You)
                elif gamemode == "Typing":
                    cursorlocation = len(typedphrase)
            elif event.key == pygame.K_DOWN:
                if gamemode == "Moving":
                    move_person(0, 1, sprite_map, You)
                elif gamemode == "Typing":
                    cursorlocation = 0
            elif event.key == pygame.K_RETURN:
                if gamemode == "Moving":
                    gamemode = "Typing"
                elif gamemode == "Typing":
                    gamemode = "Moving"
                    #language_processing(sayphrase)
            elif event.key == pygame.K_r:
                restart_level()
            elif event.key == pygame.K_q:
                parse_sentence("h pu m", sprite_map)
            
            if gamemode=="Typing":
                if event.key in legitcharacters:
                    typedphrase.insert(cursorlocation,legitcharacters)
                    cursorlocation+=1
    
    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
