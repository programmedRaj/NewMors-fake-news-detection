from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

begin_date=dt.date(2020,4,14)
end_date=dt.date(2020,5,14)
limit=10
lang='english'

tweets=query_tweets("#news AND #India ",begindate=begin_date,enddate=end_date,limit=limit,lang=lang)

df=pd.DataFrame(t.__dict__ for t in tweets)
df.to_csv('rew.csv',index=True)
