import re

from collections import Counter
from stemming.porter2 import stem
from enforceStyle import enforceStyle

counter = Counter()

def weightScoreBySigmoid(score, numOccurences):
    # More heavily penalizes common words, no steep drop for first few numbers to account for noise.
    dampingFactor = 1 / (1.2 + (numOccurences / 6) ** 3) + 0.15
    return score * dampingFactor

def getCounter():
    return counter

def updateCounter(list):
    counter.update(list)