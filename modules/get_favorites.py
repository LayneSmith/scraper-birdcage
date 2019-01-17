# -----------------------------------------------------------------------------
# GET FAVORITED TWEETS
# -----------------------------------------------------------------------------
def get_favorites(handle):

    allFaves = []

    # We'll convert this to json for writing
    payload = {}

    # GET TWITTER USER'S FAVORITED TWEETS
    # http://docs.tweepy.org/en/v3.5.0/api.html#API.favorites
    # Favorited tweets in order they were added, most recent at top.
    # print unicode('------------------------')
    # print unicode('GETTING FAVORITES...')

    tempFaves = []
    # Build array to hold raw faves
    for page in tweepy.Cursor(api.favorites, screen_name=handle).pages(testingCounts):
        # print unicode('   ... getting a page of results (1 min.) ...')
        tempFaves.extend(page)
        time.sleep(60)

    # Uncomment to see the data available for saving
    # pp.pprint(tempFaves[0]._json)
#
    for fave in tempFaves:
        thisFave = {}
        rawJson = fave._json
        thisFave['text'] = unicode(rawJson['text'])
        thisFave['name'] = rawJson['user']['name']
        thisFave['id_str'] = rawJson['id_str']
        thisFave['screen_name'] = rawJson['user']['screen_name']
        thisFave['location'] = rawJson['user']['location']
        thisFave['time_zone'] = rawJson['user']['time_zone']
        thisFave['description'] = unicode(rawJson['user']['description'])
        thisFave['friends_count'] = rawJson['user']['friends_count']
        thisFave['followers_count'] = rawJson['user']['followers_count']
        thisFave['created_at'] = rawJson['created_at']
        thisFave['profile_image_url'] = rawJson['user']['profile_image_url']
        allFaves.append(thisFave)

    payload['favorites'] = allFaves

    favoritesFile = open( handle + "/favorites.json","w+")

    # Uncomment below for a minified option
    # json.dump(payload, followersFile, sort_keys=True, separators=(',',':'))

    #prettified
    json.dump(payload, favoritesFile, sort_keys=True, indent=4)

    # print unicode('------------------------')
    # print unicode('WRITING FAVORITES TO JSON FILE...')
    time.sleep(2) # Just a UX sleep
    # print unicode('Favorites are available at ' + handle + "/favorites.json")