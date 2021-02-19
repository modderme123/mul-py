from sprites import * 
from itertools import *
# Who's doing it, verb, to what
class ConfusedError(Exception):
    def __init__(self, subject = None):
        self.subject = subject

class Word:
    def __init__(self, image_name):
        self.image_name = image_name
        self.image = pygame.image.load(image_name)

class Verb(Word): # move, interact, etc.
    def __init__(self, image_name, function):
        super().__init__(image_name)
        self.function = function

    def __call__(self, map_state, subject, object, adverb = None):
        # This actually does the action refered to by the verb
        if map_state[subject[0]][subject[1]] is not None and "orderable" in map_state[subject[0]][subject[1]].attributes:
            self.function(map_state, subject, object, adverb)
        else:
            raise ConfusedError(map_state[subject[0]][subject[1]])

class Noun(Word): # everyone, yellow, rock, you, me
    def __init__(self, image_name, thing=None):
        super().__init__(image_name)
        self.thing = thing
    
    def get_location(self, map_state, subject_coords):
        # Returns the row and col of the thing closest to subject
        # subject_coords is (row, col)

        # all row, col s
        locations = sorted(product(range(len(map_state)), range(len(map_state[0]))), key=lambda x: x[0]-subject_coords[0]+x[1]-subject_coords[1])
        for row_num, col_num in locations:
            if type(map_state[row_num][col_num]) == self.thing:
                return (row_num, col_num)
        raise ConfusedError(map_state[subject_coords[0]][subject_coords[1]])


class Adverb(Word): # up, down, left, right, underground, around
    def __init__(self, image_name):
        super().__init__(image_name)

class Letter(Word): # 
    def __init__(self, image_name):
        super().__init__(image_name)

class Address(Word): # please, hello, goodbye
    def __init__(self, image_name):
        super().__init__(image_name)

class Adjective(Word):
    def __init__(self, image_name):
        super().__init__(image_name)

def parse_sentence(sentence, map_state):
    try:
        sentence = [word_dict[word] for word in sentence.split(" ")]
        sentences = []
        current_sentence = []
        for word in sentence:
            if type(word) == Address:
                sentences.append(current_sentence)
                current_sentence = []
            else:
                current_sentence.append(word)
        sentences.append(current_sentence)

        for phrase in sentences:
            evaluate(phrase, map_state)

    except KeyError:
        raise ConfusedError()


def evaluate(sentence, map_state):
    # Takes in the word_dict (objects) for a setence and runs the verb(s) code
    #print(type(sentence))
    if len(sentence) == 0:
        return
    subject = sentence.pop(0)
    if type(subject) != Noun:
        raise ConfusedError()

    while len(sentence)>0:
        subject_coords = subject.get_location(map_state, (0, 0)) # Should only be one subject, so (0, 0) shouldn't change anything
        verb = sentence.pop(0)
        if type(verb) != Verb:
            raise ConfusedError(subject)
        
        if len(sentence) == 0:
            verb(map_state, subject_coords, None)
            continue


        next = sentence.pop(0)
        if type(next) == Adverb:
            verb(map_state, subject, None, next)
        elif type(next) == Noun:
            direct_object_coords = next.get_location(map_state, subject_coords)
            if len(sentence) == 0:
                verb(map_state, subject_coords, direct_object_coords)
                continue

            next = sentence.pop(0)
            if type(next) == Adverb:
                verb(map_state, subject_coords, direct_object_coords, next)
            else:
                sentence.insert(0, next)
                verb(map_state, subject_coords, direct_object_coords)
        else:
            sentence.insert(0, next)
            verb(map_state, subject_coords, None)


def empty(obj):
    return obj == None or "flat" in obj.attributes

def move_person(dsquare_x, dsquare_y, map, person):
    flag = True
    map_height = len(map)
    map_width = len(map[0])
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

def standard_move(map_state, subject, direct_object, adverb = None):
    # Takes the coords for objects
    move_person(0, 1, map_state, type(map_state[subject[0]][subject[1]]))

tile_size = 90 # TODO: update if changed thank

