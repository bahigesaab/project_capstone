import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('stopwords')
nltk.download('punkt')


# function to plot most frequent terms
def freq_words(x, terms=30):
    all_words = ''.join(map(str, [text for text in x]))
    all_words = all_words.split()

    fdist = FreqDist(all_words)
    words_df = pd.DataFrame({'word': list(fdist.keys()), 'count': list(fdist.values())})

    # selecting most frequent words
    d = words_df.nlargest(columns="count", n=terms)
    fig = plt.figure(figsize=(20, 15))
    ax = sns.barplot(data=d, x="count", y="word")
    ax.set_xlabel("count", fontsize=20)
    ax.set_ylabel("word", fontsize=20)
    ax.set_title("Frequency of Words Barchart", fontsize=25)
    ax.tick_params(labelsize=20)
    return fig


stop_words = stopwords.words('english')


def preprocess_text(text):
    # remove unwanted characters, numbers and symbols
    text_preprocessed = text.replace("[^a-zA-Z#]", ' ')
    # convert to lower
    text_preprocessed = text_preprocessed.lower()
    text_preprocessed = text_preprocessed.strip()
    return text_preprocessed


def remove_stopwords(text):
    # remove stopwords and words < 2 chars
    common_words = ["place", "lebanese", "site", "venue", "time", "area", "visit", "tour"]
    stop_words.extend(common_words)
    tokens = nltk.word_tokenize(text)
    text = ' '.join([w for w in tokens if w not in stop_words and len(w) > 2])
    return text


# # lemmatize using spacy
# nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
#
#
# def lemmatization(text, tags=['NOUN', 'ADJ']):  # filter noun and adjective
#     doc = nlp(text)
#     output = ' '.join([token.lemma_ for token in doc if token.pos_ in tags])
#     return output

