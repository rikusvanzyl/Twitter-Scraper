#!/usr/bin/env python

import sys
import string
import simplejson
from twython import Twython
import csv
from datetime import datetime
#Twyton module is used to access Twitter API

def getAuthTokens():

    #OAUTH authentication used to access twitter API
    tks = Twython(app_key='knYo88HSLV3GuB53jk8w4vLgT',
            app_secret='IF3NbjdVJlF2a4LAAQh0IGtdhRnnsQ0MpBjc8HcARi27oXqP4L',
            oauth_token='1942383350-OyqSwzWn5ovcHXpHvdbKOjpuzuKqqlbz6EldDCX',
            oauth_token_secret='afjDqJGtYXy0cAXrVHBimMHaB6wsDvOJwbRNJfy87uPyP')
    return tks

def getUserIDs():

    #list of twitter user IDs
    ids = "14677919, 2467791, 14511951, 44196397, 39566272,  14226882,  14235041, 14292458, 14335586, 14730894,\
    15029174, 15474846, 15634728, 15689319, 15782399, 15946841, 16116519, 16148677, 16223542,\
    16315120, 16566133, 16686673, 16801671, 41900627, 42645839, 42731742, 44157002, 44988185,\
    48073289, 48827616, 49702654, 50310311, 50361094,"
    return ids

def getTwitterData(entry):

        #assign JSON value of field to variable
        id = entry['id']
        screen_name = entry['screen_name']
        name = entry['name']
        created_at = entry['created_at']
        url= entry['url']
        followers_count = entry['followers_count']
        friends_count = entry['friends_count']
        statuses_count = entry['statuses_count']
        favourites_count = entry['favourites_count']
        listed_count = entry['listed_count']
        description = entry['description']
        location = entry['location']
        time_zome = entry['time_zone']
        lang = entry['lang']
        return (id,screen_name,name,created_at,url,followers_count,friends_count,statuses_count,favourites_count,listed_count,description,location,time_zome,lang)

def scrapeTwitterPages():

    now = datetime.now()
    day=int(now.day)
    month=int(now.month)
    year=int(now.year)

    timestamp = "{:%m_%d (%H_%M_%S)}".format(datetime.now())
    #timestamp = "{:%m-%d-%Y_%H:%M:%S}".format(datetime.now())

    tokens = getAuthTokens()
    ids = getUserIDs()

    #name for header row in output file
    fields = "id screen_name name created_at url followers_count friends_count statuses_count \
    favourites_count listed_count \
    description location time_zone lang ".split()
    #fields = "id", "screen_name", "name", "created_at", "url","followers_count", "friends_count", "statuses_count", "favourites_count", "listed_count", "contributors_enabled", "protected", "location", "lang", "expanded_url"

    #access the lookup user method of the Twitter API - limit to 100 IDS with each API call.
    #user variable is a JSON file with data on the twitter user listed above.
    users = tokens.lookup_user(user_id = ids)

    #name of output file
    #outfn = "twitter_user_data_%i_%i_%i.csv" % (now.month, now.day, now.year)
    outfile = "twitterData_%s.csv" % (timestamp)

    #initialize output file and write header row
    w = csv.writer(open(outfile,"w"))
    w.writerow(fields)
    #w.writerow(["id", "screen_name", "name", "created_at", "url","followers_count", "friends_count", "statuses_count", "favourites_count", "listed_count", "contributors_enabled", "protected", "location", "lang", "expanded_url"])

    #user varible contains information of the twitter user
    for entry in users:
        r = {}
        for f in fields:
            r[f] = ""
        #not every id withh have a 'url' key, so check for tis existence
        if 'url' in entry['entities']:
            r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
        else:
            r['expanded_url'] = ''
        #print(r)
        #create empty list
        lst = []
        #add data for each variable
        for f in fields:
            lst.append(str(r[f]).replace("\/", "/"))
        #write row with data in list
        w.writerow(getTwitterData(entry))

if __name__ == '__main__':
    scrapeTwitterPages()