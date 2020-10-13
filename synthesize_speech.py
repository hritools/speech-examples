import os
import simpleaudio as sa

from texttospeech import TextToSpeech
from tempfile     import NamedTemporaryFile

# Utility function to play .wav files
def play_wav(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

# Create a default solution
tts = TextToSpeech()

# Read what needs to be synthesized
print("Введите путь до файла с текстом для синтеза: ")
with open(input(), mode="r") as f:
    text = f.readline()

# Synthesize audiodata and write them to temporary file
audiodata = tts.synthesize(text)
with NamedTemporaryFile(mode="wb") as f:
    f.write(audiodata.get_wav_data())
    audiopath = os.path.abspath(f.name)

    # Play the file
    play_wav(audiopath)
