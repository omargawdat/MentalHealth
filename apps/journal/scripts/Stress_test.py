#Stress_test.py


## warnings
import warnings
warnings.filterwarnings("ignore")

## for data
from MentalHealth.settings.common import BASE_DIR
import numpy as np
import pandas as pd

## for plotting
import matplotlib.pyplot as plt
import seaborn as sns

## Bag of Words
from sklearn.feature_extraction.text import CountVectorizer

## TF-IDF 
from sklearn.feature_extraction.text import TfidfVectorizer

## Train-Test Split
from sklearn.model_selection import train_test_split

## for processing
import nltk
import re
import ftfy
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

## Feature selection
from sklearn import feature_selection

## Support vector machine
from sklearn.pipeline import Pipeline
import sklearn.metrics as skm
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC

## for saving and loading model
import pickle

## for word embedding with Spacy
import spacy
import en_core_web_lg


# In[2]:


# Expand Contraction
cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)


# In[3]:


## Function to perform stepwise cleaning process
def text_cleaner(tweet):

    cleaned_tweets = []
    tweet = tweet.lower() #lowercase
    
    # if url links then don't append to avoid news articles
    # also check tweet length, save those > 5 
    if re.match("(\w+:\/\/\S+)", tweet) == None and len(tweet) > 5:
    
        #remove hashtag, @mention, emoji and image URLs
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\#[A-Za-z0-9]+)|(<.>)|(pic\.twitter\.com\/.*)", " ", tweet).split())

        #fix weirdly encoded texts
        tweet = ftfy.fix_text(tweet)

        #expand contraction
        tweet = expandContractions(tweet)


        #remove punctuation
        tweet = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", tweet).split())

        #stop words and lemmatization
        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.word_tokenize(tweet)

        lemmatizer=WordNetLemmatizer()
        filtered_sentence = [lemmatizer.lemmatize(word) for word in word_tokens if not word in stop_words]
        # back to string from list
        tweet = ' '.join(filtered_sentence) # join words with a space in between them

        cleaned_tweets.append(tweet)
        

    return cleaned_tweets
     


# In[46]:


# with open("Stress_model.pkl", 'rb') as file:  
#     model = pickle.load(file)

# model

import os
model_path = os.path.join(BASE_DIR, 'apps', 'journal', 'scripts', 'Stress_model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)



# In[47]:


nlp = en_core_web_lg.load()


# In[48]:


def predict(text):
    corpus = text_cleaner(text)
    test =np.array([np.array([token.vector for token in nlp(s)]).mean(axis=0) * np.ones((300)) \
                   for s in corpus])
    result = model.predict(test)[0]
    return result 
    
    


