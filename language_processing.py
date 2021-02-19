from sprites import * 
from itertools import *
# Who's doing it, verb, to what
class ConfusedError(Exception):
    def __init__(self, subject = None):
        self.subject = subject

class Word:
    def __init__(self, image_name, my_color = [0,0,0]):
        self.image_name = image_name
        self.image = pygame.image.load(image_name)
        self.image.fill(my_color,special_flags = pygame.BLEND_ADD)

class Verb(Word): # move, interact, etc.
    def __init__(self, image_name, function, my_color = [0,0,0]):
        super().__init__(image_name,my_color=my_color)
        self.function = function

    def __call__(self, map_state, subject, object, adverb = None):
        # This actually does the action refered to by the verb
        if map_state[subject[0]][subject[1]] is not None and "orderable" in map_state[subject[0]][subject[1]].attributes:
            self.function(map_state, subject, object, adverb)
        else:
            raise ConfusedError(map_state[subject[0]][subject[1]])

class Noun(Word): # everyone, yellow, rock, you, me
    def __init__(self, image_name, thing=None, my_color = [0,0,0]):
        super().__init__(image_name,my_color=my_color)
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
    def __init__(self, image_name, my_color = [0,0,0]):
        super().__init__(image_name, my_color=my_color)

class Letter(Word): # 
    def __init__(self, image_name, my_color = [0,0,0]):
        super().__init__(image_name, my_color=my_color)

class Address(Word): # please, hello, goodbye
    def __init__(self, image_name, my_color = [0,0,0]):
        super().__init__(image_name, my_color=my_color)

class Adjective(Word):
    def __init__(self, image_name, my_color = [0,0,0]):
        super().__init__(image_name, my_color=my_color)

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

Misunderstand = Address("images/Language/Adress/Misunderstand.png") # this needs a variable
#Me = Noun("Me.png")
#You = Noun("You.png")

"""Drop = Verb("images/Language/MovementCommands/Drop.png")
Interact = Verb("images/Language/MovementCommands/Interact.png")
Throw = Verb("images/Language/MovementCommands/Throw.png")
Grab = Verb("images/Language/MovementCommands/Grab.png")
"""
word_dict = {
    'h': Address('images/Language/Adress/Hello.png'),
    'hj': Address("images/Language/Adress/Goodbye.png"),
    'plk': Noun("images/Language/Colors/Purple.png", NPC_Purple, [83,52,128]),
    'pom': Noun("images/Language/Colors/Blue.png", NPC_Blue, [55,81,139]),
    'pu': Noun('images/Language/Colors/Green.png', NPC_Green, [51,114,48]),
    'plu': Noun("images/Language/Colors/Orange.png", NPC_Orange, [144,73,41]),
    'pln': Noun("images/Language/Colors/Red.png",NPC_Red,  [88,0,0]),
    'pl': Noun("images/Language/Colors/Yellow.png",NPC_Yellow,  [143,131,54]),
    'oupu': Noun("images/Language/Things/Log.png", Log),
    'm': Verb('images/Language/Modifiers/Move.png', lambda map_state, subject, object, adverb: move_person(1, 0, map_state, type(map_state[subject[0]][subject[1]]))),
    'mn': Verb("images/Language/MovementCommands/GoDown.png", lambda map_state, subject, object, adverb: move_person(0, 1, map_state, type(map_state[subject[0]][subject[1]]))),
    'mj': Verb("images/Language/MovementCommands/GoLeft.png", lambda map_state, subject, object, adverb: move_person(-1, 0, map_state, type(map_state[subject[0]][subject[1]]))),
    'mk': Verb("images/Language/MovementCommands/GoUp.png", lambda map_state, subject, object, adverb: move_person(0, -1, map_state, type(map_state[subject[0]][subject[1]]))),
    'j': Letter("images/Language/Modifiers/Negate.png"),
    'o': Adjective("images/Language/Things/Thing.png"),
    'p': Letter("images/Language/Modifiers/Color.png"),
#    'i': Me,
    'u': Adjective("images/Language/Things/Ground.png"),
    'n': Adjective("images/Language/Things/Underground.png"),
    'k': Adjective("images/Language/Things/Sky.png"),
#    'g': Grab,
    'l': Adjective("images/Language/Things/Fire.png"),
    'jj': Address("images/Language/Adress/Emphasize.png"),
    'io': Address("images/Language/Adress/Iam.png"),
#    'ij': You,
#    'mjj': Address("images/Language/Adress/Stop.png"),
    'mo': Adverb("images/Language/Modifiers/To.png"),
    'poj': Noun("images/Language/Colors/Black.png", None),
    'pou': Noun("images/Language/Colors/Gray.png", None),
    'po': Noun("images/Language/Colors/White.png", None),
    'lk': Adjective("images/Language/Things/Lightning.png"),
    'oj': Adjective("images/Language/Things/Nothing.png"),
    'ou': Adjective("images/Language/Things/Rock.png"),
    'om': Adjective("images/Language/Things/Water.png"),
    'ouo': Adjective("images/Language/Things/Wall.png"),
    'omk': Adjective("images/Language/Things/Cloud.png"),
    'omom': Adjective("images/Language/Things/Rain.png"),
#    'gj': Drop,
#    'gm': Interact,
#    'gjm': Throw
}
