import pandas as pd
import numpy as np
import json

class TwitterData():
    def __init__(self, fp, wp, ignore=[]):
        self.fp = fp
        self.wp = wp
        self.ignore = ignore

    def load_data(self):
        data = [json.loads(line) for line in open(fp, 'r')]
        self.df  = pd.DataFrame(data)
        print (f'Initial dataset consists of {self.df.shape[0]} Tweets')
        return

    def write_data(self, fp):
        self.df.to_pickle(fp)

    def filter_bots(self):
        return

    def clean_data(self):
        """
        CLEANING FUNCTION FOR JSONL DATASET
            inputs:
                    fp - string, location of datafile
                    ignore - list[strings], columns to drop
                    purge - dictionary[strings], keys: columns to drop
                                                values: value to ignore rowwise
        """
        #DROP UNNEEDED COLUMNS
        self.df.drop(columns=self.ignore, inplace=True)

        #FILTERS
            #BOTS 
        legit_sources = list(self.df['source'].value_counts()[:5].index)
        self.df = self.df[self.df['source'].isin(legit_sources)]
            #LANGUAGE
        english_sources = self.df['lang'] == 'en'
        self.df = self.df[english_sources]
            #COUNTRY
        us_sources = self.df.place.apply(lambda d: d['country_code'] if type(d).__name__ != 'NoneType' else 'US')
        self.df = self.df[us_sources == 'US']

        #UNPACK HASHTAGS
        hashtags = self.df['entities'].apply(lambda d: d['hashtags'][0]['text'] if d['hashtags'] else None)
        self.df['hashtags'] = hashtags
        
        for col, val in self.unpack.items():
            values = self.df[col].apply(lambda d: d[val][0]['text'] if d[val] else None) #clean this up
            self.df[col] = values
            self.df.rename(columns={col:val}, inplace=True)

        #convert 
        self.df['created_at'] = pd.to_datetime(df['created_at'])
        self.df.drop(columns=['entities', 'lang', 'place'])

if __name__ == '__main__':
    fp = '../data/raw/concatenated_abridged.jsonl'
    ignore = ['contributors', 'coordinates', 'display_text_range', 
              'geo', 'id_str', 'in_reply_to_user_id_str', 'is_quote_status',
              'quoted_status_permalink', 'truncated', 'withheld_in_countries']
    clean_data(fp)