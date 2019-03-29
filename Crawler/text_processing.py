import nltk
import re
import string
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


# if no operator in between two consecutive tokens which are not in the
# 'operators' array then assume 'and' operator should be used
def extract_operators_from_query(query, operators):
    arr = []
    tokens = tokenize_filter_punctuation(query)

    i = 0

    while(i < len(tokens) - 1):
        if(tokens[i] in operators):
            arr.append(tokens[i].lower())
        else:
            if tokens[i + 1] not in operators:
                arr.append('and')
        i += 1

    return arr


def remove_words_from_query(query, words):
    filtered_query = [w for w in query if not w in words]
    return filtered_query


def download_stop_words():
    nltk.download("stopwords")
    nltk.download('punkt')


def split_into_senteces(text):
    sentences = sent_tokenize(text)
    return sentences


def tokenize_filter_punctuation(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(sentence)
    return word_tokens


def remove_non_alpha(word_tokens):
    word_tokens = [re.sub(r'[^a-zA-Z]', "", token)
                   for token in word_tokens]
    return word_tokens


def remove_stop_words(word_tokens):
    stop_words = set(stopwords.words('english'))

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    return filtered_sentence


def normalize(word_tokens):
    tokens = [w.lower() for w in word_tokens]
    return tokens


def stemming(word_tokens):
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in word_tokens]
    return stemmed


def remove_only_numbers(word_tokens):
    word_tokens = [re.sub(r'\b[0-9]+\b\s*', '', token)
                   for token in word_tokens]
    return word_tokens


def remove_empty_space(word_tokens):
    return filter(None, word_tokens)


def remove_figures_from_words(word_tokens):
    word_tokens = [re.sub(r'\d+', '', token) for token in word_tokens]
    return word_tokens


def remove_1_char_words(word_tokens):
    word_tokens = [re.sub(r'\b\w{1,3}\b', '', token) for token in word_tokens]
    return word_tokens


def process_text(text):
    sentences = split_into_senteces(text)
    tokens = set()
    for sentence in sentences:
        word_tokens = tokenize_filter_punctuation(sentence)
        word_tokens = remove_stop_words(word_tokens)
        word_tokens = remove_non_alpha(word_tokens)
        word_tokens = normalize(word_tokens)
        word_tokens = stemming(word_tokens)
        word_tokens = remove_only_numbers(word_tokens)
        word_tokens = remove_figures_from_words(word_tokens)
        word_tokens = remove_1_char_words(word_tokens)
        word_tokens = remove_empty_space(word_tokens)
        tokens.update(word_tokens)

    return tokens
