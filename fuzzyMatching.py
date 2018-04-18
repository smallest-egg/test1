from fuzz import token_set_ratio
from difflib import SequenceMatcher
from wordWeighting import getCounter, weightScoreBySigmoid

def isFuzzyMatch(string1, string2):
    """ PLACEHOLDER """
    return token_set_ratio(string1, string2) > 90