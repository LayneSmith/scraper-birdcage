# -----------------------------------------------------------------------------
# GET FRIENDS (Accounts user is following)
# -----------------------------------------------------------------------------
def get_friends(handle):

    allFriends = []

    # We'll convert this to json for writing
    payload = {}

    # GET WHO THEY'RE FOLLOWING, TWITTER CALLS THEM FRIENDS
    # Friends order they were added, most recent at top.
    # print unicode('------------------------')
    # print unicode('GETTING FOLLOWING/FRIENDS...')

    tempFriends = []
    # Build array to hold raw faves
    for page in tweepy.Cursor(api.friends, screen_name=handle).pages(testingCounts):
        # print unicode('   ...')
        tempFriends.extend(page)
        time.sleep(60)

    # Uncomment to see the data available for saving
    # pp.pprint(tempFriends[0]._json)

    for friend in tempFriends:
        thisFriend = {}
        rawJson = friend._json
        thisFriend['name'] = rawJson['name']
        thisFriend['screen_name'] = rawJson['screen_name']
        thisFriend['location'] = rawJson['location']
        thisFriend['time_zone'] = rawJson['time_zone']
        thisFriend['description'] = unicode(rawJson['description'])
        thisFriend['friends_count'] = rawJson['friends_count']
        thisFriend['followers_count'] = rawJson['followers_count']
        thisFriend['created_at'] = rawJson['created_at']
        thisFriend['profile_image_url'] = rawJson['profile_image_url']
        allFriends.append(thisFriend)

    payload['friends'] = allFriends

    friendsFile = open( handle + "/friends.json","w+")

    # Uncomment below for a minified option
    # json.dump(payload, followersFile, sort_keys=True, separators=(',',':'))

    #prettified
    json.dump(payload, friendsFile, sort_keys=True, indent=4)

    # print unicode('------------------------')
    # print unicode('WRITING FRIENDS TO JSON FILE...')
    time.sleep(2) # Just a UX sleep
    # print unicode('Friends are available at ' + handle + "/friends.json")
