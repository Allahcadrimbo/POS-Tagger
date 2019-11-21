"""
Author: Grant Mitchell
Date: 11/22/19
PA #5 NLP

In this PA we are attempting to create a part of speech (POS) tagger. What this tagger will do is it will take in a
given word and try to decide what kind of POS that word is. What ever the tagger decided it will append a POS tag onto
end of it. We will have two versions of our tagger. The first version is the basic version and the second is the
enhanced version. They will do the following.

Basic Version: OVERALL ACCURACY: 92.11%
- For each word in test data that is found in the training data, assign it the POS tag that maximizes p(tag|word).
- For each word in the test data not found in the training data (i.e., and unknown word), assign it as an NN.
- Reports the accuracy of basic version on a given test file, and also shows a confusion matrix.
  Save this output in a file named basic-tagger-output.txt.

Enhanced Version: OVERALL ACCURACY: 93.36%
- Enhances the basic version by adding extra rules that help it handle unknown words.
- Reports the accuracy of the enhanced version on the same given test file, and also show a confusion matrix.
  Save this output in a file named enhanced-tagger-output.txt.

We will build our knowledge of the "known words" from a file containing training data. This file will contain words
with their correct POS tags. We will record each word and the number of times it is given that tag. This info will
be store in a dict with another dict as it's value and will look like: dict{word1:{tag1:5, tag3:13}, word2:{tag2:7},...}


Example Input: *To use the enhanced version use the "-E" flag
    Basic Version: ./tagger pos-train.txt pos-test.txt > pos-test-with-tags-basic.txt
    Enhanced Version: /tagger pos-train.txt pos-test.txt -E > pos-test-with-tags-enhanced.txt

Output: Both of these will output the testing data with their assigned tags to file after the '>' symbol

Algorithm:
- Grab all of the command line variables and assign them to variables
- Build our training dict
    - Process training data
        - For each word in the file separate the word from the tag
        - Add the word to the dict if it doesn't exist and set the value to be a new dict with one entry tag:1
        - If the word is in the dict check if the tag is in its value dict
            - If it isn't add it and set the value to 1
            - If it is increment its value by 1
    - return the training dict
- Tag the test data
    - For every word pass it in to either the enhanced or basic rules
        - Basic: If the word is in the training dict assign it the most likely tag else it is a NN
        - Enhanced: If the word is in the training dict assign it the most likely tag else follow the extra rules
        - print the word and its assigned tag to stdout
"""

import re
import sys
import argparse


# Processes the training data
# @param train_filename Name of the file containing the training data
# @return trained_tagger Dict with words as the key and a dict as the value. The inner dict contains all POS tags
#         assigned to that word with number of times that tag was assigned to that word as the value
def process_training_data(train_filename):
    # Opens the file containing the training data
    with open(train_filename, "r", encoding="unicode_escape") as train_text:
        trained_tagger = dict()
        # For ever line(word/tag) pair separate the word from the POS tag
        for line in train_text:
            separator_index = line.rfind('/')  # Gets the index of the separator "/" in the line
            word = line[:separator_index]  # Gets the word that is being tagged
            tag = line[separator_index + 1:]  # Gets the tag the word was assigned

            # Need to strip newline chars of tag because it causes issues later when checking the dict for tags
            add_word_to_dict(word, tag.strip("\n"), trained_tagger)
    return trained_tagger


# Adds a word to the dict and adjusts its value accordingly
# @param word The word to be added or adjusted
# @param tag The tag to be added or adjusted in the dict that is the value of the key corresponding to word
# @param Dict with words as the key and a dict as the value. The inner dict contains all POS tags
#        assigned to that word with number of times that tag was assigned to that word as the value
def add_word_to_dict(word, tag, trained_tagger):
    # Checks if the key has already been encountered.
    if word in trained_tagger:
        # Checks if the tag is already in this words dict
        # If it is get the current value and increment it by 1
        if tag in trained_tagger[word]:
            curr_val = trained_tagger[word][tag]
            trained_tagger[word][tag] = curr_val + 1
        # If it isn't add it to the word's dict and set its value to 1
        else:
            trained_tagger[word][tag] = 1
    # If it hasn't the key will be added and the value will be added to its inner dict with a value of 1
    else:
        trained_tagger[word] = {tag: 1}


# Tags the test data with our training dictionary
# @param test_filename Name of the file containing the testing data to be tagged
# @param train_d Dict containing the training data we learned earlier
def tag_test_data(test_filename, train_d):
    with open(test_filename, "r", encoding="unicode_escape") as test_text:
        # Goes through ever word (line) in the test data
        for word in test_text:
            word = word.strip("\n")  # Need to remove the newline char from the test word

            # If true use the enhanced rules else use the basic rules
            if useEnhanced:
                enhanced_rules(word, train_d)
            else:
                basic_rules(word, train_d)


# Tags the word with our basic rule set
# @param word The word to be tagged
# @param train_d The training dict
def basic_rules(word, train_d):
    # If the word was encountered in the training data assign it the most likely tag else say it is a NN
    if word in train_d:
        most_likely_tag = max(train_d[word], key=train_d[word].get)  # Finds the tag/key with the largest value
        print(word + "/" + most_likely_tag)
    else:
        print(word + "/" + "NN")


# Tags the word with our enhanced rule set
# @param word The word to be tagged
# @param train_d The training dict
def enhanced_rules(word, train_d):
    # If the word was encountered in the training data assign it the most likely tag else follow the rules
    if word in train_d:  # Known Word
        most_likely_tag = max(train_d[word], key=train_d[word].get)  # Finds the tag/key with the largest value
        print(word + "/" + most_likely_tag)
    else:  # Unknown Word
        # Rule 1: If it is a proper noun the first letter is probably capitalized
        if word[0].isupper():
            print(word + "/" + "NNP")
        # Rule 2: If it contains a number there is a high chance it is CD
        elif re.search(r'.[0-9].', word):
            print(word + "/" + "CD")
        # Rule 3: If it ends in 's' it could be a plural noun
        elif word[len(word) - 1] == "s":
            print(word + "/" + "NNS")
        # Rule 4: If it ends in 'ly' it might be a RB
        elif word[len(word) - 2:] == "ly":
            print(word + "/" + "RB")
        # Rule 5: If there's a dash between two words there is a high chance it is a JJ
        elif re.search(r'[a-zA-Z]*-[a-zA-Z]', word):
            print(word + "/" + "JJ")
        # Rule 6: If it ends in "ing" it could be a VBG
        elif word[len(word) - 3:] == "ing":
            print(word + "/" + "VBG")
        # Rule 7: Default to NN
        else:
            print(word + "/" + "NN")


if __name__ == "__main__":
    pos_train_filename = sys.argv[1]  # Train data filename
    pos_test_filename = sys.argv[2]  # Test data filename
    useEnhanced = sys.argv.__contains__('-E')  # Check if '-E' flag is set. If it is useEnhanced == True

    # Get the dict containing the processed training data
    trained_dict = process_training_data(pos_train_filename)

    # Tag the test data using the trained_dict
    tag_test_data(pos_test_filename, trained_dict)
