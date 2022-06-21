from django.shortcuts import render
import pandas as pd
import re
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from . import forms,models



def sentiment_scores(tweets):
    temp = []
    pos = 0
    neg = 0
    neu=0
    sid_obj = SentimentIntensityAnalyzer()
    for tweet in tweets:
        sentiment_dict = sid_obj.polarity_scores(tweet) 
        if sentiment_dict['compound'] >= 0.05 :
            pos+=1
            temp.append("POSITIVE")
        elif sentiment_dict['compound'] <= - 0.05 :
            neg+=1 
            temp.append("NEGATIVE")
        else :
            neu+=1
            temp.append("NEUTRAL")
    return temp

def index(request):
    form = forms.testp()
    if request.method == "POST":
        form = forms.testp(request.POST)
        if form.is_valid():
            return result(request)
    return render(request,"base/index.html",{"form":form})
# Create your views here.
def result(request):
    form = forms.testp()
    if request.method=="POST":
        consumer_key = "ZwPDF9HTDny43gt7Z6Rpt0bIi"
        consumer_secret = "apXppw1TeY3ayfLd3kL84K8UlYihrYXcV9Uo7UtpE6rGwrhATl"
        access_key = "1380149184473534466-jqFb8pw4l8QHVxeWKP1Jr6gxzzfoeL"
        access_secret = "T1YRhZnE6d3EXWP7ZvPkavQuY0g2ONaxwjXCATx4XOmUM"
        # Twitter authentication
        form = forms.testp(request.POST)
        if form.is_valid():
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)   
            auth.set_access_token(access_key, access_secret) 
            # Creating an API object 
            api = tweepy.API(auth)
            username = str(form.cleaned_data['text'])
            username_tweets = tweepy.Cursor(api.search_tweets, q=username).items(10)
            tweet_list = [tweet.text for tweet in username_tweets]
            tw_list = pd.DataFrame(tweet_list)
            tw_list = tw_list.drop_duplicates()
            tw_list["text"] = tw_list[0]
            #Removing RT, Punctuation etc
            remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
            rt = lambda x: re.sub("(@[A-Za-z0–9]+)|(\w+:\/\/\S+)"," ",x)
            tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
            tw_list["text"] = tw_list.text.str.lower()
            #print(tweet_list)
            tweet_list = []
            for i in tw_list["text"]:
                tweet_list.append(i)
            sentiment = sentiment_scores(tweet_list)
            #print(sentiment)
            combine = []
            for i in range(len(tweet_list)):
                t=[]
                t.append(tweet_list[i])
                t.append(sentiment[i])
                combine.append(t)
            context = {"tweets":tweet_list,"predictions":sentiment,"username":username,"combine":combine}
            return render(request,"base/result.html",context)
        

    return render(request,"base/result.html")