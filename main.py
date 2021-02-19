import pygame
from pygame import sprite
from pygame.constants import K_SPACE
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
background.fill((255, 255, 255))
screen.blit(background, (0, 0))

level = 0
current_map = [list(row) for row in levels[level]]

map_height = len(current_map)
map_width = len(current_map[0])
mapoffset = [(width - (map_width * tile_size)) / 2,
             (height - (map_height * tile_size)) / 2]

letter_to_sprite_map = {
    "w": Wall,
    "U": You,
    "G": Goal,
    "R": Rock,
    "X": Door,
    "o": Button,
    " ": None,
    "1": Sign1,
    "2": Sign2,
    "(": NPC_Red,
    ")": NPC_Orange,
    "[": NPC_Yellow,
    "]": NPC_Green,
    "{": NPC_Blue,
    "}": NPC_Purple,
}

sprites = pygame.sprite.Group()
flat_sprites = pygame.sprite.Group()
flag = True
player = None


def next_level():
    global level, levels
    level += 1
    level %= len(levels)
    restart_level()

def restart_level():
    global doors, level, current_map, map_width, map_height, mapoffset, gamemode, typedphrase, cursorlocation, sprites, flat_sprites, sprite_map
    current_map = [list(row) for row in levels[level]]
    map_height = len(current_map)
    map_width = len(current_map[0])
    mapoffset = [(width - (map_width * tile_size)) / 2,
                 (height - (map_height * tile_size)) / 2]

    gamemode = "Moving"
    typedphrase = []
    cursorlocation = 0

    doors = []
    sprites = pygame.sprite.Group()
    flat_sprites = pygame.sprite.Group()
    sprite_map = draw_board(current_map)


def draw_board(level):
    # Changes level to be sprites instead of the objects
    global player
    new_board = [[[] for i in range(len(row))] for row in level]
    for y, row in enumerate(level):
        #print(y,row)
        for x, char in enumerate(row):
            if letter_to_sprite_map[char] != None:
                #print(x,char)
                new_board[y][x] = addSprite(level, char, x, y)
                if type(new_board[y][x]) == You:
                    player = new_board[y][x]
            else:
                new_board[y][x] = None
    return new_board


doors = []
def addSprite(level, char, x, y):
    
    if char == "w":
        #print(x,y)
        up = (level[y - 1][x] if y > 0 else "?")
        right = (level[y][x + 1] if x < map_width - 1 else "?")
        down = (level[y + 1][x] if y < map_height - 1 else "?")
        left = (level[y][x - 1] if x > 0 else "?")
        sprite = letter_to_sprite_map[char](screen, sprites, tile_size, [up, right, down, left])
    elif char == "G":
        sprite = letter_to_sprite_map[char](screen, flat_sprites, tile_size, next_level)
    elif char == "X":
        number_of_buttons = "".join(["".join(x) for x in level]).count("o")
        sprite = letter_to_sprite_map[char](screen, flat_sprites, tile_size, number_of_buttons)
        doors.append(sprite)
    elif char == "o":
        sprite = letter_to_sprite_map[char](screen, flat_sprites, tile_size, doors)
    else:
        if 'flattenable' in letter_to_sprite_map[char].attributes or 'flat' in letter_to_sprite_map[char].attributes:
            sprite = letter_to_sprite_map[char](screen, flat_sprites, tile_size)
        else:
            sprite = letter_to_sprite_map[char](screen, sprites, tile_size)

    sprite.draw_sprite((x * tile_size) + mapoffset[0],
                       (y * tile_size) + mapoffset[1])

            
    return sprite


def draw_text(screen):
    #print(len(text_sprites))
    for index, sprite in enumerate(text_sprites):
        screen.blit(pygame.transform.scale(sprite.image,(textsize,textsize)), (textsize * 1.5 * index, 0))


def update_text_sprites(phrase):
    global text_sprites
    text_sprites = []
    tempword = ""
    words = []
    for letter in phrase:
        if letter != " ":
            tempword += letter
        else:
            words.append(tempword)
            tempword = ""
    if len(tempword)>0:
        words.append(tempword)
    for word in words:
        if word in word_dict:
            text_sprites.append(word_dict[word])
        else:
            text_sprites.append(Misunderstand)


### Player Typing ###
gamemode = "Moving"
typedphrase = []
text_sprites = []
cursorlocation = 0
textsize = 50
displayhelp = False

legitcharacters = {
    pygame.K_j: "j",
    pygame.K_o: "o",
    pygame.K_u: "u",
    pygame.K_h: "h",
    pygame.K_p: "p",
    pygame.K_m: "m",
    pygame.K_g: "g",
    pygame.K_i: "i",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_n: "n",
    pygame.K_SPACE: " ",
}
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
                    if cursorlocation > len(typedphrase):
                        cursorlocation = len(typedphrase)
            elif event.key == pygame.K_LEFT:
                if gamemode == "Moving":
                    move_person(-1, 0, sprite_map, You)
                elif gamemode == "Typing":
                    cursorlocation -= 1
                    if cursorlocation < 0:
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
                    update_text_sprites(typedphrase)
                elif gamemode == "Typing":
                    try:
                        parse_sentence("".join(typedphrase), sprite_map)
                    except ConfusedError as err:
                        if err.subject == None:
                            player.be_confused()
                            pass  # Eventually should be changed to make the player confused
                        else:
                            err.subject.be_confused()
                    typedphrase = []
                    gamemode = "Moving"
                    #language_processing(sayphrase)
            elif event.key == pygame.K_r:
                if gamemode == "Moving":
                    restart_level()
            elif event.key == pygame.K_SPACE:
                if gamemode == "Moving":
                    displayhelp = not displayhelp
            # elif event.key == pygame.K_q:
            #     parse_sentence(typedphrase, sprite_map)
            #     parse_sentence("h pu m", sprite_map)
            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                if gamemode == "Typing":
                    if cursorlocation > 0:
                        cursorlocation -= 1
                        typedphrase = typedphrase[:cursorlocation] + typedphrase[cursorlocation + 1:]
                        
                        update_text_sprites(typedphrase)

            if gamemode == "Typing":
                if event.key in legitcharacters:
                    typedphrase.insert(cursorlocation, legitcharacters[event.key])
                    cursorlocation += 1
                    update_text_sprites(typedphrase)



    screen.blit(background, (0, 0))
    flat_sprites.clear(screen, background)
    sprites.clear(screen, background)
    flat_sprites.update()
    sprites.update()
    flat_sprites.draw(screen)
    sprites.draw(screen)
    if gamemode == "Typing":
        draw_text(screen)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
