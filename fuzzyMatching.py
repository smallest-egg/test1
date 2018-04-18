from fuzz import token_set_ratio
from difflib import SequenceMatcher
from wordWeighting import getCounter, weightScoreBySigmoid
from difflib import get_close_matches

def isFuzzyMatch(string1, string2):
    """ PLACEHOLDER 
    return token_set_ratio(string1, string2) > 90"""
    counter = getCounter()
    totalScore = 0
    maxPossScore = 0
    words1 = set(string1.split())
    words2 = set(string2.split())
    if len(words2) < len(words1):
        words1, words2 = words2, words1
    intersectSet = set()
    for word1 in words1:
        match = get_close_matches(word1, words2, n = 1, cutoff = 0.9)
        if match:
            intersectSet.add((word1, match[0]))
    for word1, word2 in intersectSet:
        if word1 != word2:
            numOccurences = counter[word1] + counter[word2]
        else:
            numOccurences = counter[word1]
        totalScore += weightScoreBySigmoid(100, numOccurences)
    maxPossScore = totalScore
    for word1 in (words1 - {word1 for word1, word2 in intersectSet}):
        numOccurences = counter[word1]
        maxPossScore += weightScoreBySigmoid(100, numOccurences)
    return totalScore / maxPossScore > 0.95