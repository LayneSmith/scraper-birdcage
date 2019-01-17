# Birdcage - Hack-A-Thon


## Introduction

A command line tool that will pull down tweets, images and video from either a defined user or a defined hashtag. Favorites, friends and followers are available but are disabled due to throttling limits and time required to pull. These tools brought to you by SLamm, BigKiller and the letter P.

## Installation and Usage
To run the Twitter-Scraper simply clone this repo. From your command line run 
```
pipenv install
python birdcage.py <@twitter_handle>
```
`<@twitter_handle>` would be something like `@LayneSmith`. *@ REQUIRED* This will create a directory and download all that user's tweets to a json file as well as their photos and movies.

You can search by hashtag by simply entering `$python scrape-twitter.py <hashtag>` *WITHOUT* the hashtag character to return up to 2,000 results. The same directory structure will be created.

## Pitfalls
• While this CLI will download tweets relatively fast, Twitter has a strict rate-limit. That means you get 15 enquiries every 15 minutes. A full dump of a users Twitter account will take hours and hours.

## Just because, here's an Instagram dumper
To run the Instagram scraper, visit the following repo, https://github.com/rarcega/instagram-scraper and follow the super-simple directions.

## Future features
- GET MEDIA : https://goo.gl/3rFafs
- GET SAVED SEARCHES
- http://docs.tweepy.org/en/v3.5.0/api.html#API.saved_searches
- Basic visualizations, like a network diagram
- Server deployment