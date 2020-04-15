##IMPROVMENTS
# show the names of not added 
# ignore text only posts to increase the number of songs searched since im only limited to 100
# clear the playlist automatically before repopulating

import json
import spotipy
import praw
import pandas as pd
import datetime as dt
import spotipy.util as util
import re

# spotify credentials go here
 
#reddit credentials here


token = util.prompt_for_user_token(username_s,
                           'playlist-modify-public',
                           client_id=client_id_s,
                           client_secret=client_secret_s,
                           redirect_uri='http://localhost/')

#reddit credentials
reddit = praw.Reddit(client_id=client_id_r,
                     client_secret=client_secret_r,
                     user_agent=user_agent_r,
                     username=username_r,
                     password=password_r)


def metal():
    playlist_id = '5xxWTwdlXauRl1b1b9A7Tg'
    sub = 'Metal'
    return playlist_id, sub
def listentothis():
    playlist_id = '06cwQ3H6bFfEPE3IskzMay'
    sub = 'listentothis'
    return playlist_id, sub
def music():
    playlist_id = '4LVDhvhSkgyoMqrVyuFiyg'
    sub = 'Music'
    return playlist_id, sub
def vintageobscura():
    playlist_id = '7drmhPTiA96aN8WIotIdq7'
    sub = 'vintageobscura'
    return playlist_id, sub
def default():
    return 'Please select a Subreddit'

switch_case = {
    '1': metal,
    '2': listentothis,
    '3': music,
    '4': vintageobscura
    }

def switch(x):
    return switch_case.get(x, default)()

print("Which sub do you wish to scan? ")
choice = input()
playlist_id, sub = switch(choice)

subreddit = reddit.subreddit(sub)


#how the subreddit is sorted and how many posts
hot_subreddit = subreddit.hot(limit=100)
sp = spotipy.Spotify(auth=token)
inv_count = 0

for submission in hot_subreddit:
    #looks for artist - song format
    if "-" in submission.title:
        while True:
            try:
                # this separates the post tile at the '-' resulting in [artist, title]
                #separation = submission.title.split("-")
                separation = re.split('[-([]', submission.title)
                #uses the reddit title to search the spotify library
                result = sp.search("artist:"+separation[0]+" track:"+separation[1], limit=1, offset=0, type = 'track')                
                #exctract song id from JSON
                song_id=result.get('tracks').get('items')[0].get('id')
                #add song to playlist.  5xxWTwdlXauRl1b1b9A7Tg is the playlist id 
                sp.user_playlist_add_tracks(username_s, playlist_id, [song_id], position = None)
                break
            except IndexError:
                print("invalid search: " + submission.title)
                inv_count = inv_count + 1
                
                break
print(inv_count)