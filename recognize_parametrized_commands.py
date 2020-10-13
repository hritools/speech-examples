import re

from speechtotext         import SpeechToText
from texttointent         import TextToIntentSimple
from texttointent.intents import Intent
from texttointent.slots   import Slot

# Utility functions
def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

# Define target intents and slots
class Direction(Slot):
    FORWARD  = "вперёд"
    BACKWARD = "назад"
    LEFT     = "налево"
    RIGHT    = "направо"
    UP       = "вверх"
    DOWN     = "вниз"
    UNKNOWN  = "unknown"

    def __init__(self, value):
        if value not in self.get_values():
            self.value = Direction.UNKNOWN
        else:
            self.value = value

    @staticmethod
    def get_values():
        return [Direction.FORWARD, Direction.BACKWARD, Direction.LEFT, Direction.RIGHT, Direction.DOWN, Direction.UP, Direction.UNKNOWN]
            
    @staticmethod
    def get_keywords_by_value(value):
        if value == Direction.FORWARD:
            return ["вперёд", "вперед", "прямо"]
        elif value == Direction.BACKWARD:
            return ["назад"]
        elif value == Direction.RIGHT:
            return ["направо", "вправо"]
        elif value == Direction.LEFT:
            return ["налево", "влево"]
        elif value == Direction.DOWN:
            return ["вниз"]
        elif value == Direction.UP:
            return ["вверх"]
        
        return []

class Movement(Intent):
    @staticmethod
    def get_keywords():
        return ["двигаться", "иди", "ступай", "пройди"]
    
    @staticmethod
    def get_slots():
        return [Direction]

class Rotate(Intent):
    @staticmethod
    def get_keywords():
        return ["повернись", "обернись", "поворот"]

    @staticmethod
    def get_slots():
        return [Direction]


# Start speech recognition
stt = SpeechToText()
tti = TextToIntentSimple([Movement, Rotate])
stt.adjust_for_ambient_noise(duration=1.0)

while True:
    print("Произнесите команду!")
    print("-----------------")
    record = stt.record_from_microphone()
    text   = stt.translate(record)

    # Parse the semantics
    intent = tti.parse(text)
    if intent is not None:
        print("{} ({})".format(intent.get_keywords()[0], intent.concrete_slots[0].value))

    print("-----------------")
    print("Введите Enter, чтобы продолжить...")
    input()