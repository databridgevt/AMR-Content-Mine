#!/usr/bin/env python3

from plots import *
import os
import pdfminer
import subprocess
import sys
import copy
import json
import datetime
import keras
import xlsxwriter

pdfDirectoryPath = "AmsContainer/"

##########################################
# Data Mining and Collection
##########################################
print("")
print("=======================================================================")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
print("=======================================================================")
print("")

searchedTerms = ["one health", "one medicine", "animal", "human", "environment", "ecosystem", "ecohealth", "antimicrobial resistance",
                 "antibiotic resistance", "drug resistance", "multidrug resistance",  "resistance", "AMR", "ARB", "AR", "MDR", "dairy",
                 "cow", "beef", "cattle", "poultry", "swine", "chicken", "pig", "turkey", "fish", "porcine", "bovine", "soil", "agriculture",
                 "wastewater", "pharmaceutical", "drinking water", "groundwater", "surface water", "compost", "manure", "biosolids", "aquaculture"]

data = {
    "termCounts": {
        "one health": 0,
        "one medicine": 0,
        "animal": 0,
        "human": 0,
        "environment": 0,
        "ecosystem": 0,
        "ecohealth": 0,
        "antimicrobial resistance": 0,
        "antibiotic resistance": 0,
        "drug resistance": 0,
        "multidrug resistance": 0,
        "resistance": 0,
        "AMR": 0,
        "ARB": 0,
        "AR": 0,
        "MDR": 0,
        "dairy": 0,
        "cow": 0, 
        "beef": 0, 
        "cattle": 0, 
        "poultry": 0, 
        "swine": 0, 
        "chicken": 0, 
        "pig": 0, 
        "turkey": 0, 
        "fish": 0, 
        "porcine": 0, 
        "bovine": 0, 
        "soil": 0, 
        "agriculture": 0,
        "wastewater": 0, 
        "pharmaceutical": 0, 
        "drinking water": 0, 
        "groundwater": 0, 
        "surface water": 0, 
        "compost": 0, 
        "manure": 0, 
        "biosolids": 0, 
        "aquaculture": 0
    },
    "sentenceWordCounts": {
        "one health": {},
        "one medicine": {},
        "animal": {},
        "human": {},
        "environment": {},
        "ecosystem": {},
        "ecohealth": {},
        "antimicrobial resistance": {},
        "antibiotic resistance": {},
        "drug resistance": {},
        "multidrug resistance": {},
        "resistance": {},
        "AMR": {},
        "ARB": {},
        "AR": {},
        "MDR": {},
        "dairy": {},
        "cow": {}, 
        "beef": {}, 
        "cattle": {}, 
        "poultry": {}, 
        "swine": {}, 
        "chicken": {}, 
        "pig": {}, 
        "turkey": {}, 
        "fish": {}, 
        "porcine": {}, 
        "bovine": {}, 
        "soil": {}, 
        "agriculture": {},
        "wastewater": {}, 
        "pharmaceutical": {}, 
        "drinking water": {}, 
        "groundwater": {}, 
        "surface water": {}, 
        "compost": {}, 
        "manure": {}, 
        "biosolids": {}, 
        "aquaculture": {}
    },
    "termJournalNames": {
        "one health": {},
        "one medicine": {},
        "animal": {},
        "human": {},
        "environment": {},
        "ecosystem": {},
        "ecohealth": {},
        "antimicrobial resistance": {},
        "antibiotic resistance": {},
        "drug resistance": {},
        "multidrug resistance": {},
        "resistance": {},
        "AMR": {},
        "ARB": {},
        "AR": {},
        "MDR": {},
        "dairy": {},
        "cow": {}, 
        "beef": {}, 
        "cattle": {}, 
        "poultry": {}, 
        "swine": {}, 
        "chicken": {}, 
        "pig": {}, 
        "turkey": {}, 
        "fish": {}, 
        "porcine": {}, 
        "bovine": {}, 
        "soil": {}, 
        "agriculture": {},
        "wastewater": {}, 
        "pharmaceutical": {}, 
        "drinking water": {}, 
        "groundwater": {}, 
        "surface water": {}, 
        "compost": {}, 
        "manure": {}, 
        "biosolids": {}, 
        "aquaculture": {}
    },
    "termYears": {
        "one health": {},
        "one medicine": {},
        "animal": {},
        "human": {},
        "environment": {},
        "ecosystem": {},
        "ecohealth": {},
        "antimicrobial resistance": {},
        "antibiotic resistance": {},
        "drug resistance": {},
        "multidrug resistance": {},
        "resistance": {},
        "AMR": {},
        "ARB": {},
        "AR": {},
        "MDR": {},
        "dairy": {},
        "cow": {}, 
        "beef": {}, 
        "cattle": {}, 
        "poultry": {}, 
        "swine": {}, 
        "chicken": {}, 
        "pig": {}, 
        "turkey": {}, 
        "fish": {}, 
        "porcine": {}, 
        "bovine": {}, 
        "soil": {}, 
        "agriculture": {},
        "wastewater": {}, 
        "pharmaceutical": {}, 
        "drinking water": {}, 
        "groundwater": {}, 
        "surface water": {}, 
        "compost": {}, 
        "manure": {}, 
        "biosolids": {}, 
        "aquaculture": {}
    }
}

