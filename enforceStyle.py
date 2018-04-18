import re
from roman import toRoman

def collapseSpaces(string):
    singleSpacedString = re.sub(" +", " ", string)
    respacedBracketsString = singleSpacedString.replace("( ", "(")
    respacedBracketsString = respacedBracketsString.replace(" )", ")")
    return re.sub(" \- ", "-", respacedBracketsString)

def removeBracketsIfNotAlias(string):
    standardizedSimilarPrepositions = re.sub("\((\s+From|Via|By|Due To|Only)(.*?)\)", "By\\2", string)
    return re.sub("\(((\s+In|On|With).*?)\)", "\\1", standardizedSimilarPrepositions)

def isAlias(word):
    isNumericalAcronym = any(char.isdigit() for char in word) and not word.isdigit()
    isAlphabeticalAcronym = sum(1 for char in word if char.isupper()) / len(word) > 0.2
    return (isNumericalAcronym or isAlphabeticalAcronym) and len(word) > 1

def capitalizeWords(string):
    newWords = []
    for word in string.split():
        # Capitalize word only if it is not an acronym or name including numerics (e.g. p53)
        if isAlias(word):
            newWords.append(word)
        else:
            newWords.append(word.capitalize())

    return " ".join(newWords)

def spaceOutSymbols(string):
    return re.sub("(\-|\(|\))", " \\1 ", string)

def enforceConjunctionStyle(string):
    # And/Or handled separately with spaces so as to not be thrown off by words with those strings
    noWordedConjunctionsString = re.sub(" (and|And|or|Or) ", " | ", string)
    return re.sub("(,\s+/|,|/|&)", " | ", noWordedConjunctionsString)

def romanizeNumerals(string):
    newWords = []
    for word in string.split():
        if word.isdigit():
            newWords.append(toRoman(int(word)))
        else:
            newWords.append(word)
    return " ".join(newWords)

def enforceStyle(string):
    return romanizeNumerals(collapseSpaces(removeBracketsIfNotAlias(capitalizeWords(enforceConjunctionStyle(spaceOutSymbols(string))))))