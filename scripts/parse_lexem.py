import csv
import re
import os 

csv_file_HD = 'LexemeFreqCorpus_PartofM1_HumanDisa.csv'
csv_file_M1 = 'LexemeFreqCorpus_M1.csv'

# DEFAULT_CORPSE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpse.csv')
with open(DEFAULT_CORPSE, mode='r', encoding='utf-16', newline='') as f:
    data = csv.reader(f, dialect='excel')
    corpse = { line[0] : int(line[1]) for line in data if line[0].isalpha() }

def get_word_frequency_other_dictionary(word):
    if word in corpse:
        return corpse[word]
    else:
        return 0

def generate_combinations(word):
    results = []

    def backtrack(current_word, index):
        if index == len(word):
            results.append(current_word)
            return
        
        if word[index] == '&':
            # Include the character before '&' and proceed
            backtrack(current_word[:-1] + word[index - 1], index + 1)
            # Exclude the character before '&' and proceed
            backtrack(current_word[:-1], index + 1)
        else:
            # Normal character, include and proceed
            backtrack(current_word + word[index], index + 1)

    # Start backtracking from the beginning of the word
    backtrack('', 0)

    return results


def is_hebrew_word_plus(word):
    # Regular expression to match Hebrew characters and &
    hebrew_pattern = re.compile(r'[\u0590-\u05FF&41635807]+')
    
    # Check if all characters in the word are Hebrew or &
    return all([hebrew_pattern.match(char) for char in word])

def translate(word):
    if '4' in word:
        word_v1 = word.replace('4', 'ב')
        word_v2 = word.replace('4', 'ו')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '7' in word:
        word_v1 = word.replace('7', 'ה')
        word_v2 = word.replace('7', 'א')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '0' in word:
        word_v1 = word.replace('0', 'ז')
        word_v2 = word.replace('0', 'ס')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '6' in word:
        word_v1 = word.replace('6', 'נ')
        word_v2 = word.replace('6', 'מ')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '3' in word:
        word_v1 = word.replace('3', 'ס')
        word_v2 = word.replace('3', 'צ')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '8' in word:
        word_v1 = word.replace('8', 'ס')
        word_v2 = word.replace('8', 'צ')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2
    if '5' in word:
        word_v1 = word.replace('5', 'ת')
        word_v2 = word.replace('5', 'ט')
        word = word_v1 if get_word_frequency_other_dictionary(word_v1) > get_word_frequency_other_dictionary(word_v2) else word_v2

    return word.replace('1', 'ק')

def get_base_words(line):
    words = line.split("+")
    if 'ProperName' in words: # remove names
        return None
    for word in words:
        if is_hebrew_word_plus(word):
            combinations = generate_combinations(word)
            return [translate(combination) for combination in combinations]
    return None


def get_word_dict(csv_file):
# Initialize an empty dictionary to store parsed data
    word_dict = {}

    # Open the CSV file and read it
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:  # 'utf-8-sig' handles the UTF-8 BOM if present
        csv_reader = csv.reader(file, delimiter=',')
        
        # Skip the first line which contains metadata
        next(csv_reader)
        next(csv_reader)
        
        # Iterate over each row in the CSV reader
        for row in csv_reader:
            if len(row) >= 3 and row[0]:  # Ensure row has at least 3 elements (WORD, FREQ, FREQ_LOG)
                word = row[0].strip()  # Get the word (strip removes extra spaces)
                freq = int(row[1].strip())  # Get the frequency as integer
                freq_log = float(row[2].strip())  # Get the log frequency as float
                base_words = get_base_words(word)
                if base_words is not None:
                    for base_word in base_words:
                        if word_dict.get(base_word) is None:
                            # Create a dictionary entry with word as key and parameters as value
                            word_dict[base_word] = {'details': [word], 'FREQ': freq, 'FREQ_LOG': freq_log}
                        else:
                            # Update the existing dictionary entry with new parameters
                            word_dict[base_word]['FREQ'] += freq
                            word_dict[base_word]['FREQ_LOG'] += freq_log
                            word_dict[base_word]['details'].append(word)

    # Now word_dict contains the parsed data
    return word_dict

word_dict_HD = get_word_dict(csv_file_HD)
word_dict_M1 = get_word_dict(csv_file_M1)
