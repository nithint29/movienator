import twitter

api = twitter.Api(consumer_key='z8MkWcyiR6P9v2qBNVrMjGdjV',
                      consumer_secret='U5mkJIlKuXMsPATOGpf588hURdlvKmpuoSO8xZLhjMex2oVw93',
                      access_token_key='2420679006-qbipR9ZaTL71wr1MSLHIW0vXtaNHcmClz9QLfwy',
                      access_token_secret='lwMgy9T3KbNGpL7aFKNbynCYljsmhcpITnsCe5aHhpUh5')


results = api.GetSearch(
    raw_query="l=&q=\"Black%20Panther\"%20since%3A2018-03-12%20until%3A2018-03-13")

print(results)
print(len(results))