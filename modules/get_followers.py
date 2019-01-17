# -----------------------------------------------------------------------------
# GET FOLLOWERS
# -----------------------------------------------------------------------------
def get_followers(handle):

    allFollowers = []

    # We'll convert this to json for writing
    payload = {}

    # GET TWITTER USER'S FOLLOWERS
    # http://docs.tweepy.org/en/v3.5.0/api.html#API.followers
    # Followers in order they were added, most recent at top.
    # print unicode('------------------------')
    # print unicode('GETTING FOLLOWERS...')
    tempFollowers = []
    for page in tweepy.Cursor(api.followers, screen_name=handle).pages(testingCounts):
        # print unicode('   ... getting a page of results (1 min.) ...')
        tempFollowers.extend(page)
        time.sleep(60)

    # Uncomment to see the data available for saving
    # pp.pprint(tempFollowers[0]._json)

    for follower in tempFollowers:
        thisFollower = {}
        rawJson = follower._json
        thisFollower['name'] = rawJson['name']
        thisFollower['screen_name'] = rawJson['screen_name']
        thisFollower['location'] = rawJson['location']
        thisFollower['time_zone'] = rawJson['time_zone']
        thisFollower['description'] = unicode(rawJson['description'])
        thisFollower['friends_count'] = rawJson['friends_count']
        thisFollower['followers_count'] = rawJson['followers_count']
        thisFollower['created_at'] = rawJson['created_at']
        thisFollower['profile_image_url'] = rawJson['profile_image_url']
        allFollowers.append(thisFollower)

    payload['followers'] = allFollowers

    followersFile = open( handle + "/followers.json","w+")

    # Uncomment below for a minified option
    # json.dump(payload, followersFile, sort_keys=True, separators=(',',':'))

    #prettified
    json.dump(payload, followersFile, sort_keys=True, indent=4)

    # print unicode('------------------------')
    # print unicode('WRITING FOLLOWERS TO JSON FILE...')
    time.sleep(2) # Just a UX sleep
    # print unicode('Followers are available at ' + handle + "/followers.json")


