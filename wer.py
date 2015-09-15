from sys import argv
import argparse

leftList = []
rightList = []

def GetLeftMatch(sentence, list_of_words):
    for i in xrange(len(sentence), 0, -1):
        if i == 1:
            #print "Left Single: ", sentence[0]
            return sentence[0]
        if list_of_words.get(sentence[0:i]) != None:
            #print "Left Match", sentence[0:i]
            return sentence[0:i]

def GetRightMatch(sentence, list_of_words):
    for i in xrange(0, len(sentence)):
        if i == len(sentence) - 1:
            #print "Right Single: ", sentence[i]
            return sentence[i]
        if list_of_words.get(sentence[i:]) != None:
            #print "Right Match", sentence[i:]
            return sentence[i:]

def MaxMatch(sentence, list_of_words):
    #leftList = []
    #rightList = []
    global leftList
    global rightList

    if sentence == "":
        return
    
    leftMatch = GetLeftMatch(sentence, list_of_words)
    #print "Left Match: ", leftMatch
    rightMatch = GetRightMatch(sentence, list_of_words)
    #print "Right Match: ", rightMatch

    if len(leftMatch) > len(rightMatch):
        remaining = sentence[len(leftMatch):]
        leftList.append(leftMatch)
        MaxMatch(remaining, list_of_words)
        #leftList.extend(MaxMatch(remaining, list_of_words))
    else:
        remaining = sentence[0:len(sentence) - len(rightMatch)]
        rightList.append(rightMatch)
        MaxMatch(remaining, list_of_words)
        #rightList.extend(MaxMatch(remaining, list_of_words))
        #rightList.reverse()
    #return leftList.extend(rightList)
def PopulateListOfWords(filename):
    # This function creates a dict of words from input file
    # Returns the dict

    list_of_words = {}

    # Read file line by line
    with open(filename) as f:
        for line in f:
            # Get the word and frequency
            split_line = line.rstrip().split()
            word = split_line[0]
            # TODO store frequency if needed
            if list_of_words.get(word) == None:
                # set in dict
                list_of_words[word] = word
    # return the list of files
    return list_of_words

# TODO Command Line arguments handling


def GetSubCost(source, target):
    if source == target:
        return 0
    return 1

def GetMinimumEditDistance(source, target):
    # get length of source and target
    n = len(source)
    m = len(target)

    # create a matrix
    # initialize the first row and first column
    D = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        D[i][0] = D[i-1][0] + 1

    for j in range(1,m+1):
        D[0][j] = D[0][j-1] + 1

    # iterate
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i-1][j] + 1, D[i][j-1] + 1,  D[i - 1][j - 1] + 
                    GetSubCost(source[i - 1], target[j - 1]))
    return D[n][m]

def WriteTokens(output_file, tokens):
    with open(output_file, "a") as f:
        f.write(" ".join(tokens))
        f.write("\n")

def ComputeAverageWER(output_file, ref_file):
    sum_ref = 0
    count = 0
    with open(output_file) as op, open(ref_file) as ref:
        for ref_hash, matched_op in zip(ref, op):
            # Compute List of Reference Hashtag
            base_hashtag = ref_hash.split(" ")

            # Compute List of Computed Hashtag
            matched_output = matched_op.split(" ")

            # Get Minimum Edit Distance
            min_edit = GetMinimumEditDistance(matched_output, base_hashtag)

            # Compute WER
            wer = float(min_edit) / float(len(base_hashtag))
            count += 1
            sum_ref += wer
    return sum_ref / count


if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("hashtag_file", help="Provides the file containing hashtags")
    parser.add_argument("wordlist_file", help="Provides the lexicon")
    parser.add_argument("segment_output_file", help="Provides the file "\
            "that contains segmented output")
    parser.add_argument("reference_file", help="Provides the reference "\
            "segmentation")
    args = parser.parse_args()
    # Get name of file containing hashtags
    hashtag_file = args.hashtag_file
    wordlist_file = args.wordlist_file
    output_file = args.segment_output_file
    ref_file = args.reference_file

    list_of_words = PopulateListOfWords(wordlist_file)

    with open(hashtag_file) as f:
        for line in f:
            # Get the hashtag
            hashtag = line.rstrip()

            # strip the hashtag and convert to lowercase
            hashtag = hashtag.strip('#').lower()

            # Call MaxMatch on the hashtag to get a set of tokens
            MaxMatch(hashtag, list_of_words)
            localLeftList = leftList
            localRightList = rightList
            #print localLeftList, localRightList
            localRightList.reverse()
            #print localRightList
            localLeftList.extend(localRightList)
            list_of_tokens = localLeftList
            leftList = []
            rightList = []
            print list_of_tokens

            # Write the list of tokens to a file
            WriteTokens(output_file, list_of_tokens)

    # Compute average WER
    average_wer = ComputeAverageWER(output_file, ref_file)
    print average_wer


