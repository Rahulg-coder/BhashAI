import re

with open('android/app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

queries = [
    'किताब खोलो', 'बैठ जाओ', 'चुप रहो', 'ताली बजाओ', 'हाथ उठाओ', 
    '1 से 10 तक गिनती बोलो', 'नमस्ते बच्चों', 'पानी पी लो', 'सेब', 'मछली',
    'पंक्ति में खड़े हो जाओ', 'बोर्ड पर देखो', 'जोर से बोलो', 'साफ-साफ लिखो',
    'तुम्हारा क्या नाम है', 'सब लोग सुनो', 'कोई सवाल है', 'हाजिरी बोलो',
    'कितने बच्चे आए हैं', 'समय पर आया करो', 'दो और दो कितने होते हैं', 'शाबाश'
]

kw_block = re.search(r'const KEYWORD_AUDIO_MAP = \[(.*?)\n    \];', html, re.DOTALL).group(1)
entries = kw_block.split('},')
kw_map = []
for e in entries:
    keys_m = re.search(r'keys:\s*\[(.*?)\]', e)
    audio_m = re.search(r'audio:\s*\'([^\']+)\'', e)
    sat_m = re.search(r'sat:\s*\'([^\']+)\'', e)
    pho_m = re.search(r'pho:\s*\'([^\']+)\'', e)
    if keys_m and audio_m:
        keys = [k.strip().strip("'").strip('"') for k in keys_m.group(1).split(',')]
        kw_map.append({'keys': keys, 'audio': audio_m.group(1), 'sat': sat_m.group(1) if sat_m else '', 'pho': pho_m.group(1) if pho_m else ''})

print(f"Total keyword rules: {len(kw_map)}")

all_matched = True
for q in queries:
    matched = False
    lower_q = q.lower()
    for item in kw_map:
        for k in item['keys']:
            if k.lower() in lower_q or lower_q in k.lower():
                print(f"MATCH: '{q}' -> {item['audio']} ({item['pho']})")
                matched = True
                break
        if matched:
            break
    if not matched:
        print(f"MISSED: '{q}'")
        all_matched = False

print('All test queries matched successfully:', all_matched)
