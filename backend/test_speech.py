from services.speech_to_text import speech_to_text

audio_file = "test.wav"

text = speech_to_text(audio_file)

print("\nHindi Text:")
print(text)