articleWordCounts = {}
overallWords = {}
ignoredWords = []
file = open("ignoredWords.txt", "r")
for line in file:
    if len(line) > 1:
        line = line[:-1]
    ignoredWords.append(line)


def time():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("%H:%M:%S")


def printData(key, term=None):
    print("\n========== PRINTING DATA " + key.upper() + "==========")
    for termVal in list(data[key]):
        if term == None or term == termVal:
            print("\n" + termVal + ": " + str(data[key][termVal]))

    print("\n========== DONE ==========")


lastSentenceWord = None
check = False
compoundWordChecks = ["one", "antibiotic",
    "drug", "antimicrobial", "multidrug"]


def countSentenceWords(sentence, term):
    global lastSentenceWord
    global check
    global compoundWordChecks
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
                if lastSentenceWord in data["sentenceWordCounts"][term].keys():
                    data["sentenceWordCounts"][term][lastSentenceWord] += 1
                else:
                    data["sentenceWordCounts"][term][lastSentenceWord] = 1
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
        if word in data["sentenceWordCounts"][term].keys():
            data["sentenceWordCounts"][term][word] += 1
        else:
            data["sentenceWordCounts"][term][word] = 1


def isLastWord(word, length, space, newline):
    # print("word: " + word + " LENGTH: " + str(length) + " SPACE: " + str(space) + " NEWLINE: " + str(newline))
    if (len(word) == 0 or word == " " or word == "\n"):
        return False
    lastWord = False
    if word[-1] == ".":
        lastWord = True
    if len(word) > 1:
        if word[-2:] == ".\n":
            lastWord = True
    return lastWord

# updateData updates the data global array within itself for countTerms and associated helping functions

differenceInData = {
        "termCountsPerArticle": {
        "one health": 0,
        "one medicine": 0,
        "animal": 0,
        "human": 0,
        "environment": 0,
        "ecosystem": 0,
        "ecohealth": 0,
        "antimicrobial resistance": 0,
        "antibiotic resistance": 0,
        "drug resistance": 0,
        "multidrug resistance": 0,
        "resistance": 0,
        "AMR": 0,
        "ARB": 0,
        "AR": 0,
        "MDR": 0,
        "dairy": 0,
        "cow": 0, 
        "beef": 0, 
        "cattle": 0, 
        "poultry": 0, 
        "swine": 0, 
        "chicken": 0, 
        "pig": 0, 
        "turkey": 0, 
        "fish": 0, 
        "porcine": 0, 
        "bovine": 0, 
        "soil": 0, 
        "agriculture": 0,
        "wastewater": 0, 
        "pharmaceutical": 0, 
        "drinking water": 0, 
        "groundwater": 0, 
        "surface water": 0, 
        "compost": 0, 
        "manure": 0, 
        "biosolids": 0, 
        "aquaculture": 0
    }
}

def resetDifference():
    for terms in differenceInData["termCountsPerArticle"] :
        differenceInData["termCountsPerArticle"][terms] = 0
    
    

