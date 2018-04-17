import re

from collections import Counter
from stemming.porter2 import stem
from enforceStyle import enforceStyle

counter = Counter()

def weightScoreBySigmoid(score, numOccurences):
    # More heavily penalizes common words, no steep drop for first few numbers to account for noise.
    dampingFactor = 1 / (1 + (numOccurences / 5) ** 2.5)
    return score * dampingFactor

def getCommonWords(fileNameList):
    for fileName in fileNameList:
        with open (fileName) as file:
            lines = [line[:-1] for line in file.readlines()]
        for line in lines:
            Counter.update([stem(word) for word in re.sub(r"[^\w]", " ", enforceStyle(line)).split()])
    print(Counter)

def updateCounter(list):
    counter.update(list)

def getCounter():
    return counter