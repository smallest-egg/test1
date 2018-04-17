import re
from enforceStyle import enforceStyle, isAlias
from collections import namedtuple, Counter

aliasDict = {}
Pathway = namedtuple('Pathway', ['ID', 'Desc', "Alias"])
fileName1 = "keggnamesfull.txt"
fileName2 = "wikinamesfull.txt"
Counter = Counter()

def weightScoreBySigmoid(score, numOccurences):
    # More heavily penalizes common words, no steep drop for first few numbers to account for noise.
    dampingFactor = 1 / (1 + (numOccurences / 5) ** 2.5)
    return score * dampingFactor

def getProcessRelatedWords(string):
    return [word for word in string.split() if word.endswith(("sis", "ism", "ion", "ing", "nce", "ade", "air"))]

def stripUselessWords(string):
    # Need to make more efficient when bothered
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
            if len(possibleAlias) < len(aliasAlt):
                possibleAlias, aliasAlt = aliasAlt, possibleAlias
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

def getCommonWords(fileNameList):
    for fileName in fileNameList:
        with open (fileName) as file:
            lines = [line[:-1] for line in file.readlines()]
        for line in lines:
            Counter.update(re.sub(r"[^\w]", " ", enforceStyle(line)).split())
    print(Counter)

getCommonWords([fileName1, fileName2])

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
        print(logs)
    return logs

def processToFile(fileNameList):
    for fileName in fileNameList:
        with open (fileName) as file:
            lines = [line[:-1] for line in file.readlines()]
            for line in lines:
                newLine = "/".join([subpath.ID + " " + subpath.Desc for subpath in processString(enforceStyle(line))])
                Counter.update(re.sub(r"[^\w]", " ", newLine).split())
    print(Counter)

processToFile([fileName1, fileName2])

processString(enforceStyle("Metabolism of Tetrahydrocannabinol (THC)"))
processString(enforceStyle("Insulin signalling in human adipocytes (diabetic condition)"))
processString(enforceStyle("Factors and pathways affecting insulin-like growth factor (IGF1)-Akt signaling"))
processString(enforceStyle("Fas Ligand (FasL) pathway and Stress induction of Heat Shock Proteins (HSP) regulation"))
processString(enforceStyle("TCA Cycle and Deficiency of Pyruvate Dehydrogenase complex (PDHc)"))
processString(enforceStyle("Biosynthesis and regeneration of tetrahydrobiopterin (BH4) and catabolism of phenylalanine, including diseases"))