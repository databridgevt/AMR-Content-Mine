#!/usr/bin/env python3

""" Turn Freshly Converted PDFs into normalized corpora

    This script uses nltk to create standardized documents 
    BEFORE any other data processing takes place. Cleaned
    corpora are written back out to files in the same directory 
    as their raw predecessors.
"""

# Imports ---------------------------------------------------------------------

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import sys
from pathlib import Path
import string

# Constants -------------------------------------------------------------------

working_dir = Path('AmsContainer-test')

# Functions -------------------------------------------------------------------



# Main ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 2:
        working_dir = Path(sys.argv[1])

    # Get a generator of all converted PDFs
    processed_texts_paths = working_dir.glob('./**/processed_output.txt')

    for text_path in processed_texts_paths:
        with open(text_path, 'r') as text_file:
            text = text_file.read()

            # Convert uppercase to lowercase
            text = text.lower()

            # Potentially correct contractions here. Though, I expect
            # few contractions in scientific papers.

            # Remove punctuation from text
            # 'maketrans' creates a table that maps
            # (for our purposes) no characters to punctuation
            # characters. This essentially removes all punctuation from a string.
            # Plus, it's faster/more pythonic than regex.
            # ? May want to include sentence terminators '.','?',';'
            # ? To be used in chunking
            text = text.translate(str.maketrans('', '', string.punctuation))

            # Tokenize text.
            # This converts the text into essentially, an array of smaller strings.
            # In this case, we're mostly just splitting the text on
            # whitespace.
            tokens = word_tokenize(text)

            # Remove stopwords from a text.
            # Stop words are words like 'a', 'the', 'but'. These short, simple words
            # don't really carry a lot of meaning in the greater text. So, we'll
            # remove them to make smaller files/faster operations.
            stop_words = set(stopwords.words('english'))

            filtered_tokens = [word for word in tokens if word not in stop_words]

            # Lemmatize the text.
            # Lemmatization aims to turn words like 'talking' and 'talked' into 'talk'.
            # We're trying to convert words into their simplest forms possible.
            # Alternatively, we could have 'stemmed' words here instead of
            # using lemmatization, but (to put it shortly) lemmatization always produces
            # lexoconically correct words (you could find a word in a dictionary) where stemming
            # may not.
            lemmatizer = WordNetLemmatizer()

            lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

            # Rebuild the tokens into a single string for writing
            clean_text = ' '.join(lemmatized_tokens)

            output_path = Path(text_path.parent).joinpath('cleaned_output.txt')

            with open(output_path, 'w') as output_file:
                output_file.write(clean_text)