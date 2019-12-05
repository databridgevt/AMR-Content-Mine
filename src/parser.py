#!/usr/bin/env python3

import multiprocessing
from pathlib import Path
import pdfminer
import subprocess
import sys
import json
import keras
import progressbar

# Yeah, I'm not the best at naming sometimes
from searched_terms import searched_terms

pdfDirectoryPath = "AmsContainer/"

##########################################
# Data Mining and Collection
##########################################

# Create Locks for global data structures in order to prevent race conditions
data_lock = multiprocessing.Lock()
articleWordCounts_lock = multiprocessing.Lock()
overallWords_lock = multiprocessing.Lock()
differenceInData_lock = multiprocessing.Lock()
bar_lock = multiprocessing.Lock()

# Load in a JSON object to contain word counts and relevent data
with open('src/json/aggregate_data.json') as json_file:
    aggregate_json = json.load(json_file)
with open('src/json/difference.json') as json_file:
    differenceInData = json.load(json_file)
articleWordCounts = {}
overallWords = {}
ignoredWords = []

# Total Completed use for progess bar
total_complete = 0
global_bar = None

file = open("ignoredWords.txt", "r")
for line in file:
    if len(line) > 1:
        line = line[:-1]
    ignoredWords.append(line)
file.close()


def printData(key, term=None):
    print("\n========== PRINTING DATA " + key.upper() + "==========")
    for termVal in list(aggregate_json[key]):
        if term is None or term == termVal:
            print("\n" + termVal + ": " + str(aggregate_json[key][termVal]))

    print("\n========== DONE ==========")


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
    differenceInData_lock.acquire()

    for terms in differenceInData["termCountsPerArticle"]:
        differenceInData["termCountsPerArticle"][terms] = 0

    differenceInData_lock.release()


# updateData updates the data global array within itself for countTerms
# and associated helping functions
def updateData(pdf_path):

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

        data_lock.acquire()

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
        data_lock.release()

def process_one(file_path: Path) -> None:
    """ Process PDF at a given Path

    This function take a Path() of a pdf to be parsed. It first calls a subprocess to turn
    the given pdf into a .txt file. This .txt should be stored in the same directory as the
    given pdf. The updateData is called to handel the parsing the .txt file.

    """
    # Get a string name for the file, should be fulltext.pdf
    filename = file_path.name
    # Build a path for the output file
    output_file_path = file_path.parent.joinpath("processed_output.txt")
    # Build the command for processing a pdf. I get string concatenation,
    # But I think .format() is so much nicer when there's multiple arguments

    process_command = "pdf2txt.py -o {to_output} {to_process}".format(
        to_output=output_file_path.as_posix(),
        to_process=file_path.as_posix())

    print('Processing: {}'.format(file_path.as_posix()))

    subprocess.call(process_command, shell=True)
    updateData(file_path)

    # ? Do we need the rest of this function?

    # Load a result .json in the same directory as the corresponding
    # fulltext.pdf
    #with open(file_path.parent.joinpath("eupmc_result.json")) as json_file2:
    #    specificData = json.load(json_file2)


def process_all() -> None:
    """ Uses Process Pool to Process all PDFs

    This function uses a Process Pool to speed up this script. Essentially,
    This function will create a process for every CPU core available. Then, we pass
    process_one() and a list of all PDFs to the pool.

    """

    # Get a Path Object of the current directory
    current_dir = Path.cwd()

    # Use pathlib to glob all PDFs from ./AmsContainer
    # '**' recursively matches all subdirectories
    pdfs = list(current_dir.glob('AmsContainer-test/**/fulltext.pdf'))

    print('Found {} PDFs'.format(len(pdfs)))

    # Creating a Process Pool
    pool = multiprocessing.Pool()
    print('Spawned Pool with {} Processes'.format(multiprocessing.cpu_count()))

    # Give Some work to the Pool
    # 30 is called a "chunksize." I think the processes will take pdfs
    # in groups of 30 to process.
    print('Beginning To Convert PDFs to plain text ...')
    
    pool.map(process_one, pdfs, 10)

    print('Finished Converting PDF to plain text...')

    # Politely clean up the Process Pool
    pool.close()
    pool.join()


if __name__ == "__main__":
    process_all()
