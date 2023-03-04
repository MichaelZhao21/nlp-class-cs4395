import pickle
from nltk import word_tokenize
from pathlib import Path


def read_file(filename: str) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
    '''
    Reads in the file and tokenizes the text
    '''
    # Open the file and read all lines
    with open(filename, 'r') as file:
        text = ''.join(file.readlines())

        # Clean text by removing newlines and lowercasing
        text = text.replace('\n', ' ').lower()

        # Generate tokens using word_tokenize
        tokens = word_tokenize(text)

        # Unigrams list
        unigrams = tokens
        print('Unigrams (first 50)')
        print(unigrams[:50], '\n')

        # Bigrams list
        bigrams = [(unigrams[k], unigrams[k + 1])
                   for k in range(len(unigrams) - 1)]
        print('Bigrams (first 50)')
        print(bigrams[:50], '\n')

        # Dict of unigram counts
        unigrams_dict = {t: unigrams.count(t) for t in set(unigrams)}

        # Dict of bigram counts
        bigrams_dict = {b: bigrams.count(b) for b in set(bigrams)}
        print(f'Finished generating dictionary of bigrams and unigrams for {filename}\n')

        return (unigrams_dict, bigrams_dict)


def pick(dic: dict, filename: str):
    '''
    Simply pickles a dict in a file
    '''
    with open(f'pickles/{filename}.pickle', 'wb') as file:
        pickle.dump(dic, file)


def main():
    '''
    Main routine
    '''
    # Read file and get unigrams/bigrams dictionary of counts for all data files
    ud_en, bd_en = read_file('data/LangId.train.English')
    ud_fr, bd_fr = read_file('data/LangId.train.French')
    ud_it, bd_it = read_file('data/LangId.train.Italian')

    # Create output dir
    Path('./pickles').mkdir(exist_ok=True)

    # Pickle all dictionaries
    pick(ud_en, 'unigrams_en')
    pick(bd_en, 'bigrams_en')
    pick(ud_fr, 'unigrams_fr')
    pick(bd_fr, 'bigrams_fr')
    pick(ud_it, 'unigrams_it')
    pick(bd_it, 'bigrams_it')


if __name__ == '__main__':
    main()
