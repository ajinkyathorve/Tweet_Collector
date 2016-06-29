# -*- coding: utf-8 -*-


import tweepy
import json
from datetime import datetime
import pytz


#Insert your OAuth details from Twitter in the four empty fields below
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


#Creating an OAuth instance and setting the required credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


list_tweets = [] #Creating an empty list that will be used to store all the collected information. Information from each individual tweet will be stored in a dictionary, and such dictionaries will be stored in this list


numb_tweets = 0 #Counter for the number of tweets collected


max_iter = 10 #Maximum number of iterations to be performed, each iteration collects approximately the number of tweets denoted by the count parameter while searching, in this application it is set to 100


for itr in range(max_iter): #Iterate max_iter times to collect the desired number of tweets
    if itr == 0:
        search_results = api.search(q="USA OR NY OR Buffalo OR Niagara", count=100, lang="en") #Searching for the first time, no need to include the max_id parameter
    else:
        least_id_from_last_tweet = search_results['statuses'][-1]['id'] #Obtaining the lowest id of the tweet from the previous search
        search_results = api.search(q="USA OR Buffalo OR Niagara", count=100, max_id=least_id_from_last_tweet, lang="en") #For all subsequent searches, the max_id parameter is set to the lowest id of the tweet from the previous search. This is done to avoid getting duplicate results
    for status in search_results['statuses']: #Iterate over all the collected tweets
        dict_tweet = {'text' : '', 'tweet_urls' : '', 'tweet_hashtags' : '', 'created_at' : '', 'lang' : '', 'id' : ''}  #Creating a dictionary that will store the different fields from a tweet
        dict_tweet['text'] = status['text'].encode('utf-8')
        if status['entities']['urls']:
            dict_tweet['tweet_urls'] = status['entities']['urls'][0]['expanded_url']
        if status['entities']['hashtags']:
            dict_tweet['tweet_hashtags'] = status['entities']['hashtags'][0]['text']
        datetime_temp = status['created_at']
        fmt = '%Y-%m-%dT%H:%M:%SZ'
        temp = datetime.strptime(datetime_temp,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        dict_tweet['created_at'] = temp.strftime(fmt)
        dict_tweet['lang'] = status['lang']
        dict_tweet['id'] = status['id']
        list_tweets.append(dict_tweet) #Append the dictionary containing the tweet to the list
        numb_tweets += 1 #Increment counter by 1


print "Total number of tweets collected: %d" %numb_tweets


with open("tweets_json.txt", "w") as json_en: #The output will be in a json format and saved in .txt file
	json.dump(list_tweets, json_en, ensure_ascii=False, encoding="utf-8")
