# main.py
from spell_checker import spell_checker
from grammar_checker import grammar_checker

def process_text(text):
    """Process text with both spell checker and grammar checker."""
    # First apply spell checker
    text_with_spelling_corrections = spell_checker(text)
    # Then apply grammar checker
    corrected_text = grammar_checker(text_with_spelling_corrections)
    
    return corrected_text

# Test with a sample Tamil text
if __name__ == "__main__":
    input_text = "அவர்கள் வருகிறான் புத்தகம் அந்த"
    print("Original Text:", input_text)
    corrected_text = process_text(input_text)
    print("Corrected Text:", corrected_text)