def updateData(pmcId):
    global articleWordCounts
    articleWordCounts[pmcId] = {}
    resetDifference()
    # articleTitleAdded = False
    file = open("output.txt")
    sentence = " "
    sentenceComplete = False
    compoundWordChecks = ["one", "antibiotic",
                          "drug", "antimicrobial", "multidrug", 'drinking', 'surface']
    firstWord = None
    check = False
    for line in file:
        
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
                for term in searchedTerms:
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

            for term in searchedTerms:
                compoundCheck = firstWord in searchedTerms
                if word == term.lower():
                    data["termCounts"][term] += 1
                    differenceInData["termCountsPerArticle"][term] += 1
                    if firstWord in searchedTerms:
                        data["termCounts"][firstWord] -= 1
                        differenceInData["termCountsPerArticle"][term] -= 1
                    # if (not articleTitleAdded):
                    if (True):
                        global pdfDirectoryPath
                        jsonPath = pdfDirectoryPath + pmcId + "/eupmc_result.json"
                        with open(jsonPath) as json_file:
                            jsonData = json.load(json_file)
                            year = str(jsonData["journalInfo"][0]["printPublicationDate"][0]).lower().split("-")[0]
                            title = str(
                                jsonData["journalInfo"][0]["journal"][0]["title"][0]).lower()
                            if title in data["termJournalNames"][term].keys():
                                data["termJournalNames"][term][title] += 1
                            else:
                                data["termJournalNames"][term][title] = 1
                            if compoundCheck:
                                data["termJournalNames"][firstWord][title] -= 1

                            if year in data["termYears"][term].keys():
                                data["termYears"][term][year] += 1
                            else:
                                data["termYears"][term][year] = 1
                            if compoundCheck:
                                data["termYears"][term][year] -= 1
                        # print "\n"+title+"\n"+date+"\n"+term
                        # articleTitleAdded = True
                    break

    file.close()


pdfNum = 0
print("Number of Articles = " +
      str(len(os.listdir(pdfDirectoryPath)) - 1) + " (" + time() + ")\n")
test = True

#workbook = xlsxwriter.Workbook('specificData.xlsx')
#worksheet = workbook.add_worksheet()

#worksheet.write('A1', 'Article Number')
#worksheet.write('B1', 'PMC ID')
#worksheet.write('C1', 'Article Title')
#worksheet.write('D1', 'Year Published')
#worksheet.write('E1', 'Journal')
#worksheet.write('F1', 'Authors')
#worksheet.write('G1', 'Count for "one health"')
#worksheet.write('H1', 'Count for "one medicine"')
#worksheet.write('I1', 'Count for "animal"')
#worksheet.write('J1', 'Count for "human"')
#worksheet.write('K1', 'Count for "environment"')
#worksheet.write('L1', 'Count for "ecosystem"')
#worksheet.write('M1', 'Count for "ecohealth"')
#worksheet.write('N1', 'Count for "antimicrobial resistance"')
#worksheet.write('O1', 'Count for "antibiotic resistance"')
#worksheet.write('P1', 'Count for "drug resistance"')
#worksheet.write('Q1', 'Count for "multidrug resistance"')
#worksheet.write('R1', 'Count for "resistance"')
#worksheet.write('S1', 'Count for "AMR"')
#worksheet.write('T1', 'Count for "ARB"')
#worksheet.write('U1', 'Count for "AR"')
#worksheet.write('V1', 'Count for "MDR"')
#worksheet.write('W1', 'Count for "dairy"')
#worksheet.write('X1', 'Count for "cow"')
#worksheet.write('Y1', 'Count for "beef"')
#worksheet.write('Z1', 'Count for "cattle"')
#worksheet.write('AA1', 'Count for "poultry"')
#worksheet.write('AB1', 'Count for "swine"')
#worksheet.write('AC1', 'Count for "chicken"')
#worksheet.write('AD1', 'Count for "pig"')
#worksheet.write('AE1', 'Count for "turkey"')
#worksheet.write('AF1', 'Count for "fish"')
#worksheet.write('AG1', 'Count for "porcine"')
#worksheet.write('AH1', 'Count for "bovine"')
#worksheet.write('AI1', 'Count for "soil"')
#worksheet.write('AJ1', 'Count for "agriculture"')
#worksheet.write('AK1', 'Count for "wastewater"')
#worksheet.write('AL1', 'Count for "pharmaceutical"')
#worksheet.write('AM1', 'Count for "drinking water"')
#worksheet.write('AN1', 'Count for "groundwater"')
#worksheet.write('AO1', 'Count for "surface water"')
#worksheet.write('AP1', 'Count for "compost"')
#worksheet.write('AQ1', 'Count for "manure"')
#worksheet.write('AR1', 'Count for "biosolids"')
#worksheet.write('AS1', 'Count for "aquaculture"')

