#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from pathlib import Path
import json
import xlsxwriter
from searched_terms import searched_terms

# Constants -------------------------------------------------------------------

cwd = Path.cwd()
working_directory = cwd.joinpath("AmsContainer-test")

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


def get_results_list() -> list:
    """ Returns a list of Paths of JSON results
    """
    return list(working_directory.glob('**/eupmc_result.json'))


def init_worksheet():
    """ Initialize a workbook in the current directory 
    """

    workbook = xlsxwriter.Workbook('Ams_Aggregate_Workbook.xlsx')

    # I want to store t=our data in 2 separate worksheets.
    # One to store data purely in the PMCs downloaded
    # Another to Store Word Counts
    pmc_sheet = workbook.add_worksheet('PMC Data')
    word_count_sheet = workbook.add_worksheet('Word Counts')

    # PMC Headers ---------------------------------------------------

    pmc_sheet.write(0, 0, 'PMC ID')
    pmc_sheet.write(0, 1, 'PM ID')
    pmc_sheet.write(0, 2, 'Source')
    pmc_sheet.write(0, 3, 'DOI')
    pmc_sheet.write(0, 4, 'Title')
    pmc_sheet.write(0, 5, 'Authors')
    pmc_sheet.write(0, 6, 'Date Published')

    # Word Count Headers --------------------------------------------
    word_count_sheet.write(0, 0, 'PMC ID')

    # Iterate over searched words and add each one to a header
    for i, term in enumerate(searched_terms):
        header_str = "{} Count".format(term)
        # 0, 0 already contains PMC ID, so i+1
        word_count_sheet.write(0, i+1, header_str)

    return (workbook, pmc_sheet, word_count_sheet)


def write_pmc_data(pmc_sheet, result_dict) -> None:
    """ Find and Write Relevent PMC data 
    """
    
    pass


# Main ------------------------------------------------------------------------

if __name__ == "__main__":
    paths = get_results_list()

    # ? Why do newlines get printed to the terminal as
    # ? a character sequence instead of whitespace?
    # ? It looks like json.dump() is escaping newlines
    # print("Hello\nWorld\nHello\\nWorld")
    # dump_result(result_paths[0])
    json_dicts = build_dict_list(paths)

    # I think my collector could end up eating a lot of memory
    # It might be better to ony keep one dict in memory at a time,
    # at the cost of many smaller/spread out IO operations
    paths = None

    (workbook, pmc_sheet, word_count_sheet) = init_worksheet()


    workbook.close()
