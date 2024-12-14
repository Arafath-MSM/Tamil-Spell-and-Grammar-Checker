from spellchecker import SpellChecker


# Initialize SpellChecker with custom Tamil dictionary
spell = SpellChecker(language=None)  # We use 'None' to load a custom dictionary
spell.word_frequency.load_text_file('tamil_dictionary.txt')

def spell_check(paragraph):
    """
    Detect and correct spelling errors in a Tamil paragraph.
    :param paragraph: Input paragraph in Tamil (str)
    :return: Tuple of (corrections dictionary, corrected paragraph)
    """
    words = paragraph.split()  # Tokenize paragraph into words
    corrections = {}  # To store the corrections made

    # Identify misspelled words and suggest corrections
    for word in words:
        if word not in spell:
            # Get the best correction or fallback to the original word
            correction = spell.correction(word)
            if correction:
                corrections[word] = correction

    # Construct the corrected paragraph
    corrected_paragraph = " ".join(
        [corrections.get(word, word) for word in words]
    )
    return corrections, corrected_paragraph


# Test Example
paragraph = "இந்தது என்னள பாயிரம் உள்ளது."  # Example input with spelling errors
corrections, corrected_text = spell_check(paragraph)

# Print results
print("Original Paragraph:", paragraph)
print("Corrections:", corrections)
print("Corrected Paragraph:", corrected_text)
