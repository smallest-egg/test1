from difflib import SequenceMatcher
import re
from string import capwords
from collections import namedtuple

aliasDict = {}
Pathway = namedtuple('Pathway', ['ID', 'Desc', "Alias"])

def getBestPartialMatch(string1, string2):
    shorterString, longerString = sorted([string1, string2], key = len)
    matcher = SequenceMatcher(None, shorterString, longerString, False)
    numOfPartials = len(longerString) - len(shorterString) + 1

    partialMatches = [matcher.find_longest_match(0, len(shorterString), i, i + len(shorterString)) for i in range(numOfPartials)]
    bestPartialMatch = max(partialMatches, key = lambda match: match.size)
    return bestPartialMatch

def isAlias(word):
    return any(char.isdigit() for char in word) or sum(1 for char in word if char.isupper()) > 1

def spaceOutSymbols(string):
    return re.sub("(\-|\(|\))", " \\1 ", string)

def capitalizeWords(string):
    capitalizedWords = []
    for word in string.split():
        # Capitalize word only if it is not an acronym or name including numerics (e.g. p53)
        if isAlias(word):
            capitalizedWords.append(word)
        else:
            capitalizedWords.append(word.capitalize())
    return " ".join(capitalizedWords)

def collapseSpaces(string):
    singleSpacedString = re.sub(" +", " ", string)
    respacedBracketsString = singleSpacedString.replace("( ", "(")
    respacedBracketsString = respacedBracketsString.replace(" )", ")")
    return re.sub(" \- ", "-", respacedBracketsString)

def enforceConjunctionStyle(string):
    # And/Or handled separately with spaces so as to not be thrown off by words with those strings
    noWordedConjunctionsString = re.sub(" (and|And|or|Or) ", " / ", string)
    return re.sub("(,\s+/|,|/|&)", " / ", noWordedConjunctionsString)

def removeBracketsIfNotAlias(string):
    standardizedSimilarPrepositions = re.sub("\((\s+From|Via|By|Due To|Only)(.*?)\)", "By\\2", string)
    return re.sub("\(((\s+In|On|With).*?)\)", "\\1", standardizedSimilarPrepositions)

def enforceStyle(string):
    return collapseSpaces(removeBracketsIfNotAlias(capitalizeWords(spaceOutSymbols(enforceConjunctionStyle(string)))))

def getProcessRelatedWords(string):
    return [word for word in string.split() if word.endswith(("sis", "ism", "ion", "ing", "nce", "ade", "air"))]

def stripUselessWords(string):
    #Need to make more efficient when bothered
    clausesToStrip = ("Role", "Pathway", "Superpathway", "Roles", "Pathways", "Superpathways", "Overview", "Hypothesized", "Hypothesis", "And", "Of", "Other")
    rearClausesToStrip = clausesToStrip + ("Including Diseases", "Including")
    strippedSomething = True
    while string and strippedSomething == True:
        strippedSomething = False
        if string.startswith(clausesToStrip):
            string = " ".join(string.split()[1:])
            strippedSomething = True
            continue
        if string.endswith(rearClausesToStrip):
            string = " ".join(string.split()[:-1])
            strippedSomething = True
    return string

def reorderOfsInNonconjunctiveClause(string):
    return " ".join(reversed(re.split(" Of | Underlying | Affecting ", string)))

def separateAlias(string):
    leftBracket = string.find("(")
    rightBracket = string.rfind(")")
    if leftBracket != -1 and rightBracket > leftBracket:
        possibleAlias = string[leftBracket + 1: rightBracket]
        hasAlias = any (isAlias(word) for word in possibleAlias.split())
        if hasAlias:
            aliasAlt = string[:leftBracket - 1]
            stringSansAlias = possibleAlias + string[min(rightBracket + 1, len(string)):]
            return possibleAlias, aliasAlt, stringSansAlias
    return "", "", string

def separateQualifiers(string):
    qualifierFlags = ["In ", "On ", "With ", "By ", "("]
    minIndexSoFar = len(string)
    qualifierStart = len(string)
    for flag in qualifierFlags:
        currentFlagIndex = string.find(flag)
        if currentFlagIndex < minIndexSoFar and string[currentFlagIndex - 1] != "(" and currentFlagIndex > 1:
            minIndexSoFar = currentFlagIndex
            qualifierStart = minIndexSoFar + len(flag)
    return string[qualifierStart:], string[:minIndexSoFar].rstrip()


def processString(string):
    logs = []
    for clause in string.split(" / "):
        clause = reorderOfsInNonconjunctiveClause(clause)
        alias, aliasAlt, clauseSansAlias = separateAlias(clause)
        if alias:
            aliasDict[aliasAlt] = alias
        qualifier, clauseSansQualifiers = separateQualifiers(clauseSansAlias)
        qualifier = stripUselessWords(qualifier)
        clauseSansQualifiers = stripUselessWords(clauseSansQualifiers)
        if not clauseSansQualifiers and qualifier:
            clauseSansQualifiers = qualifier
        if clauseSansQualifiers:
            logs.append(Pathway(clauseSansQualifiers, qualifier, aliasAlt))
    for i, log in enumerate(logs):
        logProcessRelatedWords = getProcessRelatedWords(log[0])
        if logProcessRelatedWords == log[0].split():
            for j in range(i + 1, len(logs)):
                possRelated = logs[j][0]
                possRelatedProcessWords = getProcessRelatedWords(possRelated)
                if possRelatedProcessWords:
                    relatedDesc = possRelated[:max(0,possRelated.find(possRelatedProcessWords[0]) - 1)]
                    logs[i] = Pathway(relatedDesc + " " + log[0], log[1], log[2])
                    break
        else if not logProcessRelatedWords

    print(logs)

processString(enforceStyle("Metabolism of Tetrahydrocannabinol (THC)"))
processString(enforceStyle("Insulin signalling in human adipocytes (diabetic condition)"))
processString(enforceStyle("Factors and pathways affecting insulin-like growth factor (IGF1)-Akt signaling"))
processString(enforceStyle("Fas Ligand (FasL) pathway and Stress induction of Heat Shock Proteins (HSP) regulation"))
processString(enforceStyle("TCA Cycle and Deficiency of Pyruvate Dehydrogenase complex (PDHc)"))
processString(enforceStyle("Biosynthesis and regeneration of tetrahydrobiopterin (BH4) and catabolism of phenylalanine, including diseases"))