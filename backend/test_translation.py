import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "ai4bharat/indictrans2-indic-indic-dist-320M"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

print("Loading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model.eval()

print("Model loaded!")

# Hindi sentence
hindi_text = "बच्चों आज हम गिनती सीखेंगे।"

print("\nHindi:")
print(hindi_text)

# Language codes
src_lang = "hin_Deva"
tgt_lang = "sat_Olck"

# Add language information
input_text = f"{src_lang} {tgt_lang} {hindi_text}"

inputs = tokenizer(
    input_text,
    return_tensors="pt"
)

print("\nTranslating...")

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_length=256,
        num_beams=5
    )

translation = tokenizer.decode(
    output[0],
    skip_special_tokens=True
)

print("\nSantali:")
print(translation)