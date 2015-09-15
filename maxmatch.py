#!/usr/bin/python

# Program for word segmentation using the Max-Match algorithm

# Input: A file which consists of the list of words, an input sentence
# Output: Tokenized array of words

from sys import argv
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wordlist", help="Provides the lexicon")
    parser.add_argument("sentence", help="Provides the sentence to be segmented")
    args = parser.parse_args()
    
    filename = args.wordlist
    sentence = args.sentence
    
    # Remove the hashtags and convert to lowercase
    sentence = sentence.strip('#').lower()
    
    # Get the list of words
    list_of_words = PopulateListOfWords(filename)
    
    # Create a token list
    tokens = []
    
    # run algorithm
    tokens = MaxMatch(sentence, list_of_words)
    
    #print list_of_words
    print tokens
