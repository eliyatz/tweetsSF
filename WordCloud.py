from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np

data = pd.read_csv(r'C:\Users\user\Desktop\sf-data\research\250521_tweets_LDA.csv', encoding='utf-8')
text = data.text.values
STOPWORDS.update(["one", "sfo", "lake", "merritt", "transit", "bike", "ride", "near", "woman",
                  "opened", "take", "bay", "tree", "street", "sidewalk", "metro", "way", "day",
                  "today", "downtown", "berkeley", "will", "next", "oakland", "sfbart", "via",
                  "sf", "request", "new", "stop", "https", "co", "san", "station", "train", "st",
                  "sanfrancisco", "bart", "glen", "park", "montgomery", "powell", "examiner", "francisco",
                  "ca", "bus", "muni", "california", "daly", "city", "airport", "civic", "center",
                  "muni metro", "california", "iphone", "bartlett", "international", "airport", "16th",
                  "center", "un", "fruitvale", "transportation", "fruitvale", "vw", "hainesforsf'",
                  "castro", "arch", "randolph", "monday", "around", "two", "ncolor", "go", "amp", "got",
                  "la", "19th", "oscar", "grant", "nmake", "mission", "embarcadero", "back", "ave", "plaza",
                  "22nd", "let", "macarthur", "taking", "chronicle", "columbus", "market", "year", "first",
                  "nan", "thing", "man", "ashby", "mins", "getting", "case", "resolved", "municipal", "area",
                  "bayarea", "nlicense", "plate", "minutes", "west", "north", "may", "re", "millbrae", ""])

twitter = Image.open(r'C:\Users\user\Desktop\sf-data\tweets\graphs\wordcloud\tweet_mask.png').convert('RGBA')

twitter_mask = np.array(twitter)

wordcloud = WordCloud(max_words=100,
                      width=300,
                      height=200,
                      background_color='white',
                      mask=twitter_mask,
                      colormap='winter',
                      contour_width=1,
                      contour_color='steelblue',
                      stopwords=STOPWORDS).generate(str(text))

image_colors = ImageColorGenerator(twitter_mask)

fig = plt.figure(
    figsize=(30, 20), )
# facecolor = 'c',
# edgecolor = 'k')

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()
