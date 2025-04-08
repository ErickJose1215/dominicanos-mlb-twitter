# tweet_poster.py

import tweepy
import os

def publicar_en_twitter(imagen_path):
    api_key = os.environ['TWITTER_API_KEY']
    api_secret = os.environ['TWITTER_API_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_secret = os.environ['TWITTER_ACCESS_SECRET']

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)

    tweet = "🇩🇴 BATEADORES DOMINICANOS EN MLB\n#MLB #Dominicanos"
    api.update_status_with_media(status=tweet, filename=imagen_path)
