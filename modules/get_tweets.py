# -----------------------------------------------------------------------------
# GET ALL TWEETS
# -----------------------------------------------------------------------------
from unidecode import unidecode
import json
import time
from modules.helpers import download_file, download_photo, download_video

def get_tweets(handle, api):

    print('-----------------------')
    print('ACCOUNT INFO')

    # We'll convert this to json for writing
    payload = {}

    # GET TWITTER USER'S ATTRIBUTES
    user = api.get_user(handle)

    payload['name'] = user.name
    print('   Name: '+payload['name'])

    payload['screen_name'] = user.screen_name
    print('   Screen name: '+payload['screen_name'])

    payload['id'] = user.id
    print('   Twitter ID: '+str(payload['id']))

    payload['created_at'] = user.created_at.isoformat()
    print('   Created at: '+str(payload['created_at']))

    try:
        payload['description'] = user.description
        print('   Description: '+payload['description'])
    except:
        payload['description'] = 'None'

    try:
        payload['location'] = user.location
        print('   Location: '+payload['location'])
    except:
        payload['location'] = 'None'

    payload['friends_count'] = user.friends_count
    print('   Following: '+str(payload['friends_count']))

    payload['favorites_count'] = user.favourites_count
    print('   Favorites: '+str(payload['favorites_count']))

    payload['followers_count'] = user.followers_count
    print('   Followers: '+str(payload['followers_count']))

    payload['profile_image'] = user.profile_image_url_https
    print('   Profile image: '+payload['profile_image'])

    try:
        payload['url'] = user.url
        print('   URL: '+payload['url'])
    except:
        payload['url'] = 'None'

    durationMinutes = user.friends_count + user.followers_count + user.favourites_count / 20
    durationHours = durationMinutes/60
    durationMinutes = durationMinutes%60
    print('------------------------')
    print('NOTE: It would take approximately ' + str(round(durationHours, 1)) + ' hours to do a complete pull. ')

    # Lists we'll fill up
    allTweets = []

    print('------------------------')
    print('GETTING TWEETS...')

    # We're going to stage them here until we process them.
    tempTweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = handle,count=200)

    # Save most recent tweets into our temp array
    tempTweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = tempTweets[-1].id - 1

    # All retweets
    retweets = api.retweets_of_me(count=1)

    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = handle,count=200,max_id=oldest)

        # save most recent tweets
        tempTweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = tempTweets[-1].id - 1

        # print unicode('   ...%s tweets downloaded so far' % (len(tempTweets)))

    # Uncomment to see the data available for saving
    # pp.pprint(tempTweets[160]._json)

    for tweet in tempTweets:
        thisTweet = {}
        rawJson = tweet._json
        thisTweet['created_at'] = rawJson['created_at']
        thisTweet['hashtags'] = rawJson['entities']['hashtags']
        thisTweet['id_str'] = rawJson['id_str']
        thisTweet['mentions'] = rawJson['entities']['user_mentions']
        thisTweet['place'] = rawJson['place']
        thisTweet['retweeted'] = rawJson['retweeted']
        thisTweet['symbols'] = rawJson['entities']['symbols']
        thisTweet['text'] = unidecode(rawJson['text'])
        thisTweet['urls'] = rawJson['entities']['urls']
        try:
            # If it's original content, not a retweet
            if not thisTweet['retweeted']:
                # Assign raw data to json
                thisTweet['media'] = rawJson['extended_entities']['media']
                # Loop through every media element present
                for media in rawJson['extended_entities']['media']:
                    # If it's a photo
                    if media['type'] == 'photo':
                        download_photo(handle, media['media_url'], to='')
                    # If it's a video
                    if media['type'] == 'video':
                        # pp.pprint(media)
                        download_video(handle, media['video_info'], to='')

        except:
            thisTweet['media'] = None

        allTweets.append(thisTweet)

    payload['tweets'] = allTweets

    tweetsFile = open( handle + "/tweets.json","w+")

    # Uncomment below for a minified option
    # json.dump(payload, tweetsFile, sort_keys=True, separators=(',',':'))

    #prettified
    json.dump(payload, tweetsFile, sort_keys=True, indent=4)

    print('------------------------')
    print('WRITING TWEETS TO JSON FILE...')
    time.sleep(2) # Just a UX sleep
    print('Tweets are available at ' + handle + "/tweets.json")