Hello = Address('images/Language/Adress/Hello.png')
Green = Noun('images/Language/Colors/Green.png', NPC_Green)
Move = Verb('images/Language/Modifiers/Move.png', lambda map_state, subject, object, adverb: move_person(1, 0, map_state, type(map_state[subject[0]][subject[1]])))

Emphasize = Address("images/Language/Adress/Emphasize.png")
I_Am = Address("images/Language/Adress/Iam.png")
Misunderstand = Address("images/Language/Adress/Misunderstand.png") # this needs a variable
#Me = Noun("Me.png")
#You = Noun("You.png")
Goodbye = Address("images/Language/Adress/Goodbye.png")
Stop = Address("images/Language/Adress/Stop.png")
Color = Letter("images/Language/Modifiers/Color.png")
Negate = Letter("images/Language/Modifiers/Negate.png")
To = Adverb("images/Language/MovementCommands/To.png")
Black = Noun("images/Language/Colors/Black.png", None)
Yellow = Noun("images/Language/Colors/Yellow.png", NPC_Yellow)
Blue = Noun("images/Language/Colors/Blue.png", NPC_Blue)
Gray = Noun("images/Language/Colors/Gray.png", None)
Orange = Noun("images/Language/Colors/Orange.png", NPC_Orange)
Purple = Noun("images/Language/Colors/Purple.png", NPC_Purple)
Red = Noun("images/Language/Colors/Red.png", NPC_Red)
White = Noun("images/Language/Colors/White.png", None)
Fire = Adjective("images/Language/Things/Fire.png")
Ground = Adjective("images/Language/Things/Ground.png")
Lightning = Adjective("images/Language/Things/Lightning.png")
Nothing = Adjective("images/Language/Things/Nothing.png")
Rock = Adjective("images/Language/Things/Rock.png")
Sky = Adjective("images/Language/Things/Sky.png")
Thing = Adjective("images/Language/Things/Thing.png")
Underground = Adjective("images/Language/Things/Underground.png")
Water = Adjective("images/Language/Things/Water.png")
Wall = Adjective("images/Language/Things/Wall.png")
Cloud = Adjective("images/Language/Things/Cloud.png")
Rain = Adjective("images/Language/Things/Rain.png")
Log = Noun("images/Language/Things/Log.png", Log)
Go_Down = Verb("images/Language/MovementCommands/GoDown.png", lambda map_state, subject, object, adverb: move_person(0, 1, map_state, type(map_state[subject[0]][subject[1]])))
Go_Up = Verb("images/Language/MovementCommands/GoUp.png", lambda map_state, subject, object, adverb: move_person(0, -1, map_state, type(map_state[subject[0]][subject[1]])))
Go_Left = Verb("images/Language/MovementCommands/GoLeft.png", lambda map_state, subject, object, adverb: move_person(-1, 0, map_state, type(map_state[subject[0]][subject[1]])))
"""Drop = Verb("images/Language/MovementCommands/Drop.png")
Interact = Verb("images/Language/MovementCommands/Interact.png")
Throw = Verb("images/Language/MovementCommands/Throw.png")
Grab = Verb("images/Language/MovementCommands/Grab.png")
"""
word_dict = {
    'h': Hello,
    'hj': Goodbye,
    'plk': Purple,
    'pom': Blue,
    'pu': Green,
    'plu': Orange,
    'pln': Red,
    'pl': Yellow,
    'oupu': Log,
    'm': Move,
    'mn': Go_Down,
    'mj': Go_Left,
    'mk': Go_Up
}
"""word_dict = {
    'j': Negate,
    'o': Thing,
    'm': Move,
    'p': Color,
    'i': Me,
    'u': Ground,
    'n': Underground,
    'k': Sky,
    'g': Grab,
    'l': Fire,
    'jj': Emphasize,
    'io': I_Am,
    'ij': You,
    'mj': Stop,
    'mo': To,
    'poj': Black,
    'pou': Gray,
    'po': White,
    'lk': Lightning,
    'oj': Nothing,
    'ou': Rock,
    'om': Water,
    'ouo': Wall,
    'omk': Cloud,
    'omom': Rain,
    'gj': Drop,
    'gm': Interact,
    'gjm': Throw
}"""



