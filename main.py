import pygame
from pygame import sprite
from language_processing import *
from sprites import *
pygame.init()
from levels import *

width = 1000
height = 800
#tile_size = 90

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


### Player Typing ###
gamemode = "Moving"
typedphrase = ""
cursorlocation = 0

legitcharacters = {
    pygame.K_j : "j", 
    pygame.K_o : "o", 
    pygame.K_u : "u", 
    pygame.K_h : "h", 
    pygame.K_p : "p", 
    pygame.K_m : "m", 
    pygame.K_g : "g",
    pygame.K_i : "i",
    pygame.K_k : "k",
    pygame.K_l : "l", 
    pygame.K_n : "n"
} 
sprite_map = draw_board(current_map)

while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if gamemode == "Moving":
                    move_person(1, 0, sprite_map,tile_size, You)
                elif gamemode == "Typing":
                    cursorlocation += 1
                    if cursorlocation>len(typedphrase):
                        cursorlocation = len(typedphrase)
            elif event.key == pygame.K_LEFT:
                if gamemode == "Moving":
                    move_person(-1, 0, sprite_map,tile_size, You)
                elif gamemode == "Typing":
                    cursorlocation -= 1
                    if cursorlocation<0:
                        cursorlocation = 0
            elif event.key == pygame.K_UP:
                if gamemode == "Moving":
                    move_person(0, -1, sprite_map,tile_size, You)
                elif gamemode == "Typing":
                    cursorlocation = len(typedphrase)
            elif event.key == pygame.K_DOWN:
                if gamemode == "Moving":
                    move_person(0, 1, sprite_map,tile_size, You)
                elif gamemode == "Typing":
                    cursorlocation = 0
            elif event.key == pygame.K_RETURN:
                if gamemode == "Moving":
                    gamemode = "Typing"
                elif gamemode == "Typing":
                    gamemode = "Moving"
                    #language_processing(sayphrase)
            elif event.key == pygame.K_r:
                if gamemode == "Moving":
                    restart_level()
            # elif event.key == pygame.K_q:
            #     parse_sentence(typedphrase, sprite_map)
            #     parse_sentence("h pu m", sprite_map)
            elif event.key == pygame.K_DELETE:
                if cursorlocation>0:
                    cursorlocation-=1
                    typedphrase = typedphrase[:cursorlocation] + typedphrase[cursorlocation+1:]
            
            if gamemode=="Typing":
                if event.key in legitcharacters:
                    typedphrase.insert(cursorlocation,legitcharacters[legitcharacters])
                    cursorlocation+=1
            # try:
            #     parse_sentence(sprite_map, typedphrase) 
            # except ConfusedError as err:
            #     if err.subject == None:
            #         pass # Eventually should be changed to make the player confused
            #     else
            #         err.subject.be_confused()
    
    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
