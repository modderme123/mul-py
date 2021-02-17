import pygame
import math

class generic_sprite(pygame.sprite.Sprite):
    '''This class holds all the data for a generic sprite'''

    attributes = []
    
    def __init__(self, image_names, screen, sprite_group, scale):


        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        #print(image_names)
        self.images = [pygame.image.load(image_name) for image_name in image_names]
        self.images = [pygame.transform.scale(image,(scale,scale)) for image in self.images]
        self.animation_frame = 0
        #self.scale = scale
        sprite_group.add(self)

    def draw_sprite(self, x, y):
        """
        Draws this piece
        args:
            x, y (ints): The location on the screen to draw this piece
            scale (int): Scale factor for the piece"""
        #image = pygame.transform.scale(self.images[0], (self.scale, self.scale))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def move(self, dx, dy):
        self.draw_sprite(self.rect.left + dx, self.rect.top + dy)

    def nextframe(self):
        self.animation_frame+=0.2
        self.animation_frame%=len(self.images)
        self.image = self.images[math.floor(self.animation_frame)]

    def update(self):
        self.nextframe()



class Wall(generic_sprite):

    attributes = []
    def __init__(self, screen, sprite_group, scale, surroundings):
        images = self.find_which_wall(surroundings)
        super().__init__(images, screen, sprite_group, scale)
    
    def find_which_wall(self,surroundings): # characters directly above, left, down and right
        coords = [1 if el=="w" else 0 for el in surroundings]
        print(coords)
        letterdict = [
            [[["?","["],["1","p"]],  # 0,0,?,?
            [["]","-"],["q","?"]]],  # 0,1,?,?

            [[["!","b"],["I","?"]], # 1,0,?,?
            [["d","?"],["?","?"]]], # 1,1,?,?
        ]
        thing = letterdict[coords[0]][coords[1]][coords[2]][coords[3]]
        if thing=='?':
            return ["images/objects/log.png"]
        return ["images/walls/"+thing+".png"]


class Rock(generic_sprite):

    attributes = ['pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/objects/rock.png"], screen, sprite_group, scale)

class Log(generic_sprite):
    attributes = ['pickable', 'pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/objects/now_this_is_a_log.png"], screen, sprite_group, scale)

class You(generic_sprite):

    attributes = ['pickable', 'pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/Player/player1.png", "images/Player/player2.png", "images/Player/player3.png"], screen, sprite_group, scale)

class Goal(generic_sprite):
    
    attributes = ['goal']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/goal/flag1.png","images/goal/flag2.png"], screen, sprite_group, scale)
