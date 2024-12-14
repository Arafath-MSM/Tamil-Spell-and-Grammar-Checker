from spell_checker import load_dictionary, spell_checker
from grammar_checker import check_subject_verb


if __name__ == "__main__":
    tamil_words = load_dictionary()

    # Input paragraph
    paragraph = "அவர்கள் வருகிறான். புத்தகம் அந்த"
    print("Original Paragraph:", paragraph)

    # Spell Check
    corrected = spell_checker(paragraph, tamil_words)
    print("After Spell Check:", corrected)

    # Grammar Check
    final_output = check_subject_verb(corrected)
    print("Final Output:", final_output)
