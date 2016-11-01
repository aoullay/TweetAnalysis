import tweepy
from textblob import TextBlob
import csv
import sys


consumer_key = <'your own personal Consumer Key'>
consumer_secret = <'your own personal Consumer Secret'>

access_token = <'your own personal Access Token'>
access_token_secret = <'your own personal Access Token Secret'>

#Authentification
def get_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

#api object
def get_api():
    auth=get_auth()
    api = tweepy.API(auth)
    return api



#find recent public tweets on a given topic
def recent_tweets(api,topic):
    public_tweets = api.search(q=topic)
    for tweet in public_tweets:
        t=tweet.text
        print(t.encode('cp437', 'ignore'))
        analysis = TextBlob(tweet.text)
        print(analysis.sentiment)
    return public_tweets

#polarity is a float within the range [-1.0, 1.0]
def polarity_analysis(tweets):
    polarity_list = []
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        if(analysis.sentiment.polarity == 0.0):
            polarity = "Neutral"
        elif(analysis.sentiment.polarity > 0.0):
            polarity = "Positive"
        else:
            polarity = "Negative"

        polarity_list.append(polarity)
                
    return polarity_list

#subjectivity is a float within the range [0.0, 1.0] 
def subjectivity_analysis(tweets):
    subjectivity_list = []
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        if(analysis.sentiment.subjectivity < 0.5):
            subjectivity = "Objective"
        elif(analysis.sentiment.subjectivity > 0.5):
            subjectivity = "Subjective"
        else:
            subjectivity = "Neither"

        subjectivity_list.append(subjectivity)
    return subjectivity_list


#creating a csv file that contains the tweet and its corresponding sentiments ( polarity + subjectivity ) 

def create_csv(topic,public_tweets,subjectivity_list,polarity_list):
  
    filename = topic.replace(' ','_') +'_sentiment.csv'
    with open(filename, 'w',newline='\n',encoding='utf-8') as f:
        fieldnames = ['Tweet', 'Polarity_Sentiment','Subjectivity_Sentiment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        i=0
        for tweet in public_tweets:
            writer.writerow({fieldnames[0]:tweet.text, fieldnames[1]:polarity_list[i],fieldnames[2]:subjectivity_list[i]})
            i=i+1
            

if __name__ == '__main__':
    api = get_api()

    print('Which topic you wanna analyze? ')
    topic = input()
    
    print('Hey i\'ve something for you :These are the recent tweets !! ')
    recent_tweets = recent_tweets(api,topic)
    
    print ('Performing Subjectivity analysis')
    subj = subjectivity_analysis(recent_tweets)
    print ('Performing Polarity analysis')
    polar= polarity_analysis(recent_tweets)
    
    print ('Writing the tweets to {}_sentiment_dataset.csv'.format(topic))
    create_csv(topic,recent_tweets,subj,polar)
  
