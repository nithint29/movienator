import twitter

api = twitter.Api(consumer_key='z8MkWcyiR6P9v2qBNVrMjGdjV',
                      consumer_secret='U5mkJIlKuXMsPATOGpf588hURdlvKmpuoSO8xZLhjMex2oVw93',
                      access_token_key='2420679006-qbipR9ZaTL71wr1MSLHIW0vXtaNHcmClz9QLfwy',
                      access_token_secret='lwMgy9T3KbNGpL7aFKNbynCYljsmhcpITnsCe5aHhpUh5')


# results = api.GetSearch(
#     raw_query="l=&q=%23Hugo%20since%3A2011-09-01%20until%3A2011-11-22")
#
# for r in results:
#     print(r)
# print(len(results))

print(api.base_url)


results = api.GetSearch(
    raw_query="query=TwitterDev%20%5C%22search%20api%5C%22&maxResults=100&fromDate=201701010000&toDate=201802010000")

for r in results:
    print(r)
print(len(results))

