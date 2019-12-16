#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from pathlib import Path
import json
import xlsxwriter
from searched_terms import searched_terms

# Constants -------------------------------------------------------------------

cwd = Path.cwd()
working_directory = cwd.joinpath("AmsContainer-test") # ! Change Before real running

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
    """ Returns a list of Paths of JSON results
    """
    return working_directory.glob('**/eupmc_result.json')


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

    write_pmc_data(pmc_sheet, word_count_sheet, None, None)

    return (workbook, pmc_sheet, word_count_sheet)

def write_pmc_data(pmc_sheet, word_count_sheet, agg_dict, diff_dict) -> None:
    """ Find and Write Relevent PMC data 
    """
    # Write PMC book keeping data
    for i, eupmc_result_path in enumerate(get_eupmc_results()):
        with open(eupmc_result_path, 'r') as eumpc_result_file:
            eumpc_result = json.load(eumpc_result_file)

            # index 0 is the header, so i+1
            try:
                pmc_sheet.write(i + 1, 0, eumpc_result["pmcid"])
                word_count_sheet.write(i + 1, 0, eumpc_result["pmcid"])
            except:
                pass # Fail quietly
            try:
                pmc_sheet.write(i + 1, 1, eumpc_result["pmid"])
            except:
                pass
            try:
                pmc_sheet.write(i + 1, 2, eumpc_result["source"])
            except:
                pass
            try:
                pmc_sheet.write(i + 1, 3, eumpc_result["doi"])
            except:
                pass
            try:
                pmc_sheet.write(i + 1, 4, eumpc_result["title"])
            except:
                pass
            try:
                pmc_sheet.write(i + 1, 5, eumpc_result["authorList"])
            except:
                pass
            try:
                pmc_sheet.write(i + 1, 6, eumpc_result["firstPublicationDate"])
            except:
                pass
            
    # Write 


# Originally From parser.py --------------------------------------------------- 

# Load in a JSON object to contain word counts and relevent data
with open('src/json/aggregate_data.json') as json_file:
    aggregate_json = json.load(json_file)
with open('src/json/difference.json') as json_file:
    differenceInData = json.load(json_file)
articleWordCounts = {}
overallWords = {}
ignoredWords = []

file = open("ignoredWords.txt", "r")
for line in file:
    if len(line) > 1:
        line = line[:-1]
    ignoredWords.append(line)
file.close()

def countSentenceWords(sentence, term):
    lastSentenceWord = None
    check = False
    compoundWordChecks = ["one", "antibiotic",
                          "drug", "antimicrobial", "multidrug"]
    words = sentence.split(" ")
    for word in words:
        if check:
            if lastSentenceWord == "one" and word == "medicine":
                word = lastSentenceWord + " " + word
            elif lastSentenceWord == "antibiotic" and word == "resistance":
                word = lastSentenceWord + " " + word
            elif lastSentenceWord == "drug" and word == "resistance":
                word = lastSentenceWord + " " + word
            elif lastSentenceWord == "antimicrobial" and word == "resistance":
                word = lastSentenceWord + " " + word
            elif lastSentenceWord == "one" and word == "health":
                word = lastSentenceWord + " " + word
            elif lastSentenceWord == "multidrug" and word == "resistance":
                word = lastSentenceWord + " " + word
            else:
                if lastSentenceWord in aggregate_json["sentenceWordCounts"][term].keys(
                ):
                    aggregate_json["sentenceWordCounts"][term][lastSentenceWord] += 1
                else:
                    aggregate_json["sentenceWordCounts"][term][lastSentenceWord] = 1
        if word in compoundWordChecks:
            check = True
            lastSentenceWord = word
            continue
        else:
            check = False
            lastSentenceWord = None

        if len(word) == 0 or word == " " or word == "\n":
            continue
        while word[-1] == "." or word[-1] == "\n":
            word = word[:-1]
        if word in aggregate_json["sentenceWordCounts"][term].keys():
            aggregate_json["sentenceWordCounts"][term][word] += 1
        else:
            aggregate_json["sentenceWordCounts"][term][word] = 1

def isLastWord(word, length, space, newline):
    if (len(word) == 0 or word == " " or word == "\n"):
        return False
    lastWord = False
    if word[-1] == ".":
        lastWord = True
    if len(word) > 1:
        if word[-2:] == ".\n":
            lastWord = True
    return lastWord


def resetDifference():
    for terms in differenceInData["termCountsPerArticle"]:
        differenceInData["termCountsPerArticle"][terms] = 0

