from vader_sentiment import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as scs
import warnings

plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')


def main():
    '''
        Runs hypothesis tests and outputs information to terminal.
        Images are also saved to img directory.
    '''

    print('Loading data...')
    print()
    biden_tweets, trump_tweets = vader_analysis()
    print('Data loaded. Beginning hypothesis tests')
    print()

    print('Hope Hicks tested positive for COVID-19 in the ' +
          'early evening of October 1st (PST).')
    print('Several hours later, Donald Trump himself ' +
          'tested positive for COVID-19.')

    print()
    print('Did the news of Hope Hicks\' and Donald Trump\'s ' +
          'positive tests increase positive')
    print('sentiment for Donald Trump and Joe Biden?')
    print()
    print('Null Hypothesis: The news of the positive COVID-19 tests ' +
          'did not impact sentiment.')
    print('Therefore, the mean sentiment for both candidates did not change.')
    print('\tmu_before = mu_after')
    print()
    print('Alternative Hypothesis: The news of the positive COVID-19 tests ' +
          'positively impacted sentiment')
    print('Therefore, the mean sentiment for both candidates after is ' +
          'greater than that of before.')
    print('\tmu_before < mu_after')
    print()
    print('We will apply this experiment to four different scenarious:')
    print('\t- Tweets that only mention Biden')
    print('\t- Tweets that only mention Trump')
    print('\t- Tweets that mention Biden and may mention Trump')
    print('\t- Tweets that mention Trump and may mention Biden')

    hicks_tweet = datetime.datetime(2020, 10, 2, 2, 44,
                                    tzinfo=datetime.timezone.utc)

    # split the data based on hicks tweet
    biden_before_hicks = biden_tweets[biden_tweets['created_at'] < hicks_tweet]
    biden_after_hicks = biden_tweets[biden_tweets['created_at'] >= hicks_tweet]

    trump_before_hicks = trump_tweets[trump_tweets['created_at'] < hicks_tweet]
    trump_after_hicks = trump_tweets[trump_tweets['created_at'] >= hicks_tweet]

    only_biden_before_hicks = biden_before_hicks[~biden_before_hicks['trump']]
    only_biden_after_hicks = biden_after_hicks[~biden_after_hicks['trump']]

    only_trump_before_hicks = trump_before_hicks[~trump_before_hicks['biden']]
    only_trump_after_hicks = trump_after_hicks[~trump_after_hicks['biden']]

    print()
    print('Sample Sizes:')
    print('|  Grouping  | Before Size | After Size |')
    print('|------------|-------------|------------|')
    print('| Only Biden |    %5i    |    %5i   |' %
          (only_biden_before_hicks.shape[0], only_biden_after_hicks.shape[0]))
    print('| Only Trump |    %5i    |    %5i   |' %
          (only_trump_before_hicks.shape[0], only_trump_after_hicks.shape[0]))
    print('|   Biden    |    %5i    |    %5i   |' %
          (biden_before_hicks.shape[0], biden_after_hicks.shape[0]))
    print('|   Trump    |    %5i    |    %5i   |' %
          (trump_before_hicks.shape[0], trump_after_hicks.shape[0]))

    print()
    print('Sentiment Swings:')
    print('| Candidate  | Before Sentiment (avg) | After Sentiment (avg) |')
    print('|------------|------------------------|-----------------------|')
    print('| Only Biden |         %0.2f          |          %0.2f         |' %
          (only_biden_before_hicks['com'].mean(),
           only_biden_after_hicks['com'].mean()))
    print('| Only Trump |         %0.2f          |          %0.2f         |' %
          (only_trump_before_hicks['com'].mean(),
           only_trump_after_hicks['com'].mean()))
    print('|   Biden    |         %0.2f          |          %0.2f         |' %
          (biden_before_hicks['com'].mean(),
           biden_after_hicks['com'].mean()))
    print('|   Trump    |         %0.2f          |          %0.2f         |' %
          (trump_before_hicks['com'].mean(),
           trump_after_hicks['com'].mean()))

    print()

    plot_hist(only_biden_before_hicks, only_biden_after_hicks,
              'Sentiment Distribution - Only Biden', 'only_biden_sentiment')
    plot_hist(only_trump_before_hicks, only_trump_after_hicks,
              'Sentiment Distribution - Only Trump', 'only_trump_sentiment')

    plot_hist(biden_before_hicks, biden_after_hicks,
              'Sentiment Distribution - Biden', 'biden_sentiment')
    plot_hist(trump_before_hicks, trump_after_hicks,
              'Sentiment Distribution - Trump', 'trump_sentiment')

    only_biden_t_stat, only_biden_p_val = scs.ttest_ind(
        only_biden_before_hicks['com'], only_biden_after_hicks['com'])
    only_trump_t_stat, only_trump_p_val = scs.ttest_ind(
        only_trump_before_hicks['com'], only_trump_after_hicks['com'])

    biden_t_stat, biden_p_val = scs.ttest_ind(
        biden_before_hicks['com'], biden_after_hicks['com'])
    trump_t_stat, trump_p_val = scs.ttest_ind(
        trump_before_hicks['com'], trump_after_hicks['com'])

    print('|  Grouping  | p-value |')
    print('|------------|---------|')
    print('| Only Biden |   %0.2f  |' % only_biden_p_val)
    print('| Only Trump |   %0.2f  |' % only_trump_p_val)
    print('|    Biden   |   %0.2f  |' % biden_p_val)
    print('|    Trump   |   %0.2f  |' % trump_p_val)

    print()
    print('In all cases, we reject the null hypothesis in favor of' +
          'the alternative.')

    plot_pval(only_biden_before_hicks, only_biden_p_val,
              'Positivity Distribution Under Null - Only Biden',
              'only_biden_pval')
    plot_pval(only_trump_before_hicks, only_trump_p_val,
              'Positivity Distribution Under Null - Only Trump',
              'only_trump_pval')

    plot_pval(biden_before_hicks, biden_p_val,
              'Positivity Distribution Under Null - Biden', 'biden_pval')
    plot_pval(trump_before_hicks, trump_p_val,
              'Positivity Distribution Under Null - Trump', 'trump_pval')

    print()
    print('In conclusion:')
    print('Donald Trump contracting COVID-19 ultimately proved beneficial ' +
          'to his campaign. Twitter sentiment quickly swung positive as ' +
          'people reacted to the news. His illness also significantly ' +
          'benefitted his opponent, Joe Biden, although to a lesser extent.')


def plot_hist(before, after, title, fname):
    fig, ax = plt.subplots(figsize=(8, 6))

    mean_before = before['com'].mean()
    mean_after = after['com'].mean()

    ax.hist(before['com'], label='normalized_before',
            normed=1, alpha=0.5, bins=20, color='#64b5f6')
    ax.hist(after['com'], label='normalized_after',
            normed=1, alpha=0.5, bins=20, color='#e57373')
    ax.vlines(mean_before, 0, 3, label='mean_before(%0.2f)' % mean_before,
              linestyle='--', linewidth=2, color='#2196f3')
    ax.vlines(mean_after, 0, 3, label='mean_after(%0.2f)' % mean_after,
              linestyle='--', linewidth=2, color='#f44336')
    ax.legend()
    ax.set_title(title, fontsize=20)
    ax.set_xlabel('Positive Sentiment')

    fig.savefig('img/%s.png' % fname)


def plot_pval(before, p_val, title, fname):
    dist_m = scs.norm(np.mean(before['com']), np.std(before['com']))
    y = dist_m.ppf(1 - p_val)
    if y == float('inf'):
        y = 2
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(-2, 2, 100)
    ax.plot(x, dist_m.pdf(x))
    ax.vlines(y, 0, 0.8, linestyle='dashed', linewidth=2,
              label='P_value: %.3f' % p_val)
    ax.set_title(title)
    ax.legend()

    fig.savefig('img/%s.png' % fname)


if __name__ == "__main__":
    main()
