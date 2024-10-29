import pandas as pd
import os
import csv
import tqdm
from bigrams import (
    ngrams_from_sentences,
    generate_ngrams,
    is_devanagari,
    remove_chars_with_regex,
    remove_emoji,
    remove_words_with_domain,
    has_indic_chars,
    has_greek_letters,
    remove_special_characters
)

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

# Unicode ranges for different languages
unicodes = {'as': (0x0980, 0x09FF), 'mai': (0x0900, 0x097F), 'gu': (0x0A80, 0x0AFF), 'bn': (0x0980, 0x09FF),
            'hi': (0x0900, 0x097F), 'kn': (0x0C80, 0x0CFF), 'ks': (0x0600, 0x06FF), 'ml': (0x0D00, 0x0D7F),
            'mr': (0x0900, 0x097F), 'mni': (0xABC0, 0xABFF), 'nep': (0x0900, 0x097F), 'or': (0x0B00, 0x0B7F),
            'pa': (0x0A00, 0x0A7F), 'san': (0x0900, 0x097F), 'sat': (0x1C50, 0x1C7F), 'sd': (0x0900, 0x097F),
            'ta': (0x0B80, 0x0BFF) , 'te': (0x0C00, 0x0C7F), 'ur': (0x0600, 0x06FF), 'brx':(0x0900, 0x097F),
            'kok':(0x0900, 0x097F), 'doi': (0x0900, 0x097F)}

ben_unicode_skip_list = ['\u0984', '\u098d', '\u098e', '\u0991', '\u0992', '\u09a9', '\u09b1', '\u09b3', '\u09b4', '\u09b5', '\u09ba', '\u09bb', '\u09c5', '\u09c6', '\u09c9', '\u09ca', '\u09cf', '\u09d0', '\u09d1', '\u09d2', '\u09d3', '\u09d4', '\u09d5', '\u09d6', '\u09d8', '\u09d9', '\u09da', '\u09db', '\u09de', '\u09e4', '\u09e5', '\u09ff', '\u200c']

hf_bigrams_file = '/home/tts/ttsteam/repos/oov_plus_plus/vits_hi_cha/manifests_old/hi-ivr/hf_bigrams.csv'
lf_bigrams_file = '/home/tts/ttsteam/repos/oov_plus_plus/vits_hi_cha/manifests_old/hi-ivr/lf_bigrams.csv'

hf_bigrams = set()
lf_bigrams = set()

new_df_hf_list = []
new_df_lf_list = []

hf_bigrams_df = pd.read_csv(hf_bigrams_file, header=None)
lf_bigrams_df = pd.read_csv(lf_bigrams_file, header=None)

print('Storing high frequency bigrams')
for i, bigram in tqdm.tqdm(hf_bigrams_df.iterrows()):
    hf_bigrams.add(bigram[0])

print('Storing low frequency bigrams')
for i, bigram in tqdm.tqdm(lf_bigrams_df.iterrows()):
    lf_bigrams.add(bigram[0])

print('High frequency bigrams: ', len(hf_bigrams))
print('Low frequency bigrams: ', len(lf_bigrams))

sentence_file = '/home/tts/ttsteam/repos/oov_plus_plus/sentences/hin/all_sentences.csv'

# sentences = pd.read_csv(sentence_file)
# with open(sentence_file, 'r') as f:
#     sentences = f.readlines()
sentences = []
col1 = []
col3 = []
col4 = []
with open(sentence_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        col1.append(row[0])
        sentences.append(row[1])
        col3.append(row[2])
  

def find_bigrams(i, sentence_bigrams_, hf_bigrams_, new_df_hf_list_):
    remove_hf_bigrams = []
    for bigram in hf_bigrams_:
        if bigram in sentence_bigrams_:
            remove_hf_bigrams.append(bigram)
    if remove_hf_bigrams != []:
        new_df_hf_list_.append((col1[i], sentences[i].replace('\n', ''), col3[i], remove_hf_bigrams))
        for bigram in remove_hf_bigrams:
            hf_bigrams_.remove(bigram)

for i in range(len(sentences)):
    if len(sentences[i].split(' ')) >= 3:
        bigrams = ngrams_from_sentences(sentences[i], 2, 'mr')
        sentence_bigrams = []
        for bigram in bigrams:
            if is_devanagari(bigram):
                sentence_bigrams.append(bigram)
    
    if sentence_bigrams!=[]:
        find_bigrams(i, sentence_bigrams, hf_bigrams, new_df_hf_list)
        find_bigrams(i, sentence_bigrams, lf_bigrams, new_df_lf_list)

    if not hf_bigrams and not lf_bigrams:
        print('all bigrams found! :)')


pd.DataFrame(new_df_hf_list).to_csv('/home/tts/ttsteam/repos/oov_plus_plus/sentences/hin/hf_bigrams_sentences.csv', header=None, index=False)
pd.DataFrame(new_df_lf_list).to_csv('/home/tts/ttsteam/repos/oov_plus_plus/sentences/hin/lf_bigrams_sentences.csv', header=None, index=False)
