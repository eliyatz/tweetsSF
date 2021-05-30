# Load DataSet into pandas DataFrame
import pandas as pd
df_tweets = pd.read_csv(r'C:\Users\user\Desktop\sf-data\research\tweets_150521.csv', encoding='utf-8')
df_tweets.head()
tweets = df_tweets[['id','text']].copy()
tweets.head()

# Data Pre-Processing

#---Tokenizing
from sklearn.feature_extraction.text import CountVectorizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models import CoherenceModel

from nltk.tokenize import RegexpTokenizer
from datetime import datetime
import nltk


import pandas as pd
import re
import math

#---StopWord:
nltk.download('stopwords')
from nltk.corpus import stopwords

sf_stop_words = ["@sfbart", "train", '@sfaims', 'transportation', 'sf', 'stmf',
                 '@stmf', '@sfmta_muni','bus', 'san', 'francisco', 'would', '@sfmta_muni',
                 'sfmta_muni', 'it', 'due', 'gentelmen', 'ladies', 'bart',
                 'public','@transportation', '@train', '@it', 'transporation',
                 'bus', 'sf', 'civic', 'bus', 'west', 'one', 'it', 'like', 'th',
                 'amp', 'ob', 'tc', 'thank', 'ca', 'ca', 'see', 'inn', 'gentlemen']
en_stop_words = stopwords.words('english')
en_stop_words.extend(sf_stop_words)

def clean_tweets(df=tweets,
                 tweet_col='text',
                 id_col='id',
                 ):
    df_copy = df.copy()

    # drop rows with empty values
    df_copy.dropna(inplace=True)

    # lower the tweets
    df_copy['preprocessed_' + tweet_col] = df_copy[tweet_col].str.lower()

    # filter out stop words and URLs
    url_re = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    df_copy['preprocessed_' + tweet_col] = df_copy['preprocessed_' + tweet_col].apply(lambda row: ' '.join(
        [word for word in row.split() if (not word in en_stop_words) and (not re.match(url_re, word))]))

    # tokenize the tweets
    tokenizer = RegexpTokenizer('[a-zA-Z]\w+\'?\w*')
    df_copy['tokenized_' + tweet_col] = df_copy['preprocessed_' + tweet_col].apply(lambda row: tokenizer.tokenize(row))
    return df_copy


df_tweets_clean = clean_tweets(tweets)
df_tweets_clean.head()

# Bag of Words
def get_most_freq_words(str, n=None):
    vect = CountVectorizer().fit(str)
    bag_of_words = vect.transform(str)
    sum_words = bag_of_words.sum(axis=0)
    freq = [(word, sum_words[0, idx]) for word, idx in vect.vocabulary_.items()]
    freq = sorted(freq, key=lambda x: x[1], reverse=True)
    return freq[:n]
freq_word = get_most_freq_words([word for tweet in df_tweets_clean.tokenized_text for word in tweet], 10)
#print(freq_word(10))

# WordCloud
#import numpy as np
#twitter = Image.open(r'C:\Users\user\Desktop\sf-data\tweets\graphs\wordcloud\tweet_mask.png').convert('RGBA')
#twitter_mask = np.array(twitter)


# Topic Coherence:
'''
   We want to calculate how much Topic My Data cal produce
   In the result plot You should gahh the plto, which is the number of Topics
'''

import matplotlib.pyplot as plt
tweets_dictionary = Dictionary(df_tweets_clean.tokenized_text)
# build the corpus i.e. vectors with the number of occurence of each word per tweet
tweets_corpus = [tweets_dictionary.doc2bow(tweet) for tweet in df_tweets_clean.tokenized_text]
# compute coherence
tweets_coherence = []
for nb_topics in range(1,36):
    lda = LdaModel(tweets_corpus, num_topics = nb_topics, id2word = tweets_dictionary, passes=10)
    cohm = CoherenceModel(model=lda, corpus=tweets_corpus, dictionary=tweets_dictionary, coherence='u_mass')
    coh = cohm.get_coherence()
    tweets_coherence.append(coh)
# visualize coherence
plt.figure(figsize=(10,5))
plt.plot(range(1,36),tweets_coherence)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence Score");

# LDA Topics Modeling
import matplotlib.gridspec as gridspec
#k= int(print(input("Number of Topics: ")))
k = 8
tweets_lda = LdaModel(tweets_corpus, num_topics=k, id2word=tweets_dictionary, passes=10)
def plot_top_words(lda=tweets_lda, nb_topics=k, nb_words=10):
    top_words = [[word for word, _ in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]
    top_betas = [[beta for _, beta in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]
    gs = gridspec.GridSpec(round(math.sqrt(k)) + 1, round(math.sqrt(k)) + 1)
    gs.update(wspace=0.5, hspace=0.5)
    plt.figure(figsize=(20, 15))
    for i in range(nb_topics):
        ax = plt.subplot(gs[i])
        plt.barh(range(nb_words), top_betas[i][:nb_words], align='center', color='blue', ecolor='black')
        ax.invert_yaxis()
        ax.set_yticks(range(nb_words))
        ax.set_yticklabels(top_words[i][:nb_words])
        plt.title("Topic " + str(i))
plt.show(plot_top_words())

# Testing Number of relevant Topics
import pyLDAvis.gensim


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
pyLDA = pyLDAvis.gensim.prepare(tweets_lda, tweets_corpus, tweets_dictionary)
pyLDAvis.show(pyLDA)



# Each Tweets Belong toEach Topic?
def format_topics_sentences(ldamodel=tweets_lda, corpus=tweets_corpus, texts=tweets['text']):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=tweets_lda, corpus=tweets_corpus, texts=tweets['text'])

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['id', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
df_dominant_topic['id'] = tweets['id']

# Show
df_dominant_topic.head(10)

# Save File
result = pd.concat([df_tweets, df_topic_sents_keywords],axis =1).reindex(df_tweets.index)
result.to_csv(r'C:\Users\user\Desktop\sf-data\research\250521_tweets_LDA.csv', encoding = 'utf-8')