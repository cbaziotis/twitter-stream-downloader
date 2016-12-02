# twitter-stream-downloader
A very simple service for downloading twitter streaming data (just text for now). Intended for research purposes.
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
4. Paste the API keys in `settings.txt` file.

```
# twitter API keys
consumer_key=ENTER_YOUR_CONSUMER_KEY
consumer_secret=ENTER_YOUR_CONSUMER_SECRET_KEY
access_token=ENTER_YOUR_ACCESS_TOKEN
access_token_secret=ENTER_YOUR_ACCESS_TOKEN_SECRET

```

### Parameters - command-line arguments
You can decide what data you want to save, by setting the following parameters:

```
>python twsd.py -h
usage: twsd.py [-h] [--lang [LANG]] [--output [OUTPUT]] [--no-rt]
               [--only-text]

optional arguments:
  -h, --help         show this help message and exit
  --lang [LANG]      filter languages. defaults to no filtering. the lang
                     codes must be comma separated.
  --output [OUTPUT]  the name of the folder where the twitter data will be
                     saved.
  --no-rt            dont't save retweets.
  --only-text        keep only the text

```


####Languages
Select the language or languages of the tweets that you want to save, using the [corresponding language codes](https://dev.twitter.com/web/overview/languages). 
Leave empty for all languages. 
The values have to be comma separated.

For example, to save only Greek and English tweets:
```
>python twsd.py --lang=el,en
```

####Output folder
You can set the name of the output folder:
```
>python twsd.py --output=myfolder
```


####Keep Retweets or not
You can decide whether to save retweets or not. A reason to decide not to, is that a tweet may be retweeted many times and this will skew the statistics of the dataset.

The default behavior is to save the retweets. To not save them just add the `--no-rt` parameter:
```
>python twsd.py --no-rt
```

####Only Text
If what you are interested in is only the message of the tweet, 
then you have the option to save just that with the `--only-text` parameter:
```
>python twsd.py --only-text 
```
This way you save space (the biggest part of the tweet object is metadata, 
and the text itself is only a small percentage of it), and the unnecessary json parsing (saving time
during the processing of the dataset).

In this case, each row in the file contains the `tweet_id` with the `text` (tab separated). 
The `tweet_id` will be useful for deduplication, if you want to merge datasets.

---
##Execution
Run the service by executing the `twsd.py` script. The service prints some useful information about it's progress. 
Here is an example where we start downloading only the text of English tweets without keeping the retweets.
```
>python twsd.py --lang=en --no-rt  --only-text
Downloading...
Total:   104     Rate: 19.54 tweets/sec          time: 0:00:11
```