import re

from speechtotext         import SpeechToText
from texttointent         import TextToIntentSimple
from texttointent.intents import Intent
from texttointent.slots   import Slot

# Utility functions
def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)


# Slots of interest
class FollowableObject(Slot):
    ME_FORWARD  = "впереди меня"
    ME_BACKWARD = "за мной"
    ME_LEFT     = "слева от меня"
    ME_RIGHT    = "справа от меня"
    UNKNOWN     = "unknown"

    def __init__(self, value):
        if value not in self.get_values():
            self.value = FollowableObject.UNKNOWN
        else:
            self.value = value

    @staticmethod
    def get_values():
        return [FollowableObject.ME_FORWARD, FollowableObject.ME_BACKWARD, FollowableObject.ME_LEFT, FollowableObject.ME_RIGHT, FollowableObject.UNKNOWN]
            
    @staticmethod
    def get_keywords_by_value(value):
        if value == FollowableObject.ME_FORWARD:
            return ["впереди меня"]
        elif value == FollowableObject.ME_BACKWARD:
            return ["позади меня", "за мной"]
        elif value == FollowableObject.ME_RIGHT:
            return ["справа от меня"]
        elif value == FollowableObject.ME_LEFT:
            return ["слева от меня"]
        
        return []

class ObjectInSpace(Slot):
    OBJECT_RED = "красный объект"
    OBJECT_BLUE = "синий объект"
    OBJECT_GREEN = "зелёный объект"
    UNKNOWN      = "unknown"

    def __init__(self, value):
        if value not in self.get_values():
            self.value = ObjectInSpace.UNKNOWN
        else:
            self.value = value

    @staticmethod
    def get_values():
        return [ObjectInSpace.OBJECT_RED, ObjectInSpace.OBJECT_BLUE, ObjectInSpace.OBJECT_GREEN, ObjectInSpace.UNKNOWN]

    @staticmethod
    def get_keywords_by_value(value):
        if value == ObjectInSpace.OBJECT_RED:
            return ["красный объект", "бордовый объект"]
        elif value == ObjectInSpace.OBJECT_GREEN:
            return ["зелёный объект", "салатовый объект"]
        elif value == ObjectInSpace.OBJECT_BLUE:
            return ["синий объект", "голубой объект"]
        
        return []

class RelativeDirection(Slot):
    UP = "вверх"
    SIDE = "вбок"
    FORWARD = "вперёд"
    UNKNOWN = "unknown"

    def __init__(self, value):
        if value not in self.get_values():
            self.value = RelativeDirection.UNKNOWN
        else:
            self.value = value

    @staticmethod
    def get_values():
        return [RelativeDirection.UP, RelativeDirection.SIDE, RelativeDirection.FORWARD, RelativeDirection.UNKNOWN]

    @staticmethod
    def get_keywords_by_value(value):
        if value == RelativeDirection.UP:
            return ["вверх", "наверх"]
        elif value == RelativeDirection.SIDE:
            return ["вбок", "в бок", "в сторону"]
        elif value == RelativeDirection.FORWARD:
            return ["вперёд", "перед собой", "впереди себя"]

        return []


# Intents of interest
class Follow(Intent):
    @staticmethod
    def get_keywords():
        return ["следуй"]
    
    @staticmethod
    def get_slots():
        return [FollowableObject]

class ToStartPosition(Intent):
    @staticmethod
    def get_keywords():
        return ["в исходное положение", "изначальная позиция"]

class GoTo(Intent):
    @staticmethod
    def get_keywords():
        return ["иди к", "направляйся к", "ступай к", "двигайся к"]

    @staticmethod
    def get_slots():
        return [ObjectInSpace]

class Find(Intent):
    @staticmethod
    def get_keywords():
        return ["найди", "обнаружь", "ищи"]

    @staticmethod
    def get_slots():
        return [ObjectInSpace]

class Touch(Intent):
    @staticmethod
    def get_keywords():
        return ["дотронься", "потрогай", "прикоснись"]
    
    @staticmethod
    def get_slots():
        return [ObjectInSpace]

class HandRaise(Intent):
    @staticmethod
    def get_keywords():
        return ["подними руку"]

    @staticmethod
    def get_slots():
        return [RelativeDirection]


# Start speech recognition
stt = SpeechToText()
tti = TextToIntentSimple([Follow, ToStartPosition, GoTo, Find, Touch, HandRaise], slot_max_distance=3)
stt.adjust_for_ambient_noise(duration=1.0)

while True:
    print("Произнесите команду!")
    print("-----------------")
    record = stt.record_from_microphone()
    text   = stt.translate(record)

    # Parse the semantics
    intent = tti.parse(text)
    if intent is not None:
        intent_name = intent.get_keywords()[0]
        slot_name   = ""
        if len(intent.concrete_slots) > 0:
            slot_name = intent.concrete_slots[0].value
        print("{} ({})".format(intent_name, slot_name))

    print("-----------------")
    print("Введите Enter, чтобы продолжить...")
    input()