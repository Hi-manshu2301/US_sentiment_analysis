import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import plotly.express as px 

import re 
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer 
from textblob import TextBlob 
from wordcloud import WordCloud 

import warnings 
warnings.filterwarnings('ignore') 

trump = pd.read_csv("hashtag_donaldtrump.csv", lineterminator='\n') 
print(trump.head(3)) 

print(trump.columns)
print(trump.columns)

biden = pd.read_csv("hashtag_joebiden.csv", lineterminator='\n') 
print(biden.head(2)) 

print(trump.shape) 
print(biden.shape)

trump.info() 
biden.info() 


trump['candidate'] = 'trump'

biden['candidate'] = 'biden'

data = pd.concat([trump, biden]) 

print('Final Data Shape :', data.shape) 

print("\nFirst 2 rows:") 
print(data.head(3)) 


data.dropna(inplace=True) 

data['country'].value_counts()

data['country'] = data['country'].replace({'United States of America': "US", 
										'United States': "US"}) 



tweets_count = data.groupby('candidate')['tweet'].count().reset_index() 

fig = px.bar(tweets_count, x='candidate', y='tweet', color='candidate', 
			color_discrete_map={'Trump': 'pink', 'Biden': 'blue'}, 
			labels={'candidate': 'Candidates', 'tweet': 'Number of Tweets'}, 
			title='Tweets for Candidates') 

fig.show() 

likes_comparison = data.groupby('candidate')['likes'].sum().reset_index() 
fig = px.bar(likes_comparison, x='candidate', y='likes', color='candidate', 
			color_discrete_map={'Trump': 'blue', 'Biden': 'green'}, 
			labels={'candidate': 'Candidate', 'likes': 'Total Likes'}, 
			title='Comparison of Likes') 

fig.update_layout(plot_bgcolor='black', 
				paper_bgcolor='black', font_color='white') 

fig.show() 

top10countries = data.groupby('country')['tweet'].count( 
).sort_values(ascending=False).reset_index().head(10) 

fig = px.bar(top10countries, x='country', y='tweet', 
			template='plotly_dark', 
			color_discrete_sequence=px.colors.qualitative.Dark24_r, 
			title='Top10 Countrywise tweets Counts') 

fig.show() 


tweet_df = data.groupby(['country', 'candidate'])[ 
	'tweet'].count().reset_index() 

tweeters = tweet_df[tweet_df['country'].isin(top10countries.country)] 


fig = px.bar(tweeters, x='country', y='tweet', color='candidate', 
			labels={'country': 'Country', 'tweet': 'Number of Tweets', 
					'candidate': 'Candidate'}, 
			title='Tweet Counts for Each Candidate in the Top 10 Countries', 
			template='plotly_dark', 
			barmode='group') 

fig.show() 

def clean(text): 
	text = re.sub(r'https?://\S+|www\.\S+', '', str(text)) 

	text = text.lower() 

	text = re.sub('[^a-z]', ' ', text) 

	text = text.split() 

	lm = WordNetLemmatizer() 

	text = [lm.lemmatize(word) for word in text if word not in set( 
		stopwords.words('english'))] 

	text = ' '.join(word for word in text) 

	return text 

def getpolarity(text): 
    return TextBlob(text).sentiment.polarity 
  
def getsubjectivity(text): 
    return TextBlob(text).sentiment.subjectivity 
  
def getAnalysis(score): 
    if score < 0: 
        return 'negative'
    elif score == 0: 
        return 'neutral'
    else: 
        return 'positive'
    
trump_tweets = data[data['candidate'] == 'trump'] 

trump_tweets = trump_tweets.loc[trump_tweets.country == 'US'] 
trump_tweets = trump_tweets[['tweet']] 
print(trump_tweets.head()) 

trump_tweets['cleantext'] = trump_tweets['tweet'].apply(clean) 
print(trump_tweets.head()) 

trump_tweets['subjectivity'] = trump_tweets['cleantext'].apply(getsubjectivity) 

trump_tweets['polarity'] = trump_tweets['cleantext'].apply(getpolarity) 

trump_tweets['analysis'] = trump_tweets['polarity'].apply(getAnalysis) 
trump_tweets.head() 

plt.style.use('dark_background') 

colors = ['orange', 'blue', 'red'] 

plt.figure(figsize=(7, 5)) 
(trump_tweets.analysis.value_counts(normalize=True) * 100).plot.bar(color=colors) 
plt.ylabel("%age of tweets") 
plt.title("Distribution of Sentiments towards Trump") 
plt.show() 

def word_cloud(wd_list): 
	stopwords = set(STOPWORDS) 
	all_words = ' '.join() 
	wordcloud = WordCloud(background_color='black', 
						stopwords=stopwords, 
						width=1600, height=800, max_words=100, max_font_size=200, 
						colormap="viridis").generate(all_words) 
	plt.figure(figsize=(12, 10)) 
	plt.axis('off') 
	plt.imshow(wordcloud) 

word_cloud(trump_tweets['cleantext'][:5000]) 

biden_tweets = data[data['candidate'] == 'biden'] 
biden_tweets = biden_tweets.loc[biden_tweets.country == 'US'] 
biden_tweets = biden_tweets[['tweet']] 
biden_tweets

biden_tweets['cleantext']=biden_tweets['tweet'].apply(clean) 
biden_tweets.head()

biden_tweets['subjectivity'] = biden_tweets['cleantext'].apply(getsubjectivity) 
biden_tweets['polarity'] = biden_tweets['cleantext'].apply(getpolarity) 
biden_tweets['analysis'] = biden_tweets['polarity'].apply(getAnalysis) 
biden_tweets.head() 

plt.style.use('dark_background') 

colors = ['orange', 'green', 'red'] 

plt.figure(figsize=(7, 5)) 
(biden_tweets.analysis.value_counts(normalize=True) * 100).plot.bar(color=colors) 
plt.ylabel("%age of tweets") 
plt.title("Distribution of Sentiments towards Biden") 
plt.show() 

word_cloud(biden_tweets['cleantext'][:5000])

Trump_Tweets.analysis.value_counts(normalize=True)*100

Biden_Tweets.analysis.value_counts(normalize=True)*100







