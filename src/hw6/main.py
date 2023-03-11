from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import nltk
import re
import pickle

# This page is the home page of the wiki for the game Hollow Knight
URL = 'https://hollowknight.fandom.com/wiki/Hollow_Knight_Wiki'

# URLs to exclude that contain the following text
# This needs to be manually done to ignore pages with irrelevant info
EXCLUDE_CONTAIN = [
    '/wiki/Hollow_Knight_Wiki',
    'Hollow_Knight_Wiki:',
    '//hollowknight.fandom.com',
    'discord.gg',
    'Special:',
    'Blog:',
    'Category:',
    'hollow-knight-fanon',
    'www.fandom.com/',
    '//community.fandom.com/wiki/Community_Central',
    'auth.fandom.com',
    'community.fandom.com',
    'about.fandom.com',
    'google',
    'apple',
    'reddit',
    'Sitemap',
    '#',
    'bg/wiki/',
    'de/wiki/',
    'es/wiki/',
    'fr/wiki/',
    'it/wiki/',
    'pl/wiki/',
    'pt/wiki/',
    'ru/wiki/',
    'uk/wiki/',
    'zh/wiki/',
    'https://www.muthead.com/',
    'https://www.futhead.com/',
    'https://www.fanatical.com/',
    'https://www.facebook.com/getfandom',
    'https://twitter.com/getfandom',
    'https://www.youtube.com/fandomentertainment',
    'https://www.instagram.com/getfandom/',
    'https://www.linkedin.com/company/157252',
    'http://bit.ly/en-spotlight-universalconquest',
    'https://letsgoluna.fandom.com/wiki/Let%27s_Go_Luna!_Wiki',
    'https://club57.fandom.com/wiki/Club_57_Wiki',
    'https://bit.ly/FandomIG',
    'https://bit.ly/TikTokFandom',
    'https://bit.ly/FanLabWikiBar',
    'https://fandom.com/fancentral/home'
]


def crawl() -> list[str]:
    '''
    Crawls the specified URL and extracts all links
    Then, fetch all texts from these links and write each page to a doc
    '''
    # Fetch the text
    uf = urllib.request.urlopen(URL)
    html = uf.read()

    # Parse text with bs
    soup = BeautifulSoup(html, features='html.parser')

    # Extract set of outlinks
    href_set = set()
    for link in soup.find_all('a'):
        # Get the href attribute of the anchor tag
        url = link.get('href')

        # Make sure the href is valid and does not contain anything from the exclude list
        if url is not None and not any(sub in url for sub in EXCLUDE_CONTAIN):
            # If relative link, append current origin to URL
            if url.startswith('http'):
                href_set.add(url)
            else:
                href_set.add('https://hollowknight.fandom.com' + url)

    # Convert the set to a list
    url_list = list(href_set)
    print(f'Gotten {len(url_list)} outlinks from {URL}!')
    print(url_list)
    return url_list


def scrape_text(url_list: list[str]):
    '''
    Scrapes a list of URLs and writes the content to their own files
    '''
    # Make sure output directory exists
    Path('output-raw').mkdir(parents=True, exist_ok=True)

    # Get content for each page
    for url in url_list:
        try:
            print(f'Processing {url}')

            # Fetch HTML content
            uf = urllib.request.urlopen(url)
            html = uf.read()

            # Parse data with BS
            soup = BeautifulSoup(html, features='html.parser')

            # Clean up by removing Javascript and CSS
            for data in soup(['style', 'script']):
                # Remove tags
                data.decompose()

            # Open output file and write text
            output_dir = 'output-raw/' + \
                url.replace('https://hollowknight.fandom.com/',
                            '').replace('/', '-')
            with open(output_dir, 'w') as file:
                file.write(soup.get_text())
            print('\t', 'Done!')
        except (urllib.request.HTTPError, urllib.request.URLError) as e:
            # Catch exceptions if we cannot open the page or is invalid URL
            print('\t', e)


def loop_through_dir(dirname: str, func):
    '''
    Helper function to loop through a directory,
    open the file, and call a function, passing in the file pointer
    '''
    for filename in os.listdir(dirname):
        f = os.path.join(dirname, filename)
        with open(f, 'r') as file:
            func(file)


def clean_and_extract_sentences(text: str, filename: str):
    '''
    Cleans the raw text, splits it into sentences,
    and writes the sentences to a new file
    '''
    print('Cleaning', filename)

    # Make sure output dir exists
    Path('output-sent').mkdir(parents=True, exist_ok=True)

    # Get text and split by newlines
    text_list = text.split('\n')

    # Remove blank lines or lines with whitespace
    processed_text_list = [s.strip() for s in list(
        filter(lambda x: not x.isspace() and x != '', text_list))]

    # Add a period at the end of each line to help the sentence tokenizer
    processed_text_list = [s if s.endswith(
        '.') else s + '.' for s in processed_text_list]

    # Rejoin all text into string for NLTK to use
    text = '\n'.join(processed_text_list)

    # Remove all content before "Talk (0)." -- everything above is the page header
    # Also remove all content after "Compendium." -- everything below is the page footer
    # Note: this of course doesn't cover all repeated text and only applies to the pages in the original domain
    loc = text.find('Talk (0).')
    loc2 = text.find('Compendium.')
    if loc != -1 and loc2 != -1:
        text = text[(loc + 10):loc2]

    # Extract sentences from the text
    sentences = nltk.sent_tokenize(text)

    # Write to file
    with open(filename.replace('output-raw', 'output-sent'), 'w') as file:
        file.write('\n'.join(sentences))


def parse_words(text: str):
    '''
    Parse through a string and clean up the text (remove punctuation & lowercase).
    Then remove stop words and return as a list of tokens
    '''
    text = re.sub(r'[.?!,:;()\-\n\d]',' ', text.lower())
    tokens = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    return [t for t in tokens if not t in stop_words]


def top_terms():
    '''
    Calculate the frequencies of all words
    and print out the top 40
    '''
    # First get a list of all words, cleaned up
    all_words = []
    loop_through_dir('output-sent', lambda file: all_words.extend(parse_words('\n'.join(file.readlines()))))

    # Count the words (getting the frequency dictionary)
    freq_dict = { t: all_words.count(t) for t in all_words }

    # Sort frequency dictionary by frequency of words
    sorted_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}

    # Convert to list of tuples
    freq_list = [(k, v) for k, v in sorted_dict.items()]

    # Print out the top 40 words
    print('The top 40 words:', freq_list[:40])


def has_term(word: str, sent: str) -> bool:
    '''
    Helper function that returns true if the word is in the sentence (cleaned up)
    '''
    text = re.sub(r'[.?!,:;()\-\n\d]',' ', sent.lower())
    return word in text


def build_knowledge_base(top_ten: list[str]):
    '''
    Generate a knowledge base by creating a dictionary of the
    key terms with values being the list of all sentences that
    pertain to the key term.
    '''
    # Get list of all sentences (as canidates to add to knowledge base)
    all_sents = []
    loop_through_dir('output-sent', lambda file: all_sents.extend(file.readlines()))

    # Create the knowledge base using a combination of list and dictionary comprehension
    knowledge = {word: [sent for sent in all_sents if has_term(word, sent)] for word in top_ten }
    print("\nHollow Knight Knowledge Base:\n")
    print(knowledge)

    # Pickle the knowledge base
    with open('knowledge.pkl', 'wb') as file:
        pickle.dump(knowledge, file)


def main():
    # 1. Output a list of >15 relavent URLs to the topic
    url_list = crawl()

    # 2. Loop through the URLs and scrape text data from them
    scrape_text(url_list)

    # 3. Loop through the raw text and clean/extract sentences, then write to a new file
    loop_through_dir(
        'output-raw',
        lambda file: clean_and_extract_sentences('\n'.join(file.readlines()), file.name)
    )

    # 4. Extract 40 most important terms
    top_terms()

    # 5. Manually determine top 10 words
    top_ten = ['knight', 'hollow', 'nail', 'dream', 'map', 'essence', 'soul', 'hallownest', 'enemies', 'void']

    # 6. Build knowledge base (Python dict)
    build_knowledge_base(top_ten)

    # 7. Write-up: https://github.com/MichaelZhao21/nlp-class-cs4395/tree/master/src/hw6/writeup.md


if __name__ == '__main__':
    main()
