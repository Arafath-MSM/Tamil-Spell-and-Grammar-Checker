import re
from indicnlp.tokenize.indic_tokenize import trivial_tokenize
from collections import defaultdict

class RuleBasedChecker:
    def __init__(self):
        self.tamil_words = self._load_tamil_dictionary()
        
        # Expanded grammar rules with patterns and corrections
        self.grammar_rules = {
            'subject_verb_agreement': [
                (r'நான்.*கிறார்கள்', 'First person singular with plural verb', r'நான்.*கிறேன்'),
                (r'நான்.*கிறான்', 'First person singular with singular masculine verb', r'நான்.*கிறேன்'),
                (r'நான்.*கிறாள்', 'First person singular with feminine singular verb', r'நான்.*கிறேன்'),
                (r'நாங்கள்.*கிறான்', 'First person plural with singular masculine verb', r'நாங்கள்.*கிறோம்'),
                (r'நாங்கள்.*கிறாள்', 'First person plural with feminine singular verb', r'நாங்கள்.*கிறோம்'),
                (r'அவள்.*கிறான்', 'Third person singular feminine with masculine verb', r'அவள்.*கிறாள்'),
                (r'அவன்.*கிறேன்', 'Third person singular masculine with first-person verb', r'அவன்.*கிறான்'),
            ],
            'spelling_patterns': [
                (r'சல்', 'Possible misspelling of செல்', 'செல்'),
                (r'பயன்படுத்திறேன்', 'Possible misspelling of பயன்படுத்துகிறேன்', 'பயன்படுத்துகிறேன்'),
            ]
        }

    def _load_tamil_dictionary(self):
        basic_dictionary = {
            'நான்': 'pronoun',
            'நீ': 'pronoun',
            'நாங்கள்': 'pronoun',
            'அவன்': 'pronoun',
            'அவள்': 'pronoun',
            'பள்ளி': 'noun',
            'பள்ளிக்கு': 'noun',
            'புது': 'adjective',
            'புத்தகம்': 'noun',
            'பழைய': 'adjective',
            'பேனா': 'noun',
            'மேசையில்': 'noun',
            'போகிறேன்': 'verb',
            'செல்கிறேன்': 'verb',
            'செல்கிறான்': 'verb',
            'செல்கிறாள்': 'verb',
            'படிக்கிறான்': 'verb',
            'வைக்கிறான்': 'verb',
            'பயன்படுத்துகிறேன்': 'verb',
        }
        return basic_dictionary

    def split_sentences(self, text):
        sentences = re.split('[.!?।]', text)
        return [s.strip() for s in sentences if s.strip()]

    def check_spelling(self, text):
        corrections = []
        words = trivial_tokenize(text)
        
        for word in words:
            for pattern, msg, correction in self.grammar_rules['spelling_patterns']:
                if re.search(pattern, word):
                    corrections.append(('spelling', msg, word, correction))
            
            if word not in self.tamil_words and not any(char.isdigit() for char in word):
                corrections.append(('spelling', f'Unknown word: {word}', word, None))
        
        return corrections

    def check_grammar(self, text):
        corrections = []
        sentences = self.split_sentences(text)
        
        for sentence in sentences:
            for pattern, error_msg, correction in self.grammar_rules['subject_verb_agreement']:
                if re.search(pattern, sentence):
                    corrected_sentence = re.sub(pattern, correction, sentence)
                    corrections.append(('grammar', error_msg, sentence, corrected_sentence))
        
        return corrections

    def apply_corrections(self, text, corrections):
        corrected_text = text
        for _, _, original, correction in corrections:
            if correction:
                corrected_text = corrected_text.replace(original, correction)
        return corrected_text

    def check_text(self, text):
        spelling_corrections = self.check_spelling(text)
        grammar_corrections = self.check_grammar(text)
        all_corrections = spelling_corrections + grammar_corrections
        corrected_text = self.apply_corrections(text, all_corrections)
        return all_corrections, corrected_text

def get_correction_suggestions(self, text):
    try:
        corrections = []
        # Run spelling checks
        spelling_corrections = self.check_spelling(text)
        corrections.extend(spelling_corrections)
        
        # Run grammar checks
        grammar_corrections = self.check_grammar(text)
        corrections.extend(grammar_corrections)
        
        # Format corrections into suggestions
        suggestions = []
        for _, msg, original, correction in corrections:
            if correction:
                suggestions.append(f"{original} → {correction} ({msg})")
            else:
                suggestions.append(f"{original} ({msg})")
        
        return suggestions
    except Exception as e:
        return [f"Error generating suggestions: {str(e)}"]


# # Example usage:
# checker = RuleBasedChecker()
# sentences = [
#     "நான் பள்ளிக்கு சல்கிறேன்.",
#     "அவள் புதிய புத்தகம் படிக்கிறான்.",
#     "நாங்கள் பழைய பேனா மேசையில் வைக்கிறாள்.",
#     "அவன் பள்ளிக்கு போகிறேன் சல்கிறான்.",
#     "நான் பெரிய கண்ணி பயன்படுத்திறேன்."
# ]

# for sentence in sentences:
#     errors, corrected = checker.check_text(sentence)
#     print(f"Original: {sentence}")
#     print(f"Errors: {errors}")
#     print(f"Corrected: {corrected}")
#     print("-" * 50)
