# grammar_checker.py
import re

def check_subject_verb_agreement(sentence):
    """Check for subject-verb agreement errors."""
    # Example: "அவர்கள் வருகிறான்" should be "அவர்கள் வருகிறார்கள்"
    if 'அவர்கள்' in sentence and 'வருகிறான்' in sentence:
        return sentence.replace('வருகிறான்', 'வருகிறார்கள்')
    return sentence

def check_word_order(sentence):
    """Check for word order errors."""
    # Example: "புத்தகம் அந்த" should be "அந்த புத்தகம்"
    if 'புத்தகம்' in sentence and 'அந்த' in sentence:
        return re.sub(r'புத்தகம் அந்த', 'அந்த புத்தகம்', sentence)
    return sentence

def grammar_check(text):
    sentences = text.split('.')  # Basic split; can be improved with more advanced NLP
    checked_text = []
    
    for sentence in sentences:
        sentence = check_subject_verb_agreement(sentence)
        sentence = check_word_order(sentence)
        checked_text.append(sentence)
    
    return '. '.join(checked_text)
