# -----------------------------------------------------------------------------
# GET ALL HASHTAGS
# -----------------------------------------------------------------------------
from unidecode import unidecode
import json
import time
from modules.helpers import download_file, download_photo, download_video

def get_hashtag(api, hashtag):

    # We're going to stage them here until we process them.
    hashtagTweets = []

    # Make initial request for most recent tweets (1000 is the maximum allowed count)
    new_tweets = api.search(q='#'+hashtag, rpp=1000, result_type="recent", include_entities=True, lang="en", count=1000)

    # Save most recent tweets into our temp array
    hashtagTweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = hashtagTweets[-1].id - 1

    # Keep grabbing tweets until there are no tweets left to grab
    while len(hashtagTweets) < 2000:

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.search(q='#'+hashtag, rpp=1000, result_type="recent", include_entities=True, lang="en", count=1000, max_id=oldest)

        # save most recent tweets
        hashtagTweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = hashtagTweets[-1].id - 1

        print('   ...%s tweets downloaded so far' % (len(hashtagTweets)))

    # Uncomment to see the data available for saving
    # pp.pprint(tempTweets[160]._json)

    payload = []
    for tweet in hashtagTweets:
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
                        download_photo(hashtag, media['media_url'], to='')
                    # If it's a video
                    if media['type'] == 'video':
                        # pp.pprint(media)
                        download_video(hashtag, media['video_info'], to='')

        except:
            thisTweet['media'] = None

        payload.append(thisTweet)

    tweetsFile = open( hashtag + "/tweets.json","w+")

    # Uncomment below for a minified option
    # json.dump(payload, tweetsFile, sort_keys=True, separators=(',',':'))

    #prettified
    json.dump(payload, tweetsFile, sort_keys=True, indent=4)

    # print unicode('------------------------')
    # print unicode('WRITING HASHTAG TWEETS TO JSON FILE...')
    time.sleep(2) # Just a UX sleep
    # print unicode('Tweets are available at ' + hashtag + "/tweets.json")
