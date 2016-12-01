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

### Settings
You can set the settings in `settings.txt`.

####Languages
Select the language or languages of the tweets that you want to save, using the [corresponding language codes](https://dev.twitter.com/web/overview/languages). 
Leave empty for all languages. 
The values have to be comma separated.

For example, to save only Greek and English tweets:
```
languages=el,en
```
####Keep Retweets or not
You can decide whether to save retweets or not. A reason to decide not to, is that a tweet may be retweeted many times and this will skew the statistics of the dataset.

The default value is `True`:
```
rt=True
```
####Output folder
You can set the name of the output folder:
```
output_folder=dump
```
---
##Execution
Run the service by executing the `download_data.py` script. The service prints some useful information about it's progress.
```
> python download_data.py
Downloading...
Total:   150     Rate: 13.48 tweets/sec          time: 0:00:19
```