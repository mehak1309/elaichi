import pandas as pd
import os
import re
import string

# unicode values in this range will be discarded
lang_number_dict = {'as': '[\u09E6-\u09EF]+',
                    'bn': '[\u09E6-\u09EF]+',
                    'hi': '[\u0966-\u096F]+',
                    'mr': '[\u0966-\u096F]+',
                    'ta': '[\u0BE6-\u0BEF]+',
                    'te': '[\u0C66-\u0C6F]+',
                    'kn': '[\u0CE6-\u0CEF]+',
                    'ml': '[\u0D66-\u0D6F]+',
                    'or': '[\u0B66-\u0B6F]+',
                    'pa': '[\u0A66-\u0A6F]+',
                    'gu': '[\u0AE6-\u0AEF]+',
                    'mni': '[\uABF0-\uABF9]+',
                    'sa': '[\u0966-\u096F]+',
                    'ks': '[\u0660-\u0669]+',
                    'ur': '[\u0660-\u0669]+',
                    'mai': '[\u0966-\u096F]+',
                    'sd': '[\u0966-\u096F]+',
                    'nep': '[\u0966-\u096F]+',
                    'brx': '[\u0966-\u096F]+',
                    'kok': '[\u0966-\u096F]+',
                    'sat': '[\u1C50-\u1C59]+',}

def is_devanagari(bigram):
    # Define Devanagari Unicode range
    devanagari_range = (0x0900, 0x097F)
    
    # Check each character in the bigram
    for char in bigram:
        if not (devanagari_range[0] <= ord(char) <= devanagari_range[1]):
            return False
    return True

# Unicode ranges for different languages
unicodes = {'as': (0x0980, 0x09FF), 'mai': (0x0900, 0x097F), 'gu': (0x0A80, 0x0AFF), 'bn': (0x0980, 0x09FF),
            'hi': (0x0900, 0x097F), 'kn': (0x0C80, 0x0CFF), 'ks': (0x0600, 0x06FF), 'ml': (0x0D00, 0x0D7F),
            'mr': (0x0900, 0x097F), 'mni': (0xABC0, 0xABFF), 'nep': (0x0900, 0x097F), 'or': (0x0B00, 0x0B7F),
            'pa': (0x0A00, 0x0A7F), 'san': (0x0900, 0x097F), 'sat': (0x1C50, 0x1C7F), 'sd': (0x0900, 0x097F),
            'ta': (0x0B80, 0x0BFF) , 'te': (0x0C00, 0x0C7F), 'ur': (0x0600, 0x06FF), 'brx':(0x0900, 0x097F),
            'kok':(0x0900, 0x097F), 'doi': (0x0900, 0x097F)}

ben_unicode_skip_list = ['\u0984', '\u098d', '\u098e', '\u0991', '\u0992', '\u09a9', '\u09b1', '\u09b3', '\u09b4', '\u09b5', '\u09ba', '\u09bb', '\u09c5', '\u09c6', '\u09c9', '\u09ca', '\u09cf', '\u09d0', '\u09d1', '\u09d2', '\u09d3', '\u09d4', '\u09d5', '\u09d6', '\u09d8', '\u09d9', '\u09da', '\u09db', '\u09de', '\u09e4', '\u09e5', '\u09ff', '\u200c']

# Removes characters specified in the Bengali skip list
def remove_chars_with_regex(input_string):
    pattern = '[' + re.escape(''.join(ben_unicode_skip_list)) + ']'
    return re.sub(pattern, '', input_string)

# Removes emojis from the input string
def remove_emoji(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

# Removes words containing specified domains from the input string.
def remove_words_with_domain(input_string):
    pattern = re.compile(r'\b(?:www\.)?\w*\.((com)|(org)|(gov.in)).?\b')
    result = re.sub(pattern, '', input_string)
    return result

# Checks if the input string contains characters within the specified Unicode range
def has_indic_chars(input_string, unicode_range):
    for char in input_string:
        if char.isnumeric() or char.isspace() or char in string.punctuation or char in string.ascii_letters:
            continue
        if unicode_range[0] <= ord(char) <= unicode_range[1]:
            continue
        else:
            return False
    return True

# Checks if the input string contains Greek letters
def has_greek_letters(input_string):
    greek_pattern = re.compile('[Α-Ωα-ω]+')
    return bool(greek_pattern.search(input_string))

# Cleans the input text based on language-specific rules
def clean_text(text, language):
    replace_patterns = [r'\u200d', r'\u200c', r'\ufeff', r'\u200b', r'‎', r'██', r'', r'￼', r'ʼʼ', r'‘‘', r'‘', r'ʼ', r'۔', r'\. \.', r'−', r'ꠞ', r'·', r'–', r'®', r'°', r'₹', r'£', r'&quot', r'Î²', r'॥', r'‚', r'…', r'”', r'“', r'¸']
    for pattern in replace_patterns:
        text = re.sub(pattern, ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = remove_emoji(text)
    text = remove_words_with_domain(text)
    text = text.replace('"', '')
    if all(char not in text for char in ['ʋ', 'ɐ', 't̺', 'ɻ', 'ā', 'â', 'Ã', 'Â']) and not (language == 'hi' and 'ऽ' in text):
        return text
    return ''

# Removes special characters from the input string
def remove_special_characters(text, language):
    text = re.sub(r'[a-zA-Z]+', '', text)
    text = re.sub(r'[()\[\]{}!@#$%&*~/؟\\=+x\/\-⁄_¯¶◾■✓·±Δ<>|•●→,←^“”.?‡Å;:ÃÂ…−á¹٪،≤„¡©¥«»﻿…¹‡|॥−?;:‚‡ÅÃÂ…−٪،¡≤«»©¥„﻿…।¹‡|॥−á¹`–—°ʋɐːt̺upuɻɐā‏‎؜āαβÎ²￼â€™武俠俠小小說慧可武俠俠小小說®ᱻ¢£¤¦§¨¬´¸×¿†‰″₹↑↓↵⇒∩≡Ⓡ☞❀？۔؛٬٫٭۔۔۔]+', '', text)
    if language != "sd":
        text = re.sub(r'[‘”"”“\'`’′‘’]+', '', text)
    text = re.sub(r'\s+', ' ', text) # remove extra spaces
    text = re.sub(r'[1234567890]+', '', text)
    if (language == "bn" or language == "as"):
        text = remove_chars_with_regex(text)
    if language in lang_number_dict:
        text = re.sub(lang_number_dict[language], '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Generate n-grams for the word
def generate_ngrams(word, n):
    ngrams = []
    if (len(word)>=n):
        ngrams = ([''.join(word[i:i + n]) for i in range(len(word) - n + 1) if len(word[i:i + n]) == n])
    return ngrams

# Generate n-grams for the sentence
def ngrams_from_sentences(sentence, n, language):
    sentence = clean_text(sentence, language)
    sentence = remove_special_characters(sentence, language) 
    sentence.strip()
    words = (sentence.split())
    all_ngrams = []
    for word in words:
        all_ngrams.extend(generate_ngrams(word,n))
    return all_ngrams