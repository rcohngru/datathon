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

    def name_check(self, s):
        ignore_locations = [
                            'Canada', 'Australia', 'United Kingdom', 'London', 'London, England', 'England, United Kingdom', 'Ontario, Canada', 'UK', 'Toronto', 
                            'Melbourne, Victoria', 'Lagos, Nigeria', 'Paris, France', 'South Africa' , 'Sydney, New South Wales', 'Germany', 'British Columbia, Canada'
                            'Nigeria', 'India', 'France', 'Scotland, United Kingdom', 'Vancouver, British Columbia', 'Malaysia', 'Perth, Western Australia', 'Deutschland', 'Europe', 'Ottawa, Ontario',
                            'Scotland', 'Worldwide', 'Hong Kong', 'London, UK', 'earth', '日本', 'Nairobi, Kenya', 'Nova Scotia, Canada', 'Cape Town, South Africa', 'World', 'Mumbai, India',
                            'Melbourne, Australia', 'Montréal, Québec', 'Singapore', 'New Delhi, India', 'Venezuela', 'Sydney', 'Brisbane, Queensland', 'México', 'Glasgow, Scotland', 'Berlin, Germany',
                            'Netherlands', 'Norway', 'Abuja, Nigeria', 'Dublin City, Ireland', 'Melbourne', 'Home', 'Sweden', 'Indonesia', 'Johannesburg, South Africa',
                            'Lagos', 'Trinidad and Tobago', 'Mexico', 'Calgary', 'Ontario, CA', 'São Paulo, Brasil', 'Aukland, New Zealand', 'Toronto, Canada', 'Colombia', 'España', 'Québec, Canada',
                            'Jamaica', 'Kenya', 'Hyderabad, India', 'Wales', 'Birmingham, England', 'Buenos Aires, Argentina', 'Winnipeg, Manitoba', 'Italy', 'Liverpool, England', 'Tokyo', 'Brasil',
                            'Nederland', 'Bangkok', 'Bristol', 'Doha, Qatar', 'Lima, Peru', 'Copenhagen, Denmark', 'Montreal', 'Portugal', 'New Delhi', 'Spain', 'Rio de Janeiro, Brasil',
                            'Cicero', 'Belfast', 'Russia', 'Uganda', 'Pakistan', 'Amsterdam', 'Lebanon', 'Bangladesh'
                            ]
        for loc in ignore_locations:
        if s.lower() == loc.lower() or s.lower() in loc.lower() or loc.lower() in s.lower():
            return False
        return True

    def filter_country(self):
        print ('Filtering non-US tweets')

        tweet_source = self.df.place.apply(lambda d: d['country_code'] if type(d).__name__ != 'NoneType' else 'US')
        foreign_sources = (tweet_source != 'US').sum()

        tweet_loc_mask = self.df['location'].apply(lambda s: self.name_check(s))

        print (f'{foreign_sources + (self.df.shape[0] - tweet_loc_mask.sum())} tweets have been removed \n')
        self.df = self.df[(tweet_source == 'US') & (tweet_loc_mask)]
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
