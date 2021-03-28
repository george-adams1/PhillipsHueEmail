'''
Script which turns Phillips Hue lights on and off
if @elonmusk tweets!
You need to create a Twitter Developer account to pass the authentication!
'''

from phue import Bridge
import time
from variables import BRIDGE_IP, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import tweepy

def accessing_lights():
    global b
    b = Bridge(BRIDGE_IP)
    light_names = b.get_light_objects('name')
    return light_names

# Function that will turn lights on and off
def twitter_lights():
    lights = accessing_lights() # Accesing Hue Bridge

    for light in lights:
        if b.get_light(light, 'on') == True:
            lights_on = True # If light ON
            for light in lights:
                lights[light].on = False

            time.sleep(5) # Change value depending on how long you want light to be off

            for light in lights:
                lights[light].on = True
                lights[light].hue = 15000
                lights[light].saturation = 100

        elif b.get_light(light, 'on') == False: # If light OFF
            lights_on = False
            for light in lights:
                lights[light].on = True
                lights[light].hue = 15000
                lights[light].saturation = 100

            time.sleep(5) # Change value depending on how long you want light to be on

            for light in lights:
                lights[light].on = False

    if lights_on == True:
        api.update_status(status="@ElonMusk I'm a bot and you just turned my creators lights off :( Contact me!")

    if lights_on == False:
        api.update_status(status="@ElonMusk you just turned my lights on :) Contact me!")

# Authenticating Tweepy
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

first = True

while True:
    if first == True:
        tweet = api.user_timeline(user_id='44196397', count=1, exclude_replies=True, include_rts=False)
        first = False
        continue

    previous_tweet = tweet
    time.sleep(5) # Change frequency of when code checks Twitter for updates

    # Loading in latest Tweets from @ElonMusk twitter page
    tweet = api.user_timeline(user_id='44196397', count=1, exclude_replies=True, include_rts=False) # Elon Musk user_id, could also use screen_name = 'elonmusk'

    if previous_tweet == tweet:
        print('Same Tweet!')
        continue

    elif previous_tweet != tweet:
        print('Not the same Tweet!')
        twitter_lights()
        continue
