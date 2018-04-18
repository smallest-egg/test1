def lcs(X , Y):
    m = len(X)
    n = len(Y)
 
    L = [[None]*(n+1) for i in range(m+1)]
 
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j] , L[i][j-1])
 
    return L[m][n]

def isIntPathMatch(string1, string2):
	alignmentScore = lcs(string1, string2)
	alignmentRatio = 2 * alignmentScore / (len(string1) + len(string2))
	cond1 = alignmentScore > (min(len(string1), len(string2)) - 1) and alignmentRatio >= 0.5
	cond2 = alignmentRatio > 0.91
	return cond1 or cond2