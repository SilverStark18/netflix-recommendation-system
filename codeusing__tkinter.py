import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import font

data = pd.read_csv("netflixData.csv")
print(data.head())
data = data[["Title", "Description", "Content Type", "Genres"]]
print(data.head())
data= data.dropna()
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Assuming 'data' is a pandas DataFrame and 'Genres' is a column in that DataFrame
feature = data["Genres"].tolist()

# Create an instance of TfidfVectorizer
tfidf = TfidfVectorizer(stop_words="english")

# Fit and transform the vectorizer on our corpus
tfidf_matrix = tfidf.fit_transform(feature)

# Compute the cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)
indices = pd.Series(data.index, index=data['Title']).drop_duplicates()


def netFlix_recommendation():
    title = e1.get()
    index = indices[title]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[0:10]
    movieindices = [i[0] for i in similarity_scores]
    result = data['Title'].iloc[movieindices]
    result_label.config(text='\n'.join(result))

master = tk.Tk()
master.geometry('520x520') 
master.configure(bg='white')  
tk.Label(master, 
         text="Enter a movie title 🎬", 
         bg='#f0f0f0', 
         fg='black').grid(row=0, column=0, columnspan=2)

e1 = tk.Entry(master)
e1.grid(row=1, column=0, columnspan=2)

button = tk.Button(master, 
                   text='Recommend 🍿', 
                   command=netFlix_recommendation, 
                   bg='#d3d3d3',  
                   fg='black')
button.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(master, text="", bg='#f0f0f0', fg='black', justify='left')
result_label.grid(row=3, column=0, columnspan=2)


bold_font = font.Font(weight="bold")
result_label['font'] = bold_font

master.mainloop()