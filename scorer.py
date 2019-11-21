"""
Author: Grant Mitchell
Date: 11/22/19
PA #5 NLP

This program is the scorer for the tagger program. We take the POS tags assigned to the test data and compare it to the
POS tags of the correct tags for the words. When we do this we compute the overall accuracy and a confusion matrix. The
confusion matrix is as follows:

- For correct classifications
    DET DET : 10,000
    meaning that 10,000 determiners (DET) were correctly identified as determiners.

- For incorrect classifications report (for example)
    NN VBD : 5
    meaning that 5 past tense verbs (VBD) were incorrectly tagged as nouns (NN). Please list the predicted tag first
    (NN) followed by the actual gold tag (VBD)

Example Input:
    ./scorer pos-test-with-tags-basic.txt pos-key.txt > basic-tagger-scores.txt

Example Output:
    The total accuracy of this POS Tagger is: 92.1177671406448%
    -------------------------------Correct POS Pairs-----------------------------------------------------
    , ,: 3070
    PRP PRP: 1042
    VBD VBD: 1573
    RB RB: 1724
    -------------------------------Incorrect POS Pairs-----------------------------------------------------
    DT RB: 14
    NN VB: 261
    VBN VBD: 223

Algorithm:
- Grab all of the command line variables and assign them to variables
- Score test tagging
    - Process test and key files
        - For each line in the file extract just the POS tag and add it to a list
        - End up with two list (list of test tags and list of key tags)
    - Calculate the scores
        - For each index pair in the two lists compare their tags
            - If they are the same the tagger got it correct and we should increment the correct counter
            - Concatenate the tags into one string and add it to the correct dict and if it is already in the dict we
              increment the value. This will give us a value for the number of occurrences
            - If they are different do the same thing as the above step but add it to the incorrect dict
        - Calculate the overall accuracy num of correct/num of tags * 100
    - Print the scores to stdout
"""
import re
import sys


# A processed file class. Each processed file will have a list of tags and the number of tags
class ProcessedFile:
    def __init__(self, tlist, num):
        self.tag_list = tlist
        self.num_tags = num


# This function begins the process of scoring the tags assigned to the test data.
# @param tagged_test_filename This is the name of the file containing the tagged test data
# @param key_filename Name of the file containing the test data with their correct tags
def score_test_tagging(tagged_test_filename, key_filename):
    # Process the test file and returns an instance of ProcessedFile
    test_processed = process_file(tagged_test_filename)

    # Process the key file and return and instance of ProcessedFile
    key_processed = process_file(key_filename)

    # If the number of tags is the same in each file continue else let the user know there is an issue
    if test_processed.num_tags == key_processed.num_tags:
        # Calculate the scores
        calculate_scores(test_processed.tag_list, key_processed.tag_list, test_processed.num_tags)
    else:
        print("Woah it looks like there has been a mistake. The number of tags to compare don't match!")


# Processes each file extracting the list of tags and the number of tags
# @param filename Name of the file to be processed
# @return An instance of ProcessedFile with the corresponding values for this particular file
def process_file(filename):
    tags_list = list()
    num_of_tags = 0
    # Open the file
    with open(filename, "r", encoding="unicode_escape") as text:
        # For each line/(word/tag pair) in the file extract just the tag and add it to a list
        for line in text:
            num_of_tags += 1  # Count the number of total tagged words to use in the accuracy calculation
            separator_index = line.rfind('/')  # Gets the index of the separator "/" in the line
            tag = line[separator_index + 1:]  # Gets the tag the word was assigned
            tags_list.append(tag.strip("\n"))  # Need to strip the tags of possible newline chars and add it to the list
    return ProcessedFile(tags_list, num_of_tags)


# Compare the two lists of tags and calculate the confusion matrix info
# @param test_tags List of tags from the test file
# @param key_tags List of tags from the key file
def calculate_scores(test_tags, key_tags, total):
    correct_dict = dict()
    incorrect_dict = dict()
    num_of_correct = 0

    # Loop through each POS tag in both the test and key list in parallel
    # Zip will map the similar indexes between the two list so we can treat it as one entity. This allows us to loop
    # through both lists in one for loop
    for test, key in zip(test_tags, key_tags):
        # Concatenate the two POS tags into one pair of POS tags
        pair = test + " " + key

        # If the test tag and key tag are the same then we tagged that word correctly
        if test == key:  # Correct Predictions
            num_of_correct += 1
            add_pair_to_dict(correct_dict, pair)
        else:  # Incorrect Predictions
            add_pair_to_dict(incorrect_dict, pair)

    # Calculate the accuracy and multiply by a 100 to get it in percent form
    accuracy = (num_of_correct/total) * 100

    # Prints the information calculated above
    print_scores(correct_dict, incorrect_dict, accuracy)


# Add the POS pair to conf_dict or adjust its value if it is already in the dict
# @param conf_dict Contains pairs of POS tags as the key and the number of occurrences of that pair as the value
# @param pair The pair of POS tags. The first tag is the prediction and the second is the correct tag
def add_pair_to_dict(conf_dict, pair):
    # If the pair is already in our confusion matrix dict then increment its value else add it and set it to 1
    if pair in conf_dict:
        conf_dict[pair] += 1
    else:
        conf_dict[pair] = 1


# Prints the score info
# @param correct Dict containing POS pairs that are correct and the number of their occurrences
# @param incorrect Dict containing POS pairs that are incorrect and the number of their occurrences
# @param accuracy The total accuracy of this tagger in percent form
def print_scores(correct, incorrect, accuracy):
    # Print the overall accuracy
    print("The total accuracy of this POS Tagger is: " + str(accuracy) + "%")

    print("-------------------------------Correct POS Pairs-----------------------------------------------------")
    # Print the correct POS pairs and their respective values
    for key, value in correct.items():
        print(key + ": " + str(value))

    print("-------------------------------Incorrect POS Pairs-----------------------------------------------------")
    # Print the incorrect POS pairs and their respective values
    for key, value in incorrect.items():
        print(key + ": " + str(value))


if __name__ == "__main__":
    pos_test_tagged_filename = sys.argv[1]  # Test data with POS tags filename
    pos_key_filename = sys.argv[2]  # Correct POS Tags filename

    score_test_tagging(pos_test_tagged_filename, pos_key_filename)
