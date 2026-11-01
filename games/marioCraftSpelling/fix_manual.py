import json

manual = {
    'OURS': 'Belonging to or associated with us.',
    'ENSURE': 'To make certain that something will occur or be the case.',
    'EVERYBODY': 'Every person.',
    'JEWELLERY': 'Personal ornaments, such as necklaces, rings, or bracelets.'
}

with open('words.json', 'r') as f:
    words = json.load(f)

for item in words:
    if item['word'] in manual:
        item['definition'] = manual[item['word']]

with open('words.json', 'w') as f:
    json.dump(words, f, indent=4)
