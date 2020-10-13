import re

from speechtotext         import SpeechToText
from texttointent         import TextToIntentSimple
from texttointent.intents import Intent

# Utility functions
def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

# Define target intents
class MoveForward(Intent):
    @staticmethod
    def get_keywords():
        return ["вперёд", "вперед"]

class MoveBackward(Intent):
    @staticmethod
    def get_keywords():
        return ["назад"]

class MoveRight(Intent):
    @staticmethod
    def get_keywords():
        return ["направо", "вправо", "право"]

class MoveLeft(Intent):
    @staticmethod
    def get_keywords():
        return ["налево", "влево", "лево"]

class Stop(Intent):
    @staticmethod
    def get_keywords():
        return ["стоп", "остановись"]


# Start speech recognition
stt = SpeechToText()
stt.adjust_for_ambient_noise(duration=1.0)
print("Произносите команды!")
print("-----------------")
record = stt.record_from_microphone()
text   = stt.translate(record)

# Parse the semantics (we already know what kind of input we have so we can work with a command by command basis)
tti                = TextToIntentSimple([MoveBackward, MoveForward, MoveLeft, MoveRight, Stop])
recognized_intents = []
for command in split([" ", "-"], text):
    intent = tti.parse(command)
    # If the intent is identified then print it
    if intent is not None:
        recognized_intents.append(intent)

# Print as required by the testing scenario
for ind, intent in enumerate(recognized_intents):
    print("{} - {}".format(ind, intent.get_keywords()[0]))
print("-----------------")
print("Все найденные команды успешно выведены!")