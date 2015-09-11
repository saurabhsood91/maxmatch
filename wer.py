from sys import argv
from maxmatch import *

def get_cost_sub(source_char, target_char):
    if source_char == target_char:
        return 0
    return 2

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
            D[i][j] = min(D[i-1][j] + 1, D[i][j-1] + 1, D[i-1][j-1] + 1)
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
            # print min_edit, ":", len(base_hashtag)
            wer = min_edit / float(len(base_hashtag))
            count += 1
            sum_ref += wer
    return sum_ref / count


if __name__ == "__main__":
    # Get name of file containing hashtags
    hashtag_file = argv[1]
    wordlist_file = argv[2]
    output_file = argv[3]
    ref_file = argv[4]

    list_of_words = PopulateListOfWords(wordlist_file)

    with open(hashtag_file) as f:
        for line in f:
            # Get the hashtag
            hashtag = line.rstrip()

            # strip the hashtag and convert to lowercase
            hashtag = hashtag.strip('#').lower()

            # Call MaxMatch on the hashtag to get a set of tokens
            list_of_tokens = MaxMatch(hashtag, list_of_words)
            
            # Write the list of tokens to a file
            WriteTokens(output_file, list_of_tokens)

    # Compute average WER
    average_wer = ComputeAverageWER(output_file, ref_file)
    print average_wer


