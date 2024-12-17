from spell_checker import load_tamil_dictionary, spell_checker
from grammar_checker import grammar_check

# Test spell checker
def test_spell_checker():
    text = "அவர்கள் வருகிறான்"
    corrected_text = spell_checker(text)
    print(f"Original: {text}")
    print(f"Corrected: {corrected_text}")

# Test grammar checker
def test_grammar_checker():
    sentence = "புத்தகம் அந்த"
    corrected_sentence = grammar_check(sentence)
    print(f"Original: {sentence}")
    print(f"Corrected: {corrected_sentence}")

if __name__ == "__main__":
    test_spell_checker()
    test_grammar_checker()
