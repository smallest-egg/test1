from difflib import SequenceMatcher

def getLCS(string1, string2):
    matcher = SequenceMatcher(None, string1, string2, False)
    numOfPartials = len(string2) - len(string1) + 1
    start1, start2, size = matcher.find_longest_match(0, len(string1), 0, len(string2))
    return string1[start1 : start1 + size]