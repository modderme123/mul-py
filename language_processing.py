from sprites import * 
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
    def __init__(self, image, thing):
        super().__init__(image)
        self.thing = thing
    
    def get_location(self, map_state, subject_coords):
        # Returns the row and col of the thing closest to subject
        # subject_coords is (row, col)
        #TODO: add bfs to find closest noun
        for row_num, row in enumerate(map_state):
            for col_num, sqr in enumerate(row):
                if type(map_state[row_num][col_num]) == self.thing:
                    return (row_num, col_num)
        raise ConfusedError

class Adverb(Word): # up, down, left, right, underground, around
    def __init__(self, image):
        super().__init__(image)

class Address(Word): # please, hello, goodbye
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

move_person = None
def set_move_person(mp):
    global move_person
    move_person = mp

def move_thing(map_state, subject, direct_object, adverb = None):
    global move_person
    # Takes the coords for objects
    move_person(0, 1, map_state, type(map_state[subject[0]][subject[1]]))


Hello = Address('Hello.png')
Green = Noun('Green.png', NPC_Green)
Move = Verb('Move.png', move_thing)

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