for name in os.listdir(pdfDirectoryPath):
    if "eupmc" in name or ".DS_Store" == name:
        continue
    pdfPath = pdfDirectoryPath + name + "/fulltext.pdf"
    # if test == True:
    #     print("name = " + pdfPath)
    #     test == False
    # if (testFirst):
    #     print(name
    if (os.path.lexists(pdfPath)):
        row = 1
        subprocess.call("pdf2txt.py -o output.txt " + pdfPath, shell=True)
        # if ((pdfNum + 1) % 10 == 0):
        print("\npdfNum = " + str(pdfNum + 1) + " (" + time() + ")\n")
        updateData(name)
        with open(pdfDirectoryPath + name + "/eupmc_result.json") as json_file2:
            specficData = json.load(json_file2)
        #create an array that stores the data for each category for only this 'name'. deletes after every iteration of for.
        #use array to access data from excel

        #helpful links: https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
            #https://xlsxwriter.readthedocs.io/
            #

        #for (p in specificData[])

        #worksheet.write(pdfNum + 1, 0, pdfNum)
        #worksheet.write(pdfNum + 1, 1, specficData['pmcid'])
        #worksheet.write(pdfNum + 1, 2, json_file2['title'])
        #worksheet.write(pdfNum + 1, 3, json_file2['pubYear'])
        #worksheet.write(pdfNum + 1, 4, json_file2['journalInfo: journal: title'])
        #worksheet.write(pdfNum + 1, 5, json_file2['authorString'])
        #worksheet.write(pdfNum + 1, 6, differenceInData["termCountsPerArticle"]['one health'])
        #worksheet.write(pdfNum + 1, 7, differenceInData["termCountsPerArticle"]['one medicine'])
        #worksheet.write(pdfNum + 1, 8, differenceInData["termCountsPerArticle"]['animal'])
        #worksheet.write(pdfNum + 1, 9, differenceInData["termCountsPerArticle"]['human'])
        #worksheet.write(pdfNum + 1, 10, differenceInData["termCountsPerArticle"]['environment'])
        #worksheet.write(pdfNum + 1, 11, differenceInData["termCountsPerArticle"]['ecosystem'])
        #worksheet.write(pdfNum + 1, 12, differenceInData["termCountsPerArticle"]['ecohealth'])
        #worksheet.write(pdfNum + 1, 13, differenceInData["termCountsPerArticle"]['antimicrobial resistance'])
        #worksheet.write(pdfNum + 1, 14, differenceInData["termCountsPerArticle"]['antibiotic resistance'])
        #worksheet.write(pdfNum + 1, 15, differenceInData["termCountsPerArticle"]['drug resistance'])
        #worksheet.write(pdfNum + 1, 16, differenceInData["termCountsPerArticle"]['multidrug resistance'])
        #worksheet.write(pdfNum + 1, 17, differenceInData["termCountsPerArticle"]['resistance'])
        #worksheet.write(pdfNum + 1, 18, differenceInData["termCountsPerArticle"]['AMR'])
        #worksheet.write(pdfNum + 1, 19, differenceInData["termCountsPerArticle"]['ARB'])
        #worksheet.write(pdfNum + 1, 20, differenceInData["termCountsPerArticle"]['AR'])
        #worksheet.write(pdfNum + 1, 21, differenceInData["termCountsPerArticle"]['MDR'])
        #worksheet.write(pdfNum + 1, 22, differenceInData["termCountsPerArticle"]['dairy'])
        #worksheet.write(pdfNum + 1, 23, differenceInData["termCountsPerArticle"]['cow'])
        #worksheet.write(pdfNum + 1, 24, differenceInData["termCountsPerArticle"]['beef'])
        #worksheet.write(pdfNum + 1, 25, differenceInData["termCountsPerArticle"]['cattle'])
        #worksheet.write(pdfNum + 1, 26, differenceInData["termCountsPerArticle"]['poultry'])
        #worksheet.write(pdfNum + 1, 27, differenceInData["termCountsPerArticle"]['swine'])
        #worksheet.write(pdfNum + 1, 28, differenceInData["termCountsPerArticle"]['chicken'])
        #worksheet.write(pdfNum + 1, 29, differenceInData["termCountsPerArticle"]['pig'])
        #worksheet.write(pdfNum + 1, 30, differenceInData["termCountsPerArticle"]['turkey'])
        #worksheet.write(pdfNum + 1, 31, differenceInData["termCountsPerArticle"]['fish'])
        #worksheet.write(pdfNum + 1, 32, differenceInData["termCountsPerArticle"]['porcine'])
        #worksheet.write(pdfNum + 1, 33, differenceInData["termCountsPerArticle"]['bovine'])
        #worksheet.write(pdfNum + 1, 34, differenceInData["termCountsPerArticle"]['soil'])
        #worksheet.write(pdfNum + 1, 35, differenceInData["termCountsPerArticle"]['agriculuture'])
        #worksheet.write(pdfNum + 1, 36, differenceInData["termCountsPerArticle"]['wastewater'])
        #worksheet.write(pdfNum + 1, 37, differenceInData["termCountsPerArticle"]['pharmaceutical'])
        #worksheet.write(pdfNum + 1, 38, differenceInData["termCountsPerArticle"]['drinking water'])
        #worksheet.write(pdfNum + 1, 39, differenceInData["termCountsPerArticle"]['groundwater'])
        #worksheet.write(pdfNum + 1, 40, differenceInData["termCountsPerArticle"]['surface water'])
        #worksheet.write(pdfNum + 1, 41, differenceInData["termCountsPerArticle"]['compost'])
        #worksheet.write(pdfNum + 1, 42, differenceInData["termCountsPerArticle"]['manure'])
        #worksheet.write(pdfNum + 1, 44, differenceInData["termCountsPerArticle"]['biosolids'])
        #worksheet.write(pdfNum + 1, 44, differenceInData["termCountsPerArticle"]['aquaculture'])
        pdfNum += 1
    else:
        print("ERROR: pdf Path ( " + str(pdfPath) + " ) does not exist...")
