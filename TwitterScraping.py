import twint

c = twint.Config()
c.Search = '#fakenew'
c.Since = '2020-06-01 00:00:01'
c.Until = '2020-06-20 00:00:01'
c.Store_object = True
c.Count = True
c.Output = 'Santi_ABASCAL'
c.Filter_retweets  = True
twint.run.Search(c)
tweets = twint.output.tweets_list
nTuits = 0
for tw in tweets:
    nTuits +=1
    print(tw.tweet)
print(tweets)
print(nTuits)
