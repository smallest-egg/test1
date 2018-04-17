import re

def collapseSpaces(string):
    singleSpacedString = re.sub(" +", " ", string)
    respacedBracketsString = singleSpacedString.replace("( ", "(")
    respacedBracketsString = respacedBracketsString.replace(" )", ")")
    return re.sub(" \- ", "-", respacedBracketsString)

def removeBracketsIfNotAlias(string):
    standardizedSimilarPrepositions = re.sub("\((\s+From|Via|By|Due To|Only)(.*?)\)", "By\\2", string)
    return re.sub("\(((\s+In|On|With).*?)\)", "\\1", standardizedSimilarPrepositions)

def isAlias(word):
    return any(char.isdigit() for char in word) or sum(1 for char in word if char.isupper()) > 1

def capitalizeWords(string):
    capitalizedWords = []
    for word in string.split():
        # Capitalize word only if it is not an acronym or name including numerics (e.g. p53)
        if isAlias(word):
            capitalizedWords.append(word)
        else:
            capitalizedWords.append(word.capitalize())
    return " ".join(capitalizedWords)

def spaceOutSymbols(string):
    return re.sub("(\-|\(|\))", " \\1 ", string)

def enforceConjunctionStyle(string):
    # And/Or handled separately with spaces so as to not be thrown off by words with those strings
    noWordedConjunctionsString = re.sub(" (and|And|or|Or) ", " / ", string)
    return re.sub("(,\s+/|,|/|&)", " / ", noWordedConjunctionsString)

def enforceStyle(string):
    return collapseSpaces(removeBracketsIfNotAlias(capitalizeWords(spaceOutSymbols(enforceConjunctionStyle(string)))))