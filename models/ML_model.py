from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import re


class StatisticalChecker:
    def __init__(self):
        # Initialize multiple vectorizers for different features
        self.word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), analyzer='word')
        self.char_vectorizer = TfidfVectorizer(ngram_range=(2, 4), analyzer='char')

        # Initialize multiple models
        self.spelling_model = MultinomialNB()
        self.grammar_model = RandomForestClassifier(n_estimators=100)

        # Expanded dataset with incorrect sentences and labels
        self.train_texts = [
            "நான் பள்ளிக்கு செல்கிறேன்",  # Correct
            "அவள் பள்ளிக்கு செல்கிறாள்",  # Correct
            "அவள் புத்தகம் படிக்கிறாள்",  # Correct
            "அவள் புதிய புத்தகம் படிக்கிறான்",  # Gender mismatch
            "நாங்கள் பள்ளிக்கு செல்கிறோம்",  # Correct
            "நாங்கள் பழைய பேனா மேசையில் வைக்கிறாள்",  # Gender mismatch
            "அவன் பள்ளிக்கு செல்கிறான்",  # Correct
            "அவன் பள்ளிக்கு போகிறேன் சல்கிறான்",  # Subject-verb mismatch
            "நான் பெரிய கண்ணி பயன்படுத்துகிறேன்",  # Correct
            "நான் பெரிய கண்ணி பயன்படுத்திறான்"   # Gender mismatch
        ]

        # Labels for spelling and grammar
        self.spelling_labels = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0]
        self.grammar_labels = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0]

        # Train the models
        self._train_models()

        # Error patterns for post-processing
        self.error_patterns = {
            'common_errors': {
                r'\b(அவன்|அவள்)\s+\w+கிறாள்\b': 'Gender mismatch',
                r'\b(நான்|நாங்கள்)\s+\w+கிறான்\b': 'Subject-verb mismatch',
                r'\b(அவள்|அவன்)\s+\w+கிறேன்\b': 'Honorific mismatch'
            },
            'suggestions': {
                'Gender mismatch': {
                    'அவள்': 'படிக்கிறாள்',
                    'அவன்': 'படிக்கிறான்',
                    'கிறேன்': 'கிறேன்'
                },
                'Subject-verb mismatch': {
                    'நான்': 'கிறேன்',
                    'நாங்கள்': 'கிறோம்'
                },
                'Honorific mismatch': {
                    'அவள்': 'கிறாள்',
                    'அவன்': 'கிறான்'
                }
            }
        }

    def _train_models(self):
        # Prepare features
        word_features = self.word_vectorizer.fit_transform(self.train_texts)
        char_features = self.char_vectorizer.fit_transform(self.train_texts)

        # Combine features
        combined_features = np.hstack([
            word_features.toarray(),
            char_features.toarray()
        ])

        # Train models
        self.spelling_model.fit(combined_features, self.spelling_labels)
        self.grammar_model.fit(combined_features, self.grammar_labels)

    def _extract_features(self, text):
        # Extract word and character features
        word_feats = self.word_vectorizer.transform([text])
        char_feats = self.char_vectorizer.transform([text])

        # Combine features
        return np.hstack([
            word_feats.toarray(),
            char_feats.toarray()
        ])

    def _analyze_patterns(self, text):
        errors = []
        # Check common error patterns
        for pattern, msg in self.error_patterns['common_errors'].items():
            match = re.search(pattern, text)
            if match:
                errors.append(('pattern', msg, text, match.group()))

        return errors

    def check_text(self, text):
        try:
            features = self._extract_features(text)

            # Get model predictions
            spelling_pred = self.spelling_model.predict_proba(features)[0]
            grammar_pred = self.grammar_model.predict_proba(features)[0]

            errors = []

            # Check spelling confidence
            if spelling_pred[0] < 0.8:  # Less than 80% confidence for correct spelling
                errors.append(('spelling', 'Low spelling confidence', text))

            # Check grammar confidence
            if grammar_pred[0] < 0.8:  # Less than 80% confidence for correct grammar
                errors.append(('grammar', 'Low grammar confidence', text))

            # Add pattern-based errors
            pattern_errors = self._analyze_patterns(text)
            errors.extend(pattern_errors)

            # Generate suggestions
            suggestions = []
            for error_type, msg, original_text, error_word in errors:
                suggestion = self.error_patterns['suggestions'].get(msg, {}).get(error_word, 'No suggestion available')
                suggestions.append((msg, error_word, suggestion))

            return suggestions
        except Exception as e:
            return [('error', str(e), text)]
