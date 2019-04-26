import tweepy
import pickle
import numpy as np
from ml.vars import FAKE_ACCOUNT_MODEL_PATH

consumer_key = "YrlvTaYmfUFw6C3OnapAKiuaM"
consumer_secret = "QUZXmYYyyugyuT3GMNoOOxtTAst9fbWziGhcNsejDdsDU5tIbL"
access_token = "795922562546970624-6S2XzPe9K2gNrHphl3OUS1tjIgIh8rQ"
access_token_secret = "bfDz7r938dbfdfJai974vcQBeENz32VD8C4eBGZ71OECy"

class FakeAccountDetectionModel():
    
    def __init__(self):
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      self.api = tweepy.API(auth)
      self._useful_columns = ["statuses_count", "followers_count", "friends_count",
        "favourites_count", "listed_count", "default_profile", "profile_banner_url",
        "profile_background_tile", "profile_background_color" ,"verified"]
      self._model_path = FAKE_ACCOUNT_MODEL_PATH
      self._load_model()
        
    def _load_model(self):
        model = pickle.load(open(self._model_path, "rb"))
        self._classifier = model["classifier"]
        self._scaler = model["scaler"]
    
    def predict(self, user_name, max_tweets=5):
      user_account = self.api.lookup_users(screen_names=[user_name])[0]
      tweets = user_account.timeline()
      outputs = []
      for i, tweet in enumerate(tweets):
        outputs.append({})
        outputs[i]['tweet'] = tweet.text 
        if i==max_tweets:
          break
        retweets = self.api.retweets(tweet.id, count=1000)
        retweets = sorted(retweets, key=lambda t: t.created_at)
        retweeter_details = [retweeter.user for retweeter in retweets]
        fake_news_prob, fake_users = self.predictTweet(retweeter_details)
        outputs[i]['fake_news_prob'] = str(fake_news_prob)
        outputs[i]['retweeters'] = fake_users
        outputs[i]['time'] = [str(t.created_at) for t in retweets]
      return outputs

    def predictTweet(self, users_details):
      fake_news_prob = 1
      fake_users = []
      for user in users_details:
        details = {
          "name": user.screen_name,
          "description": user.description,
          "following": user.friends_count,
          "followers": user.followers_count
          }
        user = self._parse_details_v2(user)
        user = self._scaler.transform(user)
        probabilities = self._classifier.predict_proba(user)
        fake_news_prob *= probabilities[0][0]
        if np.argmax(probabilities[0]) == 0:
            details['isFake'] = 1
        else:
            details['isFake'] = 0
        fake_users.append(details)
      return fake_news_prob ** (1/len(users_details)), fake_users
   
    def _parse_details_v2(self, user_details):
        """ Parses user details for prediction """
        data = []
        for col in self._useful_columns:
            try:
                val = getattr(user_details, col)
                if isinstance(val, int):
                    data.append(val)
                elif isinstance(val, bool):
                    if val is True:
                        data.append(1)
                    else:
                        data.append(0)
                elif isinstance(val, str):
                    if col == 'profile_banner_url':
                        if val:
                            data.append(1)
                        else:
                            data.append(0)
                    elif col == 'profile_background_color':
                        if val != 'C0DEED':
                            data.append(1)
                        else:
                            data.append(0)
            except:
                data.append(0)
        return np.array(data).reshape(1, -1)
