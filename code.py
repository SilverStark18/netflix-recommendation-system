import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("netflixData.csv")
print(data.head())

# lets clear the null values for better analysis.
# The dataset contains null values, but before removing the null values, 
# let’s select the columns that we can use to build a Netflix recommendation system:
print(data.isnull().sum())


data = data[["Title", "Description", "Content Type", "Genres"]]
print(data.head())

# let’s drop the rows containing null values and move further:

data = data.dropna()

import nltk
import re
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword=set(stopwords.words('english'))

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
data["Title"] = data["Title"].apply(clean)

# let’s have a look at some samples of the Titles before moving forward:
print(data.Title.sample(10))




feature = data["Genres"].tolist()

# Create an instance of TfidfVectorizer
tfidf = TfidfVectorizer(stop_words="english")

# Fit and transform the vectorizer on our corpus
tfidf_matrix = tfidf.fit_transform(feature)

# Compute the cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)

def netFlix_recommendation(title, similarity = similarity):
    index = indices[title]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[0:10]
    movieindices = [i[0] for i in similarity_scores]
    return data['Title'].iloc[movieindices]

print(netFlix_recommendation("girlfriend"))