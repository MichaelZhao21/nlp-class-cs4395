import pickle
from nltk import word_tokenize, ngrams


def unpick(filename: str) -> dict:
    '''
    Reads pickles from file into a dict
    '''
    with open(f'pickles/{filename}.pickle', 'rb') as file:
        return pickle.load(file)


def calculate_prob(text: str, ud: dict, bd: dict):
    '''
    Calculates the probability a text belongs in a language
    '''
    # Generate count for unique tokens
    V = len(ud)

    # Get unigrams and bigrams from input text
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # Calculate probability using laplace smoothing
    p = 1

    # Loop through all bigrams of test text
    for bigram in bigrams_test:
        n = bd[bigram] if bigram in bd else 0
        d = ud[bigram[0]] if bigram[0] in ud else 0
        p = p * ((n + 1) / (d + V))

    return p


def line_prob(text: str) -> str:
    '''
    Returns the language that the input text
    is most likely to be
    '''
    # Calculate probability for each line
    prob_en = calculate_prob(text, ud_en, bd_en)
    prob_fr = calculate_prob(text, ud_fr, bd_fr)
    prob_it = calculate_prob(text, ud_it, bd_it)

    # Get max prob and return language that matches that max
    max_val = max([prob_en, prob_fr, prob_it])

    if max_val == prob_en:
        return 'English'
    elif max_val == prob_fr:
        return 'French'
    else:
        return 'Italian'


def get_sols():
    '''
    Get all language solutions
    '''
    with open('data/LangId.sol') as file:
        lines = file.readlines()
        return [l.replace('\n', '').split(' ')[1] for l in lines]


def main():
    # Declare these as global as to not pass unneccisarily
    global ud_en, bd_en, ud_fr, bd_fr, ud_it, bd_it

    # Read in pickled files
    ud_en = unpick('unigrams_en')
    bd_en = unpick('bigrams_en')
    ud_fr = unpick('unigrams_fr')
    bd_fr = unpick('bigrams_fr')
    ud_it = unpick('unigrams_it')
    bd_it = unpick('bigrams_it')

    # Get the correct answers
    sols = get_sols()
    num_wrong = 0

    # Loop through test file and calculate probabilities for each line
    with open('data/LangId.test', 'r') as file:
        # Output string
        out = ''

        # Iterate through lines of input file
        for i, line in enumerate(file):
            lang = line_prob(line)
            out += f'{i+1} {lang}\n'

            # Check if language is correct and print if not
            if sols[i] != lang:
                num_wrong += 1
                print(f'Line {i+1} is incorrect!')

        # Write solutions to file
        with open('output', 'w') as output_file:
            output_file.write(out)

        # Print accuracy
        print(f'Accuracy: {(len(sols) - num_wrong) / (len(sols))}')


if __name__ == '__main__':
    main()
