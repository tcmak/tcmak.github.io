import json
import urllib.request
import time
import re
import sys

with open('words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

def is_bad(d):
    d = d.strip()
    if 'In a manner that is' in d: return True
    if '[Obs.]' in d: return True
    if d.startswith('See '): return True
    if 'Consisting of a moiety' in d: return True
    return False

def get_def(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if isinstance(data, list) and len(data) > 0:
                meanings = data[0].get('meanings', [])
                for meaning in meanings:
                    defs = meaning.get('definitions', [])
                    if defs:
                        return defs[0].get('definition')
    except Exception as e:
        pass
    return None

count = 0
for item in words:
    if is_bad(item.get('definition', '')):
        w = item['word']
        new_d = get_def(w)
        if new_d:
            word_pattern = re.compile(r'\b' + re.escape(w) + r'\b', re.IGNORECASE)
            masked = word_pattern.sub('*' * len(w), new_d)
            item['definition'] = masked
            count += 1
            print(f"Fixed {w}")
        time.sleep(0.1)

with open('words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, indent=4)
print(f"Total fixed via API: {count}")
