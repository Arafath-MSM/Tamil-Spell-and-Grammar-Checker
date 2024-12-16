from sklearn.feature_extraction.text import CountVectorizer # type: ignore
from sklearn.naive_bayes import MultinomialNB # type: ignore
from sklearn.model_selection import train_test_split # type: ignore

# Sample Data
sentences = [
    "அவன் போக",  # Incorrect
    "அவன் போகன்",  # Correct
    "நாங்கள் வர",  # Incorrect
    "நாங்கள் வரம்"  # Correct
]
labels = [0, 1, 0, 1]  # 0 = Incorrect, 1 = Correct

# Convert text to features
vectorizer = CountVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(sentences)
y = labels

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Naive Bayes Model
model = MultinomialNB()
model.fit(X_train, y_train)


# Test on New Sentence
test_sentence = ["அவன் வர"]
test_features = vectorizer.transform(test_sentence)
prediction = model.predict(test_features)

print("Test Sentence:", test_sentence[0])
print("Prediction (1=Correct, 0=Incorrect):", prediction[0])
