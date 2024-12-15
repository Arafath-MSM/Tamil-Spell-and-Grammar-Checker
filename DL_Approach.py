from transformers import pipeline

# Load a Pre-trained Tamil Language Model
grammar_checker = pipeline("text-classification", model="ai4bharat/indic-bert")

# Test Sentence
sentence = "அவன் போக"
result = grammar_checker(sentence)

print("Input Sentence:", sentence)
print("Grammar Check Result:", result)
