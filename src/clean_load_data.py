import pandas as pd
import numpy as np
import json
import os

class TwitterData():
    def __init__(self, fp, wp, ignore=[]):
        self.fp = fp
        self.wp = wp
        self.ignore = ignore

    def load_data(self):
        data = [json.loads(line) for line in open(fp, 'r')]
        self.df  = pd.DataFrame(data)
        print (f'Initial dataset consists of {self.df.shape[0]} Tweets \n')
        return

    def write_data(self):
        print (f'Final dataset consists of {self.df.shape[0]} Tweets \n')
        self.df.to_pickle(self.wp)
        return

    def filter_bots(self):
        #Narrows the dataset down to credible platforms
        print ('Filtering likely Twitter bots')

        legit_sources = ['Twitter for iPhone', 'Twitter for Android', 
                         'Twitter Web App', 'Twitter for iPad', 'TweetDeck']

        all_sources = self.df['source'].apply(lambda s: s.split('>')[1].replace('</a', '') if s else 'None')

        legit_tweets = self.df[all_sources.isin(legit_sources)].shape[0]
        sketchy_tweets = self.df.shape[0] - legit_tweets
        
        self.df = self.df[all_sources.isin(legit_sources)]
        print (f'{sketchy_tweets} unusable tweets have been removed \n')
        return

    def filter_language(self):
        print ('Filtering non-English tweets')

        english_sources = self.df['lang'] == 'en'
        non_english = (self.df['lang'] != 'en').sum()

        print (f'{non_english} tweets have been removed \n')
        self.df = self.df[english_sources]
        return

    def filter_country(self):
        print ('Filtering non-US tweets')

        tweet_source = self.df.place.apply(lambda d: d['country_code'] if type(d).__name__ != 'NoneType' else 'US')
        foreign_sources = (tweet_source != 'US').sum()

        print (f'{foreign_sources} tweets have been removed \n')
        self.df = self.df[tweet_source == 'US']
        return

    def clean_data(self):
        """
        CLEANING FUNCTION FOR JSONL DATASET
        """
        #DROP UNNEEDED COLUMNS
        self.df.drop(columns=self.ignore, inplace=True)

        #UNPACK HASHTAGS
        hashtags = self.df['entities'].apply(lambda d: d['hashtags'][0]['text'] if d['hashtags'] else None)
        self.df['hashtags'] = hashtags
        
        #UNPACK USER INFO
        categories = ['location', 'screen_name', 'name', 'description', 'created_at', 'followers_count', 'friends_count', 'verified']
        print (f'Unpacking user data for parameters:\n{", ".join(categories)}')
        for category in categories:
            values = self.df['user'].apply(lambda d: d[category])
            if category == 'created_at':
                values = pd.to_datetime(values)
                category = 'acct_created_date'
            self.df[category] = values

        #CONVERT TWEET TIMESTAMPS
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])

        #FILTERS
            #BOTS 
        self.filter_bots()
            #LANGUAGE
        self.filter_language()
            #COUNTRY
        self.filter_country()
        #DROP COLUMNS NO LONGER NEEDED
        self.df.drop(columns=['entities', 'lang', 'place', 'user'], inplace=True)
        return

if __name__ == '__main__':
    fp = 'data/raw/concatenated_abridged.jsonl'

    wp = 'data/clean/twitter_data.pkl'
    try:
        os.mkdir('data/clean/')
    except:
        pass

    ignore = ['contributors', 'coordinates', 'display_text_range', 
              'geo', 'id_str', 'in_reply_to_user_id_str', 'is_quote_status',
              'quoted_status_permalink', 'truncated', 'withheld_in_countries']

    data = TwitterData(fp, wp, ignore)
    data.load_data()
    data.clean_data()
    data.write_data()
