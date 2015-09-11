#!/usr/bin/python

# Program for word segmentation using the Max-Match algorithm

# Input: A file which consists of the list of words, an input sentence
# Output: Tokenized array of words

from sys import argv

def get_cost_sub(source_char, target_char):
    if source_char == target_char:
        return 0
    return 2

def MaxMatch(sentence, list_of_words):
    tokens = []
    
    if sentence == "":
        return tokens
    
    for i in xrange(len(sentence), 0, -1):
        if i == 1:
            tokens.append(sentence[0])
            rest = sentence[i:]
            tokens.extend(MaxMatch(rest, list_of_words))
            break
        if list_of_words.get(sentence[0:i]) != None:
            # Found in dict
            tokens.append(sentence[0:i])
            # Compute the rest
            rest = sentence[i:]
            tokens.extend(MaxMatch(rest, list_of_words))
            break
    return tokens

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

if __name__ == "__main__":
    filename = argv[1]
    sentence = argv[2]
    
    # Remove the hashtags and convert to lowercase
    sentence = sentence.strip('#').lower()
    
    # This is actually useless at this point of time
    if filename == "" or filename==None:
        print "Filename missing"
        print "Syntax: maxmatch filename 'sentence'"
        exit()
        
    if sentence == "" or sentence == None:
        print "Sentence missing"
        print "Syntax: maxmatch filename 'sentence'"
        exit()
        
    # Get the list of words
    list_of_words = PopulateListOfWords(filename)
    
    # Create a token list
    tokens = []
    
    # run algorithm
    tokens = MaxMatch(sentence, list_of_words)
    
    #print list_of_words
    print tokens