# updateData updates the data global array within itself for countTerms
# and associated helping functions
def update_one_data(pdf_path: Path) -> None:
    pmcId = pdf_path.parent.name

    global articleWordCounts
    articleWordCounts[pmcId] = {}
    resetDifference()

    # Getting the path for the correct output file
    output_path = pdf_path.parent.joinpath("processed_output.txt")

    with open(output_path, "r") as plain_text_file:
        sentence = " "
        sentenceComplete = False
        compoundWordChecks = [
            "one",
            "antibiotic",
            "drug",
            "antimicrobial",
            "multidrug",
            'drinking',
            'surface']
        firstWord = None
        check = False

        for line in plain_text_file:

            if (len(line) == 1):
                continue
            lineWords = line.split(" ")

            for word in lineWords:

                word = word.lower()
                if "\n" in word:
                    word = word[:-1]
                if word in ignoredWords:
                    continue
                if (len(word) == 0 or word == " " or word == "\n"):
                    continue
                sentence = sentence + word + " "

                while isLastWord(word, len(word), word == " ", word == "\n"):
                    # Needs to match searchedTerm
                    # print(sentence.split("."))
                    sentence = sentence.split(".")[0] + " "
                    for term in searched_terms:
                        if " " + term.lower() + " " in sentence.lower():
                            countSentenceWords(sentence, term)
                    sentence = " "
                    word = word.split(".")[1]

                if word == "":
                    continue
                # Check for compound words
                if check:
                    articleWordCounts[pmcId][firstWord] -= 1
                    overallWords[firstWord] -= 1
                    if firstWord == "one" and word == "medicine":
                        word = firstWord + " " + word
                    elif firstWord == "antibiotic" and word == "resistance":
                        word = firstWord + " " + word
                    elif firstWord == "drug" and word == "resistance":
                        word = firstWord + " " + word
                    elif firstWord == "antimicrobial" and word == "resistance":
                        word = firstWord + " " + word
                    elif firstWord == "one" and word == "health":
                        word = firstWord + " " + word
                    elif firstWord == "multidrug" and word == "resistance":
                        word = firstWord + " " + word
                    elif firstWord == "drinking" and word == "water":
                        word = firstWord + " " + word
                    elif firstWord == "surface" and word == "water":
                        word = firstWord + " " + word
                if word in compoundWordChecks:
                    check = True
                    firstWord = word.lower()
                else:
                    check = False
                    firstWord = None

                if word in articleWordCounts[pmcId].keys():
                    articleWordCounts[pmcId][word] += 1
                else:
                    articleWordCounts[pmcId][word] = 1

                if word in overallWords.keys():
                    overallWords[word] += 1
                else:
                    overallWords[word] = 1

                for term in searched_terms:
                    compoundCheck = firstWord in searched_terms
                    if word == term.lower():
                        aggregate_json["termCounts"][term] += 1
                        differenceInData["termCountsPerArticle"][term] += 1
                        if firstWord in searched_terms:
                            aggregate_json["termCounts"][firstWord] -= 1
                            differenceInData["termCountsPerArticle"][term] -= 1
                        with open(pdf_path.parent.joinpath('eupmc_result.json')) as json_file:
                            jsonData = json.load(json_file)
                            year = str(
                                jsonData["journalInfo"][0]["printPublicationDate"][0]).lower().split("-")[0]
                            title = str(
                                jsonData["journalInfo"][0]["journal"][0]["title"][0]).lower()
                            if title in aggregate_json["termJournalNames"][term].keys(
                            ):
                                aggregate_json["termJournalNames"][term][title] += 1
                            else:
                                aggregate_json["termJournalNames"][term][title] = 1
                            if compoundCheck:
                                aggregate_json["termJournalNames"][firstWord][title] -= 1
                            if year in aggregate_json["termYears"][term].keys():
                                aggregate_json["termYears"][term][year] += 1
                            else:
                                aggregate_json["termYears"][term][year] = 1
                            if compoundCheck:
                                aggregate_json["termYears"][term][year] -= 1
                        break

# Main ------------------------------------------------------------------------

if __name__ == "__main__":
    paths = get_eupmc_results()
    for pdf_path in working_directory.glob('**/fulltext.pdf'):
        update_one_data(pdf_path)
    

    # ? Why do newlines get printed to the terminal as
    # ? a character sequence instead of whitespace?
    # ? It looks like json.dump() is escaping newlines
    # print("Hello\nWorld\nHello\\nWorld")
    # dump_result(result_paths[0])
    json_dicts = build_dict_list(paths)

    (workbook, pmc_sheet, word_count_sheet) = init_worksheet()

    write_pmc_data(pmc_sheet, word_count_sheet, aggregate_json, differenceInData)

    workbook.close()
