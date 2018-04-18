import re
from enforceStyle import enforceStyle, isAlias
from roman import fromRoman
from stemming.porter2 import stem

aliasDict = {}

#def getProcessRelatedWords(string):
#    return [word for word in string.split() if word.endswith(("sis", "ism", "ion", "ing", "nce", "ade", "air"))]

def stripUselessWords(string):
    # Need to make more efficient when bothered
    clausesToStrip = ("Role", "Pathway", "Superpathway", "Roles", "Pathways", "Superpathways", "Overview", "Hypothesized", "Hypothesis", "Other", "The")
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
            longForm = string[:leftBracket - 1]
            if len(possibleAlias) > len(longForm):
                possibleAlias, longForm = longForm, possibleAlias
            lastWord = longForm.split()[-1]
            lastLetter = possibleAlias[-1]
            if (lastWord.isdigit() or (lastWord == len(lastWord) * "I")) and lastLetter.isdigit():
                #Need to replace with a robust roman numeral check
                if not lastWord.isdigit():
                    lastWord = fromRoman(lastWord)
                else:
                    lastWord = int(lastWord)
                if lastWord == int(lastLetter):
                    possibleAlias = possibleAlias[:-1].rstrip("-")
                    longForm = " ".join(longForm.split()[:-1])
            stringSansAlias = longForm + string[min(rightBracket + 1, len(string)):]
            return stem(possibleAlias), stem(longForm), stringSansAlias
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
    for clause in string.split(" | "):
        clause = reorderOfsInNonconjunctiveClause(clause)
        alias, longForm, clauseSansAlias = separateAlias(clause)
        if alias:
            if alias in aliasDict and aliasDict[alias] != longForm:
                print("ALIAS CONFLICT: " + aliasDict[alias] + " || " + longForm)
            aliasDict[alias] = longForm
        clauseSansAlias = stripUselessWords(clauseSansAlias)
        logs.append(clauseSansAlias)
    return logs

def getAliasDict():
    return aliasDict

processString(enforceStyle("Metabolism of Tetrahydrocannabinol (THC)"))
processString(enforceStyle("Insulin signalling in human adipocytes (diabetic condition)"))
processString(enforceStyle("Factors and pathways affecting insulin-like growth factor (IGF1)-Akt signaling"))
processString(enforceStyle("Fas Ligand (FasL) pathway and Stress induction of Heat Shock Proteins (HSP) regulation"))
processString(enforceStyle("TCA Cycle and Deficiency of Pyruvate Dehydrogenase complex (PDHc)"))
processString(enforceStyle("Biosynthesis and regeneration of tetrahydrobiopterin (BH4) and catabolism of phenylalanine, including diseases"))