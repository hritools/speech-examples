from speechtotext import SpeechToText

# Create a default solution
stt = SpeechToText()

# Start recording the text but first adjust for ambient noise
stt.adjust_for_ambient_noise(duration=1.0)
print("Говорите!")
record = stt.record_from_microphone()

# Recognize what was said
text = stt.translate(record)

print(text)