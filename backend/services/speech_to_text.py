import whisper

print("Loading Whisper model...")

model = whisper.load_model("small")

print("Whisper model loaded!")


def speech_to_text(audio_file):
    result = model.transcribe(
        audio_file,
        language="hi",
        fp16=False,
        temperature=0
    )

    return result["text"].strip()