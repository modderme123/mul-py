from sprites import * 
from iter_tools import *
# Who's doing it, verb, to what
class ConfusedError(Exception):
    def __init__(self):
        pass

class Word:
    def __init__(self, image):
        self.image = image

class Verb(Word): # move, interact, etc.
    def __init__(self, image, function):
        super().__init__(image)
        self.function = function

    def __call__(self, map_state, subject, object, adverb = None):
        # This actually does the action refered to by the verb
        self.function(map_state, subject, object)

class Noun(Word): # everyone, yellow, rock, you, me
    def __init__(self, image, thing=None):
        super().__init__(image)
        self.thing = thing
    
    def get_location(self, map_state, subject_coords):
        # Returns the row and col of the thing closest to subject
        # subject_coords is (row, col)

        # all row, col s
        locations = list(product(range(map_state), map_state[0])).sort(lambda row, col: row-subject_coords[0]+col-subject_coords[1])
        for row_num, col_num in locations:
            if type(map_state[row_num][col_num]) == self.thing:
                return (row_num, col_num)
        raise ConfusedError


class Adverb(Word): # up, down, left, right, underground, around
    def __init__(self, image):
        super().__init__(image)

class Letter(Word): # 
    def __init__(self, image):
        super().__init__(image)

class Address(Word): # please, hello, goodbye
    def __init__(self, image):
        super().__init__(image)

class Adjective(Word):
    def __init__(self, image):
        super().__init__(image)

def parse_sentence(sentence, map_state):
    try:
        sentence = [words[word] for word in sentence.split(" ")]
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
        raise ConfusedError


def evaluate(sentence, map_state):
    # Takes in the words (objects) for a setence and runs the verb(s) code
    #print(type(sentence))
    if len(sentence) == 0:
        return
    subject = sentence.pop(0)
    if type(subject) != Noun:
        raise ConfusedError
    subject_coords = subject.get_location(map_state, (0, 0)) # Should only be one subject, so (0, 0) should change anything

    while len(sentence)>0:
        verb = sentence.pop(0)
        if type(verb) != Verb:
            raise ConfusedError
        
        if len(sentence) == 0:
            verb(map_state, subject_coords, None)
            continue

        # TODO: Add checks to look for end of sentence

        next = sentence.pop(0)
        if type(next) == Adverb:
            verb(map_state, subject, None, next)
        elif type(next) == Noun:
            direct_object_coords = next.get_location(map_state, subject_coords)
            next = sentence.pop(0)
            if type(next) == Adverb:
                verb(map_state, subject_coords, direct_object_coords, next)
            else:
                sentence.insert(0, next)
                verb(map_state, subject_coords, direct_object_coords)


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

def move_thing(map_state, subject, direct_object, adverb = None):
    # Takes the coords for objects
    move_person(0, 1, map_state, type(map_state[subject[0]][subject[1]]))

tile_size = 90 # TODO: update if changed thank

Hello = Address('Hello.png')
Green = Noun('Green.png', NPC_Green)
Move = Verb('Move.png', move_thing)

Emphasize = Address("Emphasize.png")
I_Am = Address("I am.png")
Misunderstand = Address("Misunderstand.png")
#Me = Noun("Me.png")
#You = Noun("You.png")
Goodbye = Address("Goodbye.png")
Stop = Address("Stop.png")
Color = Letter("Color.png")
Negate = Letter("Negate.png")
To = Adverb("To.png")
Black = Noun("Black.png", None)
Yellow = Noun("Yellow.png", NPC_Yellow)
Blue = Noun("Blue.png", NPC_Blue)
Gray = Noun("Gray.png", None)
Orange = Noun("Orange.png", NPC_Orange)
Purple = Noun("Purple.png", NPC_Purple)
Red = Noun("Red.png", NPC_Red)
White = Noun("White.png", None)
Fire = Adjective("Fire.png")
Ground = Adjective("Ground.png")
Lightning = Adjective("Lightning.png")
Nothing = Adjective("Nothing.png")
Rock = Adjective("Rock.png")
Sky = Adjective("Sky.png")
Thing = Adjective("Thing.png")
Underground = Adjective("Underground.png")
Water = Adjective("Water.png")
Wall = Adjective("Wall.png")
Cloud = Adjective("Cloud.png")
Rain = Adjective("Rain.png")
Log = Noun("Log.png",)
Go_Down = Verb("Go Down.png", move_thing)
Go_Up = Verb("Go Up.png", move_thing)
Go_Left = Verb("Go Left.png", move_thing)
Drop = Verb("Drop.png")
Interact = Verb("Interact.png")
Throw = Verb("Throw.png")
Grab = Verb("Grab.png")

words = {
    'h': Hello,
    'pu': Green,
    'm': Move
}
"""words = {
    'h': Hello,
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
    'hj': Goodbye,
    'mo': To,
    'poj': Black,
    'pom': Blue,
    'pou': Gray,
    'pu': Green,
    'plu': Orange,
    'pln': Red,
    'pl': Yellow,
    'plk': Purple,
    'po': White,
    'lk': Lightning,
    'oj': Nothing,
    'ou': Rock,
    'om': Water,
    'ouo': Wall,
    'omk': Cloud,
    'omom': Rain,
    'oupu': Log,
    'mn': Go_Down,
    'mj': Go_Left,
    'mk': Go_Up,
    'gj': Drop,
    'gm': Interact,
    'gjm': Throw
}"""



