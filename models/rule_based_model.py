import re
from indicnlp.tokenize.indic_tokenize import trivial_tokenize

class RuleBasedChecker:
    def __init__(self):
        self.tamil_words = self._load_tamil_dictionary()
        
        # Updated grammar rules with different patterns
        self.grammar_rules = {
            'subject_verb_agreement': [
                (r'அவன்.*செல்கிறான்', 'Third person singular with informal verb'),
                (r'அவள்.*செல்கிறாள்', 'Third person singular feminine with informal verb'),
                (r'நாங்கள்.*செல்கிறோம்', 'First person plural with appropriate verb'),
                (r'நீ.*செல்கிறாய்', 'Second person singular with informal verb'),
                (r'அவர்.*செல்கிறார்', 'Honorific subject with formal verb')
            ],
            'spelling_patterns': [
                (r'சொல்', 'Possible misspelling of சொல்'),
                (r'பாஷை', 'Possible misspelling of மொழி'),
                (r'எங்கே', 'Possible misspelling of எங்கு')
            ],
            'word_spacing': [
                (r'\w+க்கு\w+', 'Missing space before க்கு'),
                (r'\w+ல்\w+', 'Missing space before ல்'),
                (r'\w+முடன்\w+', 'Missing space before முடன்')
            ]
        }

    def _load_tamil_dictionary(self):
        basic_dictionary = {
            'அவன்': 'pronoun',
            'அவள்': 'pronoun',
            'நாங்கள்': 'pronoun',
            'பள்ளி': 'noun',
            'பள்ளிக்கு': 'noun',
            'செல்கிறான்': 'verb',
            'செல்கிறாள்': 'verb',
            'செல்கிறோம்': 'verb',
            'பாடல்': 'noun',
            'பாடுகிறாள்': 'verb',
            'ஆசிரியர்': 'noun',
            'நல்ல': 'adjective',
            'மொழி': 'noun',
            'கற்றுக்': 'verb',
            'கொடுக்கிறார்': 'verb'
        }
        
        try:
            with open("data/tamil_dictionary.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            basic_dictionary[parts[0]] = parts[1]
        except FileNotFoundError:
            pass  # Use the basic dictionary if the file is not found
            
        return basic_dictionary

    def split_sentences(self, text):
        # Simple sentence splitting based on punctuation
        sentences = re.split('[.!?।]', text)
        return [s.strip() for s in sentences if s.strip()]

    def check_spelling(self, text):
        errors = []
        words = trivial_tokenize(text)
        
        for word in words:
            # Check spelling patterns
            for pattern, msg in self.grammar_rules['spelling_patterns']:
                if re.match(pattern, word):
                    errors.append(('spelling', msg, word))
            
            # Check against dictionary
            if word not in self.tamil_words and not any(char.isdigit() for char in word):
                errors.append(('spelling', f'Unknown word: {word}', word))
            
            # Check word spacing
            for pattern, msg in self.grammar_rules['word_spacing']:
                if re.match(pattern, word):
                    errors.append(('spelling', msg, word))
        
        return errors

    def check_grammar(self, text):
        errors = []
        sentences = self.split_sentences(text)
        
        for sentence in sentences:
            # Check subject-verb agreement
            for pattern, error_msg in self.grammar_rules['subject_verb_agreement']:
                if re.search(pattern, sentence):
                    errors.append(('grammar', error_msg, sentence))
        
        return errors

    def check_text(self, text):
        try:
            # Run spelling checks
            spelling_errors = self.check_spelling(text)
            
            # Run grammar checks
            grammar_errors = self.check_grammar(text)
            
            # Combine all errors
            all_errors = spelling_errors + grammar_errors
            
            # If no errors found, return empty list
            if not all_errors:
                return []
                
            return all_errors
            
        except Exception as e:
            return [('error', f'Error in text analysis: {str(e)}', text)]