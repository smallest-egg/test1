from fuzzywuzzy import fuzz

def isFuzzyMatch(string1, string2):
	return fuzz.ratio(string1, string2) > 80