# load_dictionary.py
import pandas as pd

def load_tamil_dictionary():
    # You can use an external dictionary or a list of Tamil words here.
    # This is a mock function to simulate loading a Tamil word list.
    # Replace this with actual Tamil words list or use a text file.
    tamil_words = pd.read_csv('tamil_dictionary.csv')  # A CSV file containing Tamil words
    return set(tamil_words['word'])  # Return a set for faster lookups

