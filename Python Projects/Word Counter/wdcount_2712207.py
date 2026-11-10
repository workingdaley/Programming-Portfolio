"""
Name: Djesse Jackson
CSU ID: 2712207
Linux ID: dejackso
"""

import sys

def main():

    # error coding to ensure that program doesn't do anything if user does not enter a file name
    if len(sys.argv) < 2:
        print("No file provided")
    else:
        
        # program assumes file is in the same folder as program
        file = open(sys.argv[1])

        # create empty dictionary to be filled with words
        words = {}

        # iterate through file and add words to dictionary, making the key the word count
        # if the word is already in the dicitonary, then add 1 to word count
        for line in file:
            for word in line.split():
                if word.lower() in words:
                    words[word.lower()] += 1
                else:
                    words[word.lower()] = 1

        # sort the dictioinary of words in decending order
        sorted_words = {word: count for word, count in sorted(words.items(), key=lambda item: item[1], reverse=True)}

        # print the sorted words with their word count
        for word, count in sorted_words.items():
            print(word, count)

        # close file
        file.close()

if __name__ == '__main__':
    main()