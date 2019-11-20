import re
import sys


def process_training_data(train_filename):

    with open(train_filename, "r", encoding="unicode_escape") as train_text:
        trained_tagger = dict()
        for line in train_text:
            separator_index = line.rfind('/')  # Gets the index of the separator "/" in the line
            word = line[:separator_index]  # Gets the word that is being tagged
            tag = line[separator_index + 1:]  # Gets the tag the word was assigned

            add_word_to_dict(word, tag.strip("\n"), trained_tagger)
    return trained_tagger


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


def tag_test_data_basic(test_filename, train_d):
    with open(test_filename, "r", encoding="unicode_escape") as test_text:
        # Goes through ever word (line) in the test data
        for word in test_text:
            word = word.strip("\n")  # Need to remove the newline char from the test word
            # If the word was encountered in the training data assign it the most likely tag else say it is a NN
            if word in train_d:
                most_likely_tag = max(train_d[word], key=train_d[word].get)  # Finds the tag/key with the largest value
                print(word + "/" + most_likely_tag)
            else:
                print(word + "/" + "NN")


if __name__ == "__main__":
    sys.stdout = open('pos-test-with-tags-basic.txt', 'w')
    pos_train_filename = sys.argv[1]  # Train data filename
    pos_test_filename = sys.argv[2]  # Test data filename

    trained_dict = process_training_data(pos_train_filename)

    tag_test_data_basic(pos_test_filename, trained_dict)
