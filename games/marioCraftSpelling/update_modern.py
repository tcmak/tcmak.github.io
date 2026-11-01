import json
import re

with open('simple_dictionary.json', 'r', encoding='utf-8') as f:
    simple_dict = json.load(f)

with open('words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

count_updated = 0
count_missed = 0
missed_words = []

def get_def(w):
    entry = simple_dict.get(w)
    if entry and 'MEANINGS' in entry and len(entry['MEANINGS']) > 0:
        return entry['MEANINGS'][0][1]
    return None

for item in words:
    w = item['word'].upper()
    new_def = get_def(w)
    
    if not new_def and w.endswith('S'):
        new_def = get_def(w[:-1])
    if not new_def and w.endswith('ES'):
        new_def = get_def(w[:-2])
    if not new_def and w.endswith('ED'):
        new_def = get_def(w[:-2])
    if not new_def and w.endswith('ING'):
        new_def = get_def(w[:-3])
    if not new_def and w.endswith('LY'):
        new_def = get_def(w[:-2])
        
    if new_def:
        word_pattern = re.compile(r'\b' + re.escape(item['word']) + r'\b', re.IGNORECASE)
        masked_def = word_pattern.sub('*' * len(item['word']), new_def)
        item['definition'] = masked_def.capitalize() + ('.' if not masked_def.endswith('.') else '')
        count_updated += 1
    else:
        missed_words.append(w)
        count_missed += 1

with open('words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, indent=4)

print(f"Updated {count_updated}, Missed {count_missed}")
if count_missed > 0:
    print(f"Sample missed: {missed_words[:20]}")
