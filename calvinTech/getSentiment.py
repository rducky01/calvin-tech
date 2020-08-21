from django import forms
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class getSentimentForm(forms.Form):
    message = forms.CharField(label='Say something positive or negative.', widget=forms.Textarea())

def buildCorpus(df):
    '''
    Function builds a corpus out of a paragraph for use in computational linguistics.
    '''
    
    # Create empty lists for each step in the feature extraction.
    tokens = []
    stems = []
    lemmatized = []
    
    # Define the vectorizer function, stemmer, and lemmatizer.
    cv = CountVectorizer(stop_words = 'english', lowercase = True)
    vFn = cv.build_analyzer()
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    # Populate the tokens list with tokenized list for each row.
    for i in range(0, len(df)):
        t =vFn(df['input'][i])
        tokens.append(t)
        
    # Stem each token.
    for t in tokens:
        for i in range(0, len(t)):
            t[i] = stemmer.stem(t[i])
        stems.append(t)
        
    # Lemmatize each list in stems.
    for s in stems:
        for i in range(0, len(s)):
            s[i] = lemmatizer.lemmatize(s[i])
        lemmatized.append(s)
        
    # Form lemmas into corpus.
    corpus = [' '.join(l) for l in lemmatized]
    
    return corpus

def getSentiment(df):
    '''
    Function assigns sentiment to each sentence in the corpus and adds them as a new row on the dataframe.
    '''
    
    # Generate corpus of review_text
    corpus = buildCorpus(df)
    
    # Build sentiment analyzer.
    analyzer = SentimentIntensityAnalyzer()
    sentiment = [analyzer.polarity_scores(i) for i in corpus]
    
    # build new dataframe around detected sentiment.
    df1 = pd.DataFrame(sentiment)
    df1['input'] = corpus
    
    # Label the rows using the compound sentiment score.
    sents = []
    
    for i in range(len(df1)):

        if df1['compound'][i] > 0.5:
            
            x = 'very positive'
        
        if df1['compound'][i] > 0.05:
            
            x = 'positive'
            
        elif df1['compound'][i] < -0.05:
            
            x = 'negative'

        elif df1['compound'][i] < -0.5:
            
            x = 'very negative'
            
        else:
            
            x = 'neutral'
            
        sents.append(x)
        
    df1['sentiment'] = pd.Series(sents)
    
    return df1