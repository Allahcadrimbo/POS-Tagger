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