#with open('articleData.txt', 'w') as outfile:
    #json.dumps(articleData, outfile)



##########################################
# Data Analysis and Visualization
##########################################

# file = open("wordCloudFile.txt", "w")
# key = "termCounts"
# for term in list(data[key]):
#     for x in range(data[key][term]):
#         print term
#
# for term in list(data[key]):
#     for x in range(data[key][term]):
#         file.write(term + "\n")

def collectLines():
    min = 10000
    max = 0
    termYears = data["termYears"]
    lines = []
    for term in searchedTerms:
        yearList = list(termYears[term].keys())
        for year in yearList:
            if int(year) < min:
                min = int(year)
            if int(year) > max:
                max = int(year)

    x = range(min, max + 1)
    ys = []
    termIndex = 0
    for term in searchedTerms:
        ys.append([])
        for year in x:
            if str(year) in termYears[term].keys():
                ys[termIndex].append(termYears[term][str(year)])
            else:
                ys[termIndex].append(0)
        termIndex += 1
    return (x, ys)


def collectCountBars():
    x = []
    y = []
    termCounts = data["termCounts"]
    for term in termCounts:
        x.append(term)
        y.append(termCounts[term])
    return (x, y)


def overallTopWordsTable(n=10):
    global overallWords
    topWords = []
    for i in range(n):
        topWords.append((None, 0))
    for word in overallWords:
        wordCount = overallWords[word]
        i = 0
        while (i < len(topWords)):
            topWord = topWords[i]
            if wordCount >= topWord[1]:
                topWords.insert(i, (word, wordCount))
                topWords = topWords[:n]
                break
            i += 1
    return topWords


