import math
import nltk
import sys
import os
import re
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            result[filename] = f.read()

    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Convert document to lower case then split into individual words
    result = nltk.word_tokenize(document.lower())
    # Remove any words that don't contain one alphabetic charachter
    loop_over = result.copy()
    for i in range(len(loop_over)):
        word = loop_over[i]
        if word in nltk.corpus.stopwords.words("english"):
            result.remove(word)
            # No need to remove punctuation
            continue
        # Remove anything that isn't white space or a letter or num
        stripped_word = re.sub("[^\w\s]", "", word)
        # If no match or if the word is a stop word
        if stripped_word == "":
            result.remove(word)
        else:
            # Replace the old word for the stripped word
            result[result.index(word)] = stripped_word

    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    An improvement to be made would be to sort words alphabetically this would make gets quicker (log(n) instead of n), which would make this  nlog(n) instead of n^2.
    """
    result = {}
    for filename in documents:
        print(filename)
        for word in documents[filename]:
            if word == "on":
                print("on found in", filename)
            # Try and add the word to the dict
            word_set = result.get(word, set())
            # Using a set so you can add duplicate filenames (if the word appears multiple times in the same file and it won't be duplicated)
            word_set.add(filename)
            result[word] = word_set

    # Now calculate the idfs - n time complexity
    # print(result)
    num_docs = len(documents)
    for word in result:
        # The word on generates a set with only 1 item
        result[word] = math.log(num_docs/len(result[word]))

    return result


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
