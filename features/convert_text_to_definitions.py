from __future__ import division

from textblob import Word

def convert_text_to_definitions(text):
    definitions = []
    for word in text.split():
        definitions.extend(Word(word).definitions)
    return " ".join(definitions)