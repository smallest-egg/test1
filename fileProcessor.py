from stemming.porter2 import stem
from nltk import download
from nltk.corpus import stopwords
from enforceStyle import enforceStyle
from stringManipulator import processString, getAliasDict
from wordWeighting import updateCounter, getCommonWords, getCounter
from difflib import get_close_matches
from fuzzyMatching import isFuzzyMatch

import re

cachedStopWords = set(stopwords.words("english"))

fileName1 = "keggnamesfull.txt"
fileName2 = "wikinamesfull.txt"
fileList = [fileName1, fileName2]
memoize = {}
originalPathwaysList = []
processedPathwaysList = []
processedWordsList = []
allCandidateLists = []
matchDict = {}
lineNumber = [0] #ignore the nonlocal hack

def processFile(fileNameList, fn):
    lineNumber[0] = 0
    for fileName in fileNameList:
        with open (fileName) as file:
            lines = [line[:-1] for line in file.readlines()]
            for line in lines:
                fn(line)

def tokenize(line):
    newLine = processString(enforceStyle(line))
    newLine  = re.sub("(\||\(|\)|-)", " ", " ".join(newLine))
    return newLine.split()

def stopwordStripAndStem(line):
    strippedStemmedList = [stem(word) for word in tokenize(line) if word.lower() not in cachedStopWords]
    updateCounter(strippedStemmedList)
    return strippedStemmedList

def initLine(line):
    originalPathwaysList.append(line)
    strippedStemmedList = stopwordStripAndStem(line)
    processedWordsList.extend(strippedStemmedList)
    processedPathwaysList.append(" ".join(strippedStemmedList))

    for word in strippedStemmedList:
        if word in matchDict:
            matchDict[word].append(lineNumber[0])
        else:
            matchDict[word] = [lineNumber[0]]
    lineNumber[0] += 1

def getCandidates(line):
    candidateList = []
    for word in stopwordStripAndStem(line):
        if word not in memoize:
            memoize[word] = get_close_matches(word, processedWordsList, n = 3, cutoff = 0.75)
        for matchedWord in memoize[word]:
            candidateList.extend(matchDict[matchedWord])
    candidateList = set(candidateList)
    if lineNumber[0] in candidateList:
        candidateList.remove(lineNumber[0])
    allCandidateLists.append(list(candidateList))
    lineNumber[0] += 1


#getCommonWords(fileList)
processFile(fileList, initLine)

processedWordsList = set(processedWordsList)

uselessKeys = []
for key, val in matchDict.items():
    if len(val) > 15:
        uselessKeys.append(key)
for key in uselessKeys:
    del matchDict[key]
    processedWordsList.remove(key)

processedWordsList = list(processedWordsList)

processFile(fileList, getCandidates)

for pathwayNum, candidates in enumerate(allCandidateLists):
    for candidate in candidates:
        if isFuzzyMatch(processedPathwaysList[pathwayNum], processedPathwaysList[candidate]):
            print(originalPathwaysList[pathwayNum] + " ||| " + originalPathwaysList[candidate])