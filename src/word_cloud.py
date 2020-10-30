from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def wordcloud_generator(corpus, stopwords=[]):
    #combine specific cloud words 
    exclude_always = ['https', 'RT', 'co', 'tonight', 'flotus', 'amp']
    stopwords.extend(exclude_always)
    stopwords.extend(STOPWORDS)
    stopwords = set(stopwords)

    comment_words = ''
    for val in corpus:
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
                
        comment_words += " ".join(tokens) + " "
    wordcloud = WordCloud(width = 800, height = 800, 
                          background_color ='white', 
                          stopwords = stopwords, 
                          min_font_size = 10).generate(comment_words) 
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 