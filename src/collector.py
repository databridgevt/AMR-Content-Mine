#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

import csv
import json

from nltk import ngrams
from nltk.tokenize import word_tokenize

from pathlib import Path
from searched_terms import searched_terms
import sys

# Constants -------------------------------------------------------------------

WORKING_DIRECTORY = Path("AmsContainer")

# Functions -------------------------------------------------------------------


def load_result(result_path: Path) -> dict:
    """ Load a JSON file at the specified path

    Parameters:
    result_path (Path): A Path object of the json file to load in.

    Returns:
    dict: The JSON file loaded into python as a dict.
    """
    with open(result_path.as_posix(), "r") as result_file:
        result_dict = json.load(result_file)
        return result_dict


def dump_result(result_path: Path) -> None:
    """ Print the JSON file at the given Path

    Parameters:
    result_path (Path): A Path object of the json file to load in.
    """
    with open(result_path.as_posix(), "r") as result_file:
        result_str = json.dumps(result_file.read(), indent=2)

    print(result_str)


def build_dict_list(paths: list) -> list:
    """ Build a list of Dictionaries from result JSONs

    Parameters:
    result_list (list): A list of Paths

    Returns:
    list: A list of dicts returned from json.loads()
    """
    dict_list = []
    for path in paths:
        dict_list.append(load_result(path))
    return dict_list


def get_eupmc_results():
    """ Returns a generator of Paths of JSON results
    """
    return WORKING_DIRECTORY.glob('**/eupmc_result.json')

def get_cleaned_results():
    """ Returns a generator of Paths to cleaned texts
    """
    return WORKING_DIRECTORY.glob('**/cleaned_output.txt')


# Main ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 2:
        WORKING_DIRECTORY = Path(sys.argv[1])

    # Build tsv of eupmc results
    with open('eupmc_results.tsv', 'w', newline='') as eupmc_results_tsv:
        # Select eupmc field names to store in tsv
        fields = [
            'pmcid',
            'pmid',
            'doi',
            'title',
            'authorString',
            'firstPublicationDate',
            'source']

        # Create writer object
        eupmc_writer = csv.DictWriter(
            eupmc_results_tsv,
            fieldnames=fields,
            restval='N/A',
            extrasaction='ignore',
            delimiter='\t')

        eupmc_writer.writeheader()

        print('Processing EUPMC JSON results...')
        paths = get_eupmc_results() # Get all paths of eupmc results
        for eupmc_path in paths:
            with open(eupmc_path, 'r') as eupmc_file:   # Open the file
                eupmc_dict = json.load(eupmc_file)      # Load in the JSON
                eupmc_writer.writerow(eupmc_dict)  # Write the JSON (loaded as a dict)
                
    #* Because almost every property in a eupmc_result.json is an array,
    #* The dicts above all get written with a few more characters than necessary.
    #* The following lines trim each field the the tsv
    eupmc_rows = None
    with open('eupmc_results.tsv', 'r') as eupmc_results_tsv:
        eupmc_reader = csv.reader(eupmc_results_tsv, delimiter='\t')
        eupmc_rows = list(eupmc_reader)
    with open('eupmc_results.tsv', 'w') as eupmc_results_tsv:
        eupmc_writer = csv.writer(eupmc_results_tsv, delimiter='\t')
        eupmc_writer.writerow(eupmc_rows[0])
        for row in eupmc_rows[1:]:
            for i, column in enumerate(row):
                row[i] = column[2:-2]
            eupmc_writer.writerow(row)
    eupmc_rows = None


    # Build a csv for counting all search terms
    with open('total_counts.csv', 'w', newline='') as total_counts_file:
       
        total_count_writer = csv.writer(total_counts_file)
        # Write the header row
        total_count_writer.writerow(['pmcid', *searched_terms])
        
        cleaned_paths = get_cleaned_results()
        print('Counting Searched Terms in cleaned texts ...')
        
        for cleaned_path in cleaned_paths:
            #Create a list with the PMCID and 0's for each search term            
            local_counts = [cleaned_path.parent.name] + [0]*len(searched_terms)
            
            with open(cleaned_path, 'r') as cleaned_file:
                cleaned_text = cleaned_file.read()
                # Spilt the text into bigrams
                bigrams = ngrams(word_tokenize(cleaned_text), 2)
                # Concatenate each bigram tuple with a space (to match the search terms)
                concated_bigrams = (' '.join(gram) for gram in bigrams)
            
                for gram in concated_bigrams:
                    for i, term in enumerate(searched_terms):
                        if term in gram:
                            local_counts[i + 1] += 1

            # This method double counts for unigram search terms
            for i, term in enumerate(searched_terms):
                if not ' ' in term:
                    local_counts[i+1] //= 2
                            
            total_count_writer.writerow(local_counts)

        # Use the counts found above to one-hot encode search term occurrence
    with open('total_counts.csv', 'r', newline='') as total_counts_file:
        with open('one_hot_counts.csv', 'w', newline='') as one_hot_file:
            total_count_reader = csv.reader(total_counts_file)
            one_hot_writer = csv.writer(one_hot_file)

            next(total_count_reader) # Skip the first row
            print('One Hot Encoding Searched Terms...')
            for row in total_count_reader:
                one_hot_count = [1 if int(value) > 0 else 0 for column in row[1:] for value in column]
                one_hot_writer.writerow([row[0]] + one_hot_count)
