# spell_checker.py
from Levenshtein import distance as levenshtein
import langid
from load_dictionary import load_tamil_dictionary

tamil_dict = load_tamil_dictionary()

def is_tamil_word(word):
    return word in tamil_dict

def suggest_correction(word):
    """Suggest the closest match for the misspelled word based on Levenshtein distance."""
    suggestions = [(w, levenshtein(word, w)) for w in tamil_dict]
    sorted_suggestions = sorted(suggestions, key=lambda x: x[1])
    return sorted_suggestions[0][0] if sorted_suggestions else word

def spell_checker(text):
    words = text.split()  # Basic split; you can improve tokenization with NLP libraries
    corrected_text = []
    
    for word in words:
        if not is_tamil_word(word):
            corrected_text.append(suggest_correction(word))
        else:
            corrected_text.append(word)
    
    return ' '.join(corrected_text)