def sentenceWordTable(term, n=10):
    sentenceWords = data["sentenceWordCounts"][term]
    if len(sentenceWords) > 0:
        del sentenceWords[term]
    topWords = []
    for i in range(n):
        topWords.append((None, 0))
    for word in sentenceWords:
        wordCount = sentenceWords[word]
        i = 0
        while(i < len(topWords)):
            topWord = topWords[i]
            if wordCount >= topWord[1]:
                topWords.insert(i, (word, wordCount))
                topWords = topWords[:n]
                break
            i += 1
    return topWords


def writeTop10ArticleWords(file, pmcId, n):
    top10words = []
    articleWords = articleWordCounts[pmcId]
    for i in range(n):
        top10words.append((None, 0))
    for word in articleWords:
        wordCount = articleWords[word]
        i = 0
        while (i < len(top10words)):
            topWord = top10words[i]
            if wordCount >= topWord[1]:
                top10words.insert(i, (word, wordCount))
                top10words = top10words[:n]
                break
            i += 1
    return top10words


def articleWordTable(pmcId="all", n=25):
    global articleWordCounts
    file = open("articleWordTable.txt", "w")
    if (pmcId == "all"):
        table = []
        for articleId in articleWordCounts:
            table.append(writeTop10ArticleWords(file, articleId, n))
        return table
    else:
        return writeTop10ArticleWords(file, pmcId, n)


##### KEY TERM OCCURENCE VS TIME LINE GRAPH #####
lineData = collectLines()
x = lineData[0]
ys = lineData[1]
title = "How Term Frequency Changes Over Time"
xlabel = "Date"
ylabel = "Count"
legend = searchedTerms
lines = linePlot(x, ys, title=title, xlabel=xlabel,
                 ylabel=ylabel, legend=legend)

##### KEY TERM OCCURENCE BAR GRAPH #####
barData = collectCountBars()
x = barData[0]
y = barData[1]
title = "Term Frequency"
xlabel = "Term"
ylabel = "Count"
barPlot(barData[0], barData[1], title=title, xlabel=xlabel, ylabel=ylabel)

########## TOP ARTICLE WORDS TABLE ##########
file = open("top_article_words.csv", "w")
pmcId = "PMC2973834"
for pmcId in articleWordCounts:
    print("\n" + pmcId + ":")
    topWords = articleWordTable(pmcId=pmcId)
    file.write(pmcId+ ":\n")
    for w in topWords:
        print(w)
        file.write(str(w[0]) + "," + str(w[1]) + "\n")
file.close()


########## SENTENCE WORDS MULTI BAR PLOT ##########
xs = []
ys = []
subtitles = []
title = "Terms Found in the Same Sentence as Key Terms"
xlabel = "Sentence Terms"
ylabel = "Occurrences"
file = open("top_sentence_words_per_term.txt", "w")
termIndex = 0
for term in searchedTerms[8:12]:
    termTitle = term[0]
    if len(term)>0:
        termTitle += term[1:]
    subtitles.append(termTitle)
    xs.append([])
    ys.append([])
    sentenceWords = sentenceWordTable(term, n=25)
    file.write("\n" + term + ": \n")
    for wordData in sentenceWords:
        xs[termIndex].append(wordData[0])
        if xs[termIndex][len(xs[termIndex]) - 1] == None:
            xs[termIndex][len(xs[termIndex]) - 1] = "*No Occurences Found*"
        ys[termIndex].append(wordData[1])
        # print str(wordData[0]) + ": " + str(wordData[1])
        file.write(str(wordData[0]) + ": " + str(wordData[1]) + "\n")
    termIndex += 1
file.close()
multiBarPlot(xs, ys, 2, 2, title=title, subtitles=subtitles, xlabel=xlabel, ylabel=ylabel, fontSize=16)


########## OVERALL WORDS BAR GRAPH ###########
x = []
y = []
file = open("top_words_overall.txt", "w")
topWords = overallTopWordsTable(n=25)
first = True
for w in topWords:
    print("\n'" + w[0] + "'" + ": " + str(w[1]))
    file.write(w[0] + ": " + str(w[1]) + "\n")
    x.append(w[0])
    y.append(w[1])

title = "Overall Word Count"
xlabel = "Term"
ylabel = "Count"
barPlot(x, y, title=title, xlabel=xlabel, ylabel=ylabel)
