# twitter-stream-downloader
A very simple service for downloading twitter streaming data.
The service also takes advantage of the recent changes in Twitter API, by also saving tweets longer than 140 chars (`"tweet_mode" = "extended"`).
### install requirements

```
pip install -r /path/to/requirements.txt
```

---
### Get Twitter API keys
The service needs to have access to Twitter’s APIs and in order to do so, it needs the necessary API keys.

1. Create a Twitter user account if you do not already have one.
2. Go to <https://apps.twitter.com/> and log in with your Twitter user account, and create a new App.
3. Then in your App's page, click on “Keys and Access Tokens” tab, and copy your “API key” and “API secret”. 
Scroll down and click “Create my access token”, and copy your “Access token” and “Access token secret”.
4. Create a file `twsd/settings.txt` and save the API keys in it, with the following format:

```
# twitter API keys
consumer_key=ENTER_YOUR_CONSUMER_KEY
consumer_secret=ENTER_YOUR_CONSUMER_SECRET_KEY
access_token=ENTER_YOUR_ACCESS_TOKEN
access_token_secret=ENTER_YOUR_ACCESS_TOKEN_SECRET
```

### Parameters - command-line arguments
You can decide what data you want to save, by setting the following parameters:

```shell
$ python twsd/main.py -h
usage: main.py [-h] [--lang [LANG]] [--storage [{text,db}]] [--omit-rt]
               [--only-text]

twitter stream downloader

optional arguments:
  -h, --help            show this help message and exit
  --lang [LANG]         filter languages. defaults to no filtering. the lang codes must be comma separated.
  --storage [{text,db}]
                        the type of storage.
                        - Set to "text" for saving the tweets in text files.
                        - Set to "db" for saving the tweets in a MongoDB database.
  --omit-rt             omit retweets
  --only-text           keep only the text. 

```
#### Storage
You have two options for saving the twitter data, (1) on disk in text files, or (2) in a database (MongoDB).
```
$ python twsd/main.py --storage db
```

#### Languages
Select the language or languages of the tweets that you want to save, using the [corresponding language codes](https://dev.twitter.com/web/overview/languages). 
Leave empty for all languages. 
The values have to be comma separated.

For example, to save only Greek and English tweets:
```
$ python twsd/main.py --lang=el,en
```


#### Omit Retweets
You can decide whether to save retweets or not. A reason to decide not to, is that a tweet may be retweeted many times and this will skew the statistics of the dataset.

The default behavior is to save the retweets. To not save them just add the `--omit-rt` parameter:
```
$ python twsd/main.py --omit-rt
```

#### Only Text
If what you are interested in is only the message of the tweet, then you have the option to save just that with the `--only-text` parameter:
```
$ python twsd/main.py --only-text 
```
This way you save space (the biggest part of the tweet object is metadata, and the text itself is only a small percentage of it), and the unnecessary json parsing (saving time during the processing of the dataset). Each row in the file contains the `tweet_id` with the `text` (tab separated). The `tweet_id` will be useful for deduplication, if you want to merge datasets.

---
## Execution
Run the service by executing the `twsd/main.py` script. The service prints some useful information about it's progress. 
Here is an example where we start downloading only the text of English tweets without keeping the retweets.
```
$ python twsd/main.py --lang=en --omit-rt  --only-text
Downloading...
Total:   104     Rate: 19.54 tweets/sec          time: 0:00:11
```
