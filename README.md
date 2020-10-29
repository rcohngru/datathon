# Datathon: WEST COAST III
## Sentiment Analysis of Twitter Data
Early this year, British and Brazilian presidents saw increases in approval ratings after being diagnosed with Covid-19. Source https://www.pri.org/stories/2020-10-02/trump-positive-what-catching-covid-19-meant-boris-johnson-jair-bolsonaro. There were rumbling on the left that, after Trump announced he had contracted the virus following the first presidential debate, the US President was strategically manipulating American sentiment to avoid criticism from his bad debate performance. We set out to see if there was any merit to this claim and if this would have any outcome on the election. 

"Our results suggest that Twitter is becoming a more reliable platform to gather the true sentiment of a certain topic. Comparing sentiment of tweets to reliable polling data shows a correlation as high as 84% using a moving average smoothing technique.":
https://medium.com/shiyan-boxer/2020-us-presidential-election-twitter-sentiment-analysis-and-visualization-89e58a652af5

## The 2020 Presidential Election Twitter Dataset, September 30 2020 - October 2 2020
    link:

The full dataset consists of 140,337 tweets & metadata from 121,040 unique users. Twitter data is infamously messy, however for the purposes of this study, the issue is not as dramatic. We obtained a JSONL file consisting of 32 keys with only several columns providing use. 
<p align="center">
<img src="https://raw.githubusercontent.com/rcohngru/datathon/main/img/data_synopsis.png" width='300'>
</p>
Since we wanted to make this a distinctly American study, we had to be as confident as possible in our dataset's sources. Our full cleaning process can be read in the src/load_clean_data.py file. 

The `lang` column was the easiest to start with, of which 16,082 non-English tweets were dropped. 

The `source` column also showed potential problems. The bulk of the tweets came from The iPhone or Android Twitter apps, however many values looked like potential bots coming from 3rd party apps, so we dropped 1,456 tweets generated outside of the 5 most common sources officially integrated by Twitter.

The `user` column - a nested dictionary containing a `location` value - proved the trickiest to identify non-American tweets as Twitter does not enforce any standardization of profile info, leading joke values such as `Planet Earth` or multiple values for the same foreign city, (i.e. `London`, `London, England`, `London, UK`). We dropped 56,508 tweets based on this column.

Our final dataset consists of 66,337 tweets, evenly distributed across each of the 3 days following the first Presidential Debate on September 29th. <br>
<p align="center">
<img src="https://raw.githubusercontent.com/rcohngru/datathon/main/img/tweetsperday.png" width='600'><br><br>

## Initial Observations
There is a strong presidential race theme in this dataset, with over half the tweets directly mentioning Trump while ~1/3rd mention Biden. This did not surprise us as Trump is more active on Twitter.<br><br>
<p align="center">
<img src="https://raw.githubusercontent.com/rcohngru/datathon/main/img/candidateengagement.png" width='600'><br><br>

Something that sparked our interest was how quickly the 'Twittershpere' latched onto and then moved on from mentioning 'debate'. The early morning of the 30th (essentially late evening of the 29th) had around 300 tweets per hour mentioning the debate and stayed above 100 per hour the entire day, before dropping to 50 per and then close to 0 on the following. <br><br>
<p align="center">
<img src="https://raw.githubusercontent.com/rcohngru/datathon/main/img/debatementionsperhour.png" width='600'><br><br>





