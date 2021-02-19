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
        self.standing_on = None
        #self.scale = scale
        self.sprite_group = sprite_group
        self.sprite_group.add(self)
        self.scale = scale

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
    
    def start_standing(self,obj):
        self.standing_on = obj
        if obj is not None:
            obj.becomestood(self)
    
    def stop_standing(self):
        temp = self.standing_on
        self.standing_on = None
        if temp is not None:
            temp.becomeunstood(self)
        return temp

    def becomestood(self,stander):
        pass
    
    def becomeunstood(self,unstander):
        pass

    def be_confused(self):
        confusion = Confusion(self.rect.left, self.rect.top-round(self.scale*1.5), self.sprite_group, round(self.scale*1.5))

class Confusion(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group, scale):
        super().__init__()
        image_names = ["images/thinking/thinking_1.png","images/thinking/thinking_2.png"]
        self.images = [pygame.image.load(image_name) for image_name in image_names]
        self.images = [pygame.transform.scale(image,(scale,scale)) for image in self.images]
        self.animation_frame = 0

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        sprite_group.add(self)

    def nextframe(self):
        self.animation_frame+=0.2
        self.image = self.images[math.floor(self.animation_frame%len(self.images))]

        if self.animation_frame >= 10:
            self.kill()

    def update(self):
        self.nextframe()

class Wall(generic_sprite):

    attributes = []
    def __init__(self, screen, sprite_group, scale, surroundings):
        images = self.find_which_wall(surroundings)
        super().__init__(images, screen, sprite_group, scale)
    
    def find_which_wall(self,surroundings): # characters directly above, right, down and left
        ans = ""
        if surroundings[0]=="w": ans+="N"
        if surroundings[1]=="w": ans+="E"
        if surroundings[2]=="w": ans+="S"
        if surroundings[3]=="w": ans+="W"
        if len(ans)==0:
            return ["images/walls/block.png"]
        return ["images/walls/"+ans+".png"]


class Rock(generic_sprite):

    attributes = ['pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/rock/rock_1.png","images/rock/rock_2.png"], screen, sprite_group, scale)

class Log(generic_sprite):

    attributes = ['pickable', 'pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/log/log_1.png","images/log/log_2.png"], screen, sprite_group, scale)

class You(generic_sprite):

    attributes = ['pickable', 'pushable']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/Player/player1.png", "images/Player/player2.png", "images/Player/player3.png"], screen, sprite_group, scale)

class Goal(generic_sprite):
    
    attributes = ['goal', 'flat']
    def __init__(self, screen, sprite_group, scale, nextlevel):
        self.nextlevel = nextlevel
        super().__init__(["images/goal/flag1.png","images/goal/flag2.png"], screen, sprite_group, scale)
    def becomestood(self, stander):
        if type(stander)==You:
            print("hi!")
            self.nextlevel()
            #idk win or something
        return super().becomestood(stander)

class Sign1(generic_sprite):

    attributes = ['flat']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/signs/sign_1.png"], screen, sprite_group, scale)


class Sign2(generic_sprite):

    attributes = ['flat']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/signs/sign_2.png"], screen, sprite_group, scale)

class NPC(generic_sprite):

    attributes = ['orderable']
    def __init__(self, image_names, screen, sprite_group, scale):
        super().__init__(image_names, screen, sprite_group, scale)

class NPC_Green(NPC):
    attributes = ['orderable','green']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/green/green_1.png","images/green/green_2.png"], screen, sprite_group, scale)
class NPC_Blue(NPC):
    attributes = ['orderable','blue']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/blue/blue_1.png","images/blue/blue_2.png"], screen, sprite_group, scale)
class NPC_Yellow(NPC):
    attributes = ['orderable','yellow']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/yellow/yellow_1.png","images/yellow/yellow_2.png"], screen, sprite_group, scale)
class NPC_Orange(NPC):
    attributes = ['orderable','orange']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/orange/orange_1.png","images/orange/orange_2.png"], screen, sprite_group, scale)
class NPC_Red(NPC):
    attributes = ['orderable','red']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/red/red_1.png","images/red/red_2.png"], screen, sprite_group, scale)
class NPC_Purple(NPC):
    attributes = ['orderable','purple']
    def __init__(self, screen, sprite_group, scale):
        super().__init__(["images/purple/purple_1.png","images/purple/purple_2.png"], screen, sprite_group, scale)

class Button(generic_sprite):
    attributes = ['flat']
    def __init__(self, screen, sprite_group, scale, doors):
        self.doors = doors
        super().__init__(["images/objects/button_up.png","images/objects/button_down.png"], screen, sprite_group, scale)

    def becomestood(self, stander):
        self.image = self.images[1]
        for door in self.doors:
            door.receive_button_press()
        return super().becomestood(stander)
    
    def becomeunstood(self, unstander):
        self.image = self.images[0]
        for door in self.doors:
            door.remove_button_press()

        return super().becomestood(unstander)

    def update(self):
        pass

class Door(generic_sprite):
    attributes = ['flattenable']
    def __init__(self, screen, sprite_group, scale, number_of_buttons):
        super().__init__(["images/objects/door_up.png","images/objects/door_down.png"], screen, sprite_group, scale)
        self.number_of_buttons = number_of_buttons
        self.buttons_pressed = 0

    def receive_button_press(self):
        self.buttons_pressed += 1
        if self.buttons_pressed >= self.number_of_buttons:
            Door.attributes = ["flat"]
            self.image = self.images[1]


    def remove_button_press(self):
        self.buttons_pressed -= 1
        if self.buttons_pressed < self.number_of_buttons:
            Door.attributes = []
            self.image = self.images[0]
    
    def update(self):
        pass
    
