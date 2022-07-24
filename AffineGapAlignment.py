
DELETION = 'D'
INSERTION = 'I'
MATCH = 'M'
MISMATCH = 'm'
UP = '^'
DOWN = 'v'
MIDDLE = 'M'

def AffineGapAlignment(v, w, matchReward, mismatchPenalty, gapOpenPenalty, gapExtensionPenalty):
    negInf = -2**31-1
    i = len(v)
    j = len(w)
    middle = [[0] * (len(w) + 1) for x in range(len(v) + 1)]
    lower = [[0] * (len(w) + 1) for x in range(len(v) + 1)]
    upper = [[0] * (len(w) + 1) for x in range(len(v) + 1)]
    for i in range(len(v) + 1):
        lower[i][0] = middle[i][0] = 0 if i == 0 else -(gapOpenPenalty + (i-1)*gapExtensionPenalty)
        upper[i][0] = negInf
    for j in range(len(w) + 1):
        upper[0][j] = middle[0][j] = 0 if j == 0 else-(gapOpenPenalty + (j-1)*gapExtensionPenalty)
        lower[0][j] = negInf
    
    bt_upper = [[DOWN] * (len(w) + 1) for x in range(len(v) + 1)]
    bt_middle = [[0] * (len(w) + 1) for x in range(len(v) + 1)]
    bt_lower = [[UP] * (len(w) + 1) for x in range(len(v) + 1)]

    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            # lower
            lowerij = max(lower[i-1][j] - gapExtensionPenalty, middle[i-1][j] - gapOpenPenalty)
            lower[i][j] = lowerij

            # upper
            upperij = max(upper[i][j-1] - gapExtensionPenalty, middle[i][j-1] - gapOpenPenalty)
            upper[i][j] = upperij

            # middle
            isMatch = v[i - 1] == w[j - 1]
            match = middle[i-1][j-1] + matchReward if isMatch else middle[i-1][j-1]-mismatchPenalty

            middle[i][j] = max(match, lowerij, upperij)
            
            if middle[i][j] == lowerij:
                bt_middle[i][j] = DOWN
                bt_lower[i][j] = DELETION
            elif middle[i][j] == upperij:
                bt_middle[i][j]  = UP
                bt_upper[i][j] = INSERTION
            else:
                bt_middle[i][j]  = MATCH

    return [lower, middle, upper], [bt_lower, bt_middle, bt_upper]

def Affine_findBacktrackStartAndScore(scores):
    # bias towards the middle matrix
    highest_matrix_index = 1
    m = scores[highest_matrix_index]
    highest_score = m[len(m)-1][len(m[0]) - 1]

    for i in range(len(scores)):
        m = scores[i]
        this_score = m[len(m)-1][len(m[0]) - 1]
        if this_score > highest_score:
            highest_matrix_index = i
            highest_score = this_score

    return highest_score, highest_matrix_index


def AffineGapAlignment_BT(bt, whichToStart, v, w):
    i = len(v)
    j = len(w)
    vAlignment = ''
    wAlignment = ''
    currentMatrixIndex = whichToStart
    currentMatrix = bt[currentMatrixIndex]

    while i > 0 or j > 0:
        if i > 0 and j > 0 and currentMatrix[i][j] == MATCH:
            i -= 1
            j -= 1
            vAlignment = v[i] + vAlignment
            wAlignment = w[j] + wAlignment
        elif i > 0 and currentMatrix[i][j] == DOWN:
            currentMatrixIndex -= 1
            currentMatrix = bt[currentMatrixIndex]
        elif i > 0 and currentMatrix[i][j] == DELETION:
            i -= 1
            vAlignment = v[i] + vAlignment
            wAlignment = '-' + wAlignment
        elif j > 0 and currentMatrix[i][j] == UP:
            currentMatrixIndex += 1
            currentMatrix = bt[currentMatrixIndex]
        elif j > 0 and currentMatrix[i][j] == INSERTION:
            j -= 1
            vAlignment = '-' + vAlignment
            wAlignment = w[j] + wAlignment        
        else:
            # treat as deletion or insertion
            if i > 0:
                i -= 1
                vAlignment = v[i] + vAlignment
                wAlignment = '-' + wAlignment
            if j > 0:
                j -= 1
                vAlignment = '-' + vAlignment
                wAlignment = w[j] + wAlignment        

    return vAlignment, wAlignment

inputFileName = 'input.txt'
#inputFileName = 'dataset_249_8.txt'
lines = open(inputFileName).readlines()

weights = lines[0].strip().split(' ')
matchReward = int(weights[0].strip())
mismatchPenalty = int(weights[1].strip())
gapOpenPenalty = int(weights[2].strip())
gapContinuePenalty = int(weights[3].strip())

v = lines[1].strip()
w = lines[2].strip()

scores, bt = AffineGapAlignment(v, w, matchReward, mismatchPenalty, gapOpenPenalty, gapContinuePenalty)

high_score, whichMatrixToStart = Affine_findBacktrackStartAndScore(scores)

output = AffineGapAlignment_BT(bt, whichMatrixToStart, v, w)

print(f"matchReward: {matchReward}  mismatchPenalty: {mismatchPenalty}  gapOpenPenalty: {gapOpenPenalty} gapContinuePenalty: {gapContinuePenalty}")
print(f"V: {v}")
print(f"W: {w}")

print(high_score)
print(output[0])
print(output[1])


