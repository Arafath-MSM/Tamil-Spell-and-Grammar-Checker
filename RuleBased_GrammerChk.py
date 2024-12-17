import re

def check_subject_verb_agreement(sentence): #ss
    """
    Detect and correct subject-verb agreement errors.
    :param sentence: Input sentence (str)
    :return: Corrected sentence (str)
    """
    corrections = []
    
    # Simple rule: If subject is "அவன்" or "அவள்", verb must end with "ன்" or "ள்"
    patterns = [
        (r"(அவன்|அவள்)\s+(\w+?)(?!ன்|ள்)", r"\1 \2ன்"),
        (r"(நாங்கள்|நாம்)\s+(\w+?)(?!ம்)", r"\1 \2ம்")
    ]
    
    for pattern, replacement in patterns:
        sentence, count = re.subn(pattern, replacement, sentence)
        if count > 0:
            corrections.append((pattern, replacement))
    
    return sentence, corrections

# Test Example
sentence = "அவன் போக"
corrected_sentence, corrections = check_subject_verb_agreement(sentence)

print("Original Sentence:", sentence)
print("Corrected Sentence:", corrected_sentence)
print("Corrections Applied:", corrections)
