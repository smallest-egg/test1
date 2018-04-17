from stemming.porter2 import stem
from nltk import download
from nltk.corpus import stopwords
from enforceStyle import enforceStyle
from stringManipulator import processString, getAliasDict
from wordWeighting import updateCounter, getCommonWords, getCounter

import re

cachedStopWords = set(stopwords.words("english"))

fileName1 = "keggnamesfull.txt"
fileName2 = "wikinamesfull.txt"

def processToFile(fileNameList, fn):
    for fileName in fileNameList:
        with open (fileName) as file:
            lines = [line[:-1] for line in file.readlines()]
            for line in lines:
                print(fn(line))

def tokenize(line):
	newLine = processString(enforceStyle(line))
	newLine  = re.sub("(\||\(|\)|-)", " ", " ".join(newLine))
	return newLine.split()

def stopwordStripAndStem(line):
	strippedStemmedList = [stem(word) for word in tokenize(line) if word not in cachedStopWords]
	updateCounter(strippedStemmedList)
	return " ".join(strippedStemmedList)

getCommonWords([fileName1, fileName2])

processToFile([fileName1, fileName2], stopwordStripAndStem)

print(getCounter())