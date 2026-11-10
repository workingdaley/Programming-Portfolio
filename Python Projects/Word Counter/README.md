# Word Counter (Python)

A command-line program that counts word frequency in a text file and prints results sorted from most to least frequent.

## What It Does

Given a text file, the program:

1. Reads the file line by line, splitting each line into individual words.
2. Builds a frequency dictionary, treating words as case-insensitive (`"The"` and `"the"` count as the same word).
3. Sorts the resulting word counts in descending order by frequency.
4. Prints each word alongside its total count.

## Usage

```
python wdcount_2712207.py <text_file>.txt
```

## Skills Demonstrated

- File I/O and text processing
- Dictionary-based frequency counting
- Sorting data structures by value using a custom key function
