def check_subject_verb(sentence):
    rules = {
        "அவர்கள்": "வருகிறார்கள்",
        "அவன்": "வருகிறான்",
    }
    words = sentence.split()
    for word in words:
        if word in rules:
            return sentence.replace(word, rules[word])
    return sentence
