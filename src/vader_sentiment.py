import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
import numpy as np
import datetime
import pickle

#nltk.download('vader_lexicon') #note: only need this if vader_lexicon has not been downloaded
plt.style.use('fivethirtyeight')

def vader_analysis():
    #load the data
    data = load_data('data/clean/twitter_data.pkl')
    
    #clean the tweets
    data['clean_text'] = clean_tweets(data['full_text'])
    
    #calculate VADER sentiment scores for each tweet
    data['pos'], data['neu'], data['neg'], data['com'] = score_data(data['clean_text'])
    
    #find candidates mentioned in each tweet
    data['biden'] = [True if 'biden' in tweet.lower() else False for tweet in data['full_text']]
    data['trump'] = [True if 'trump' in tweet.lower() else False for tweet in data['full_text']]
    
    #split tweets based on candidate mentions. Note: there will be overlap amongst tweets that mention both
    biden_tweets = data[data['biden']]
    trump_tweets = data[data['trump']]
    
    #VADER isn't perfect, and some tweets are coming back completely neutral. 
    #Getting rid of these to better hone in on raw emotion
    biden_tweets = biden_tweets[~((biden_tweets['neu'] == 1) & (biden_tweets['com'] == 0))]
    trump_tweets = trump_tweets[~((trump_tweets['neu'] == 1) & (trump_tweets['com'] == 0))]
    
    #specify intervals
    intervals = pd.date_range(start='2020-09-30', end='2020-10-03', freq='1H', tz='UTC')

    #compute VADER sentiment rolling average
    biden_avg = []
    trump_avg = []
    for i in range(len(intervals)):
        start = i - 1
        end = i + 1

        if i == 0: start = i
        if i == len(intervals) - 1: end = i

        biden_set = biden_tweets[(biden_tweets['created_at'] > intervals[start]) & 
                                 (biden_tweets['created_at'] < intervals[end])]

        trump_set = trump_tweets[(trump_tweets['created_at'] > intervals[start]) &
                                 (trump_tweets['created_at'] < intervals[end])]

        biden_avg.append(biden_set['com'].mean())
        trump_avg.append(trump_set['com'].mean())

    plot_VADER(biden_avg, trump_avg, intervals)
    
    return biden_avg, trump_avg
    
    
    
def plot_VADER(biden_avg, trump_avg, intervals):  
    '''
        Plots the avg VADER sentiment.
        
        Input:
        -biden_avg: list of average vader sentiments corresponding to 3 hr intervals
        -trump_avg: list of average vader sentiments corresponding to 3 hr intervals
        -intervals: list of hour intervals (UTC)
        
        Returns None
    '''
    
    
    #important tweet timestamps
    trump_tweet = datetime.datetime(2020, 10, 2, 4, 54)
    hicks_tweet = datetime.datetime(2020, 10, 2, 2, 44)
    hospital_tweet = datetime.datetime(2020, 10, 2, 22, 16)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(intervals, biden_avg, linewidth=2, label='biden')
    ax.plot(intervals, trump_avg, linewidth=2, label='trump')
    ax.axvline(trump_tweet, -.1, 1, linewidth=1, color='black')
    ax.axvline(hicks_tweet, -.1, 1, linewidth=1, color='black')
    ax.text(trump_tweet + datetime.timedelta(hours=2), 0.25, 'Trump Tweet', fontsize=13)
    ax.text(hicks_tweet - datetime.timedelta(hours=16), 0.15, 'Hope Hicks Tweet', fontsize=13)
    ax.set_title('VADER sentiment 3-hr average', fontsize=20)
    ax.set_ylabel('Positive Sentiment', fontsize=15)
    ax.set_xlabel('Time', fontsize=15)
    ax.legend()
    
    fig.savefig('img/VADER.png')

def score_data(data):
    '''
        Computes VADER sentiment scores for every string in the data passed in.
        
        Input:
        -data: a pandas Series object containing strings to be scored
        
        Returns:
        pos, neu, neg, com list objects containing the respective scores for each string
    '''
    sid = SentimentIntensityAnalyzer()
    
    pos = []
    neu = []
    neg = []
    com = []
    for i in range(data.shape[0]):
        score = sid.polarity_scores(data[i])
        pos.append(score['pos'])
        neu.append(score['neu'])
        neg.append(score['neg'])
        com.append(score['compound'])
    
    return pos, neu, neg, com

def load_data(fpath):
    '''
        Loads and unpickles the cleaned data
        
        Input:
        -fpath: a string representing the filepath of the data
        
        Returns:
            Returns the unpickled dataframe
    '''
    with open(fpath, 'rb') as f:
        data = pickle.load(f)
        data.reset_index(drop=True, inplace=True)
    return data
    
        
def remove_pattern(input_txt, pattern):
    '''
        Removes all instances of a patter from a string. 
        Code sourced from Amey Band 
            (https://medium.com/python-in-plain-english/twitter-sentiment-analysis-using-vader-tweepy-b2a62fba151e)
            
        Input:
        -input_txt: a string of text to be cleaned
        -pattern: the pattern to be removed from the input_txt
        
        Returns:
            A cleaned string
    '''
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def clean_tweets(tweets):
    '''
        Cleans a corpus of tweets
        Code sourced from Amey Band
            (https://medium.com/python-in-plain-english/twitter-sentiment-analysis-using-vader-tweepy-b2a62fba151e)
            
        Input:
        -tweets: a pandas Series of text data, in traditional Tweet format
        
        Returns a pandas Series of cleaned tweets
    '''
    #remove twitter Return handles (RT @xxx:)
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:") 
    
    #remove twitter handles (@xxx)
    tweets = np.vectorize(remove_pattern)(tweets, "@[\w]*")
    
    #remove URL links (httpxxx)
    tweets = np.vectorize(remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")
    
    #remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
    
    return tweets

if __name__ == "__main__":
    vader_analysis()