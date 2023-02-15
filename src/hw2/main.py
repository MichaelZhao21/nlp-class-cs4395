import sys
import re
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random


def get_datafile_path() -> str:
    '''
    Reads in the datafile path from the command line arguments
    and returns an error if not found
    '''
    # Check to make sure datafile path is defined
    if len(sys.argv) < 2:
        print('Error: no datafile path defined in the command line arguments')
        sys.exit(1)

    return sys.argv[1]


def read_file(file_path: str) -> str:
    '''
    Reads in all lines of the file
    '''
    with open(file_path) as file:
        return ''.join(file.readlines())


def preprocess(raw_text: str) -> tuple[list[str], list[str]]:
    '''
    Preprocess the text (question 3)
    '''
    # Remove all punctuation and lowercase
    text = re.sub(r'[.?!,:;()\-\n\d]', ' ', raw_text.lower())

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    sw = stopwords.words('english')
    tokens_no_stop = [t for t in tokens if t not in sw]

    # Lemmatize and get unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens_no_stop]
    lemmas_unique = list(set(lemmas))

    # Part of speech tagging
    tags = pos_tag(lemmas_unique)
    print(f'1st 20 POS-tagged lemmas: {tags[:20]}')

    # Get only nouns
    lemmas_nouns = [t[0] for t in tags if t[1].startswith('N')]

    # Print stats
    print(f'Total tokens: {len(tokens)}')
    print(f'Total nouns: {len(lemmas_nouns)}')

    return (tokens, lemmas_nouns)


def get_freq_list(tokens: list[str], lemmas: list[str]) -> dict[str, int]:
    '''
    Figures out the frequency of nouns and stores it in a dictionary
    '''
    # Dict of frequencies
    fd = {}

    # Loop through all tokens and check it against the lemma list
    for t in tokens:
        if t in lemmas:
            # If token in output list, increment the counter;
            # otherwise initialize the counter
            if t in fd:
                fd[t] += 1
            else:
                fd[t] = 1

    # Convert the dict to a list of tuples
    fd_list = list(fd.items())

    # Sort the list by count
    fd_list.sort(key=lambda a: a[1], reverse=True)

    # Return the 50 most common words
    return [item[0] for item in fd_list][:50]


def guessing_game(poss_words: list[str]):
    '''
    Runs a guessing game based on the instructions!
    '''
    # Start user off with 5 points; game ends if score is negative
    points = 5

    # Score is num of words guessed
    score = 0

    # Randomly choose secret word and convert it to a list
    word = list(random.choice(poss_words))
    print(word)

    # Create display string for guessed letters
    display = list('_' * len(word))

    # Create set of guessed letters so user cannot farm points
    guessed = set()

    # Print welcome message
    print('Let\'s play a guessing game!')

    # Main game loop
    while points >= 0:
        # Print out display and ask user for input
        print(' '.join(display))
        guess = input('Guess a letter: ')

        # Check to see if guess is empty
        if guess == '' or len(guess) > 1:
            print('You need to enter a single character!')
            continue

        # Check to see if user entered exit character (!)
        if guess == '!':
            break

        # Check if already guessed
        if guess in guessed:
            print('Letter', guess, 'has already been guessed!')
            continue

        # Add guess to guessed list
        guessed.add(guess)

        # Check if letter is in word
        if guess in word:
            print('Right!', end=' ')

            # Replace all correct letters in string
            for i in range(len(word)):
                if guess == word[i]:
                    display[i] = guess

            # Add to score if right
            points += 1
        else:
            # Otherwise, print error and subtract from score
            if points > 0:
                print('Sorry, guess again.', end=' ')
            points -= 1

        # Print score if not less than 0
        if points >= 0:
            print('Score is', points)

        # If user has guessed entire word then print end text
        if word == display:
            # Print end text
            print('You solved it!\n')
            print('Current score:', points, '\n')
            print('Guess another word')

            # Increment score
            score += 1

            # Reset game
            word = list(random.choice(poss_words))
            display = list('_' * len(word))
            guessed.clear()
            print(word)

    # Print game over message
    print('\nGame over! You guessed', score, 'words')


def main():
    '''
    Main routine
    '''
    # Get the datafile path
    datafile_path = get_datafile_path()

    # Read the file
    text = read_file(datafile_path)

    # Lexical diversity (2)
    tokens = word_tokenize(text)
    print(f'Lexical Diversity: {len(set(tokens)) / len(tokens)}')

    # Preprocess text (3)
    (tokens, lemmas_nouns) = preprocess(text)

    # Create list of 50 most frequent tokens (4)
    tokens_freq = get_freq_list(tokens, lemmas_nouns)

    # Run the guessing game (5)
    guessing_game(tokens_freq)


if __name__ == '__main__':
    main()
