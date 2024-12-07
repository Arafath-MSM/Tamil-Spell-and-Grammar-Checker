from leven import levenshtein

def load_dictionary():
    with open('words.txt', 'r', encoding='utf-8') as file:
        return set(file.read().splitlines())

def get_closest_word(word, dictionary):
    return min(dictionary, key=lambda x: levenshtein(word, x))

def spell_checker(sentence, dictionary):
    corrected = []
    words = sentence.split()
    for word in words:
        if word not in dictionary:
            corrected.append(get_closest_word(word, dictionary))
        else:
            corrected.append(word)
    return ' '.join(corrected)
