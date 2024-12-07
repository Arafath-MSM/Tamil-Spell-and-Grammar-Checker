from spell_checker import load_dictionary, spell_checker
from grammar_checker import check_subject_verb

def run_tests():
    tamil_words = load_dictionary()

    # Test Spell Checker
    test_sentence = "புத்தகம் அந்த"
    print("Original:", test_sentence)
    print("Corrected:", spell_checker(test_sentence, tamil_words))

    # Test Grammar Checker
    grammar_sentence = "அவர்கள் வருகிறான்"
    print("Original:", grammar_sentence)
    print("Corrected:", check_subject_verb(grammar_sentence))
