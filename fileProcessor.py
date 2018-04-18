from stemming.porter2 import stem
from nltk import download
from nltk.corpus import stopwords
from enforceStyle import enforceStyle
from stringManipulator import processString, getAliasDict
from wordWeighting import getCounter, updateCounter
from difflib import get_close_matches
from fuzzyMatching import isFuzzyMatch

import re
import pprint
pp = pprint.PrettyPrinter(indent=2, width=150)

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

def stripStemLine(line):
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

def replaceAliasIn(line):
    for alias in aliasDict.keys():
        if alias in line:
            ind = line.find(alias)
            noTextLeft = ind == 0 or line[ind - 1] in (" ", "-")
            noTextRight = (ind + len(alias) >= len(line)) or (line[ind + len(alias)] in (" ", "-"))
            if noTextLeft and noTextRight:
                # print("REPLACED ALIAS: " + line)
                return line.replace(alias, aliasDict[alias])
    return line

def getCandidates(line):
    candidateList = []
    line = replaceAliasIn(line)
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

def enforceAliasReplacement():
    toAdd = []
    for ind, pathway in enumerate(processedPathwaysList):
        processedPathwaysList[ind] = replaceAliasIn(pathway)
    for key in matchDict.keys():
        if key in aliasDict:
            if aliasDict[key] in matchDict:
                matchDict[aliasDict[key]] = list(set(matchDict[aliasDict[key]] + matchDict[key]))
            else:
                toAdd.append([aliasDict[key], key])
    for key, val in toAdd:
        if key in matchDict:
            matchDict[key] = list(set(matchDict[key] + matchDict[val]))
        else:
            matchDict[key] = matchDict[val]

def cleanUselessKeys():
    processedWordsSet = set(processedWordsList)

    uselessKeys = []
    for key, val in matchDict.items():
        if len(val) > 15:
            uselessKeys.append(key)
    for key in uselessKeys:
        del matchDict[key]
        processedWordsSet.remove(key)

    return list(processedWordsSet)

def merge(pathwayPairs):
  sets = [set(pair) for pair in pathwayPairs]
  merged = 1
  while merged:
    merged = 0
    results = []
    while sets:
      common, rest = sets[0], sets[1:]
      sets = []
      for x in rest:
        if x.isdisjoint(common):
          sets.append(x)
        else:
          merged = 1
          common |= x
      results.append(common)
    sets = results
  return sets

def detectPathwayMatches():
    pathwayPairsToMerge = set()
    for pathwayNum, candidates in enumerate(allCandidateLists):
        for candidate in candidates:
            assert pathwayNum != candidate
            if isFuzzyMatch(processedPathwaysList[pathwayNum], processedPathwaysList[candidate]):
                pathwayPairsToMerge.add((candidate, pathwayNum))
    pathwaysToMerge = merge(pathwayPairsToMerge)
    namesOfPathwaysToMerge = [[originalPathwaysList[ind] for ind in pathwaysSet] for pathwaysSet in pathwaysToMerge]
    pp.pprint(namesOfPathwaysToMerge)
    mergeCount = 0
    for pathwaysSet in pathwaysToMerge:
        mergeCount += len(pathwaysSet) - 1
    print(mergeCount)


processFile(fileList, stripStemLine)
aliasDict = getAliasDict()
enforceAliasReplacement()
processedWordsList = cleanUselessKeys()
processFile(fileList, getCandidates)
detectPathwayMatches()