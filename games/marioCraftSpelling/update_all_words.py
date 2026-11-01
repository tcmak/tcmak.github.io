import os
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

CACHE_FILE = 'definitions_cache.json'
WORDS_FILE = 'words.json'
API_KEY = os.environ.get('OPENAI_API_KEY')

if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not found.")

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def is_self_referential(word, definition):
    w = word.lower().strip()
    d = definition.lower()
    
    # 1. Exact word boundary check
    pattern = r'\b' + re.escape(w) + r'\b'
    if re.search(pattern, d):
        return True
    
    # 2. Inflections: plurals, -ed, -ing, -ly, -er, -est
    pattern_infl = r'\b' + re.escape(w) + r'(s|es|d|ed|ing|ly|er|est)?\b'
    if re.search(pattern_infl, d):
        return True
        
    # 3. If word ends with 'e', check dropping 'e' + ing/ed
    if w.endswith('e') and len(w) > 3:
        stem = w[:-1]
        pattern_stem = r'\b' + re.escape(stem) + r'(ing|ed)\b'
        if re.search(pattern_stem, d):
            return True
            
    # 4. If word ends with 'y', check 'ies', 'ied'
    if w.endswith('y') and len(w) > 3:
        stem = w[:-1]
        pattern_y = r'\b' + re.escape(stem) + r'(ies|ied)\b'
        if re.search(pattern_y, d):
            return True
            
    # 5. If word is plural (ends with 's'), check singular
    if w.endswith('s') and len(w) > 3:
        singular = w[:-1]
        if re.search(r'\b' + re.escape(singular) + r'\b', d):
            return True
            
    # 6. If word ends with 'ing', check root
    if w.endswith('ing') and len(w) > 5:
        root = w[:-3]
        if re.search(r'\b' + re.escape(root) + r'\b', d):
            return True

    return False

def call_openai(prompt, max_retries=5):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'response_format': {'type': 'json_object'}
    }
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode('utf-8'))
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                content = data['choices'][0]['message']['content']
                return json.loads(content)
        except Exception as e:
            wait_time = (2 ** attempt) + 1
            print(f"Error on attempt {attempt+1}: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            
    raise RuntimeError("Failed to complete OpenAI request after max retries.")

def generate_batch(batch):
    prompt = f'''You are writing kid-friendly clue definitions for an educational word guessing game (MarioCraft) played by 8-year-olds (Grade 3).
For each given word, write a simple, fun, easy-to-understand clue or definition that allows an 8-year-old child to guess the word without giving the word away.

CRITICAL RULES:
1. NEVER include the target word itself, or any direct variation/inflection (plurals, -ing, -ed, -er, root form, etc.) in the definition!
2. Do NOT give away the word directly (do NOT say "If you X someone...", do NOT say "A X is...", do NOT use X).
3. Provide a clear clue or kid-friendly definition describing what it is, what it does, what it looks like, or where you find it.
4. Match the provided emoji and category.
5. Keep each definition concise (1 short sentence, around 6 to 18 words), properly capitalized and ending with a period.
6. Highly age-appropriate, wholesome, and educational for an 8-year-old child.

Input list of items:
{json.dumps(batch, indent=2)}

Respond ONLY with a JSON object in this format:
{{"items": [{{"word": "ACT", "definition": "Doing something, like playing a fun character on stage."}}]}}
'''
    result = call_openai(prompt)
    return result.get('items', [])

def fix_single_word(item):
    prompt = f'''You are writing a kid-friendly clue definition for an educational word guessing game (MarioCraft) for 8-year-olds.
Word to guess: "{item['word']}"
Emoji: {item['emoji']}
Category: {item['category']}

CRITICAL: You MUST NOT use the word "{item['word']}" or ANY variation of it anywhere in the definition.
Do NOT say "If you {item['word'].lower()}..." or "A {item['word'].lower()} is...".
Write a fun, simple 1-sentence clue (8-16 words) that lets an 8-year-old guess the word "{item['word']}".

Respond ONLY with a JSON object: {{"word": "{item['word']}", "definition": "..."}}
'''
    res = call_openai(prompt)
    return res.get('definition', '')

def main():
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words_data = json.load(f)

    cache = load_cache()
    print(f"Loaded {len(cache)} cached definitions out of {len(words_data)} total words.")

    # Filter words needing generation or that fail validation
    needed = []
    for item in words_data:
        w = item['word']
        if w not in cache or is_self_referential(w, cache[w]):
            needed.append({
                'word': w,
                'emoji': item.get('emoji', '❓'),
                'category': item.get('category', 'Vocabulary')
            })

    print(f"Words needing generation or fixing: {len(needed)}")

    BATCH_SIZE = 35
    batches = [needed[i:i + BATCH_SIZE] for i in range(0, len(needed), BATCH_SIZE)]
    print(f"Total batches to process: {len(batches)}")

    if batches:
        completed = 0
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_batch = {executor.submit(generate_batch, b): b for b in batches}
            for future in as_completed(future_to_batch):
                batch_items = future_to_batch[future]
                try:
                    generated_items = future.result()
                    for item in generated_items:
                        w = item.get('word')
                        d = item.get('definition', '').strip()
                        if w and d:
                            cache[w] = d
                    completed += 1
                    save_cache(cache)
                    print(f"[{completed}/{len(batches)}] Saved batch. Total cached: {len(cache)}")
                except Exception as e:
                    print(f"Batch failed: {e}")

    # Validation and individual fix phase
    print("\n--- Running Validation Check ---")
    invalid_words = []
    for item in words_data:
        w = item['word']
        d = cache.get(w, '')
        if not d or is_self_referential(w, d):
            invalid_words.append(item)

    print(f"Found {len(invalid_words)} words needing individual fix.")
    for idx, item in enumerate(invalid_words):
        w = item['word']
        fixed_def = fix_single_word(item)
        if fixed_def and not is_self_referential(w, fixed_def):
            cache[w] = fixed_def
            print(f"[{idx+1}/{len(invalid_words)}] Fixed {w}: {fixed_def}")
        else:
            # Try once more with stronger instruction
            print(f"Retry fixing {w}...")
            fixed_def = fix_single_word(item)
            cache[w] = fixed_def
            print(f"[{idx+1}/{len(invalid_words)}] Fixed {w}: {fixed_def}")
        save_cache(cache)

    # Final verification
    print("\n--- Final Verification ---")
    still_invalid = []
    for item in words_data:
        w = item['word']
        d = cache.get(w, '')
        if not d:
            still_invalid.append((w, "MISSING"))
        elif is_self_referential(w, d):
            still_invalid.append((w, d))

    print(f"Remaining self-referential or missing: {len(still_invalid)}")
    for w, d in still_invalid:
        print(f"STILL INVALID: {w} -> {d}")

    # Update words.json
    print("\n--- Updating words.json ---")
    updated_count = 0
    for item in words_data:
        w = item['word']
        if w in cache:
            # Ensure clean formatting: capitalized and ends with period
            clean_def = cache[w].strip()
            if clean_def and not clean_def.endswith(('.', '!', '?')):
                clean_def += '.'
            item['definition'] = clean_def
            updated_count += 1

    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully updated {updated_count} words in {WORDS_FILE}!")

if __name__ == '__main__':
    main()
