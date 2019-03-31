#! /usr/bin/python3
'''
startSourceRankPercentile and endSourceRankPercentile: The parameters can be used to filter the returned articles to include only those that are from news sources that are of a certain ranking. Sources are ranked according to the global Alexa site ranking. By setting startSourceRankPercentile to 0 and endSourceRankPercentile to 20 would, for example, return only articles from top ranked news sources that would amount to about approximately 20% of all matching content. Note: 20 percentiles do not represent 20% of all top sources. The value is used to identify the subset of news sources that generate approximately 20% of our collected news content.
'''

from eventregistry import *
from build_database import *
from process_text import *
import json

# upload input text from file/GUI/command line
phrases = find_phrases()

'''
# get articles from event-registry with processed text from list of credible sources URIs
API_KEY = "c40d087b-97be-4617-9008-19d209368072"
er = EventRegistry(apiKey = API_KEY)

# print("Reminaing available requests: ", er.getRemainingAvailableRequests())
# print("Daily available requests: ", er.getDailyAvailableRequests())

it = QueryArticlesIter(
        keywords = QueryItems.OR(phrases),
        dataType = ["news", "pr", "blog"],
        keywordsLoc = "body,title",
        sourceUri = QueryItems.OR(source_uri),
        lang="eng",
        dateStart = datetime(2019, 1, 1)
    )

res = it.execQuery(er, 
                    sortBy = "rel", # sourceAlexaGlobalRank, socialScore, sourceImportance
                    maxItems = 10,
                    returnInfo = ReturnInfo(
                        articleInfo = ArticleInfoFlags(
                            links = True,
                            image = True,
                            socialScore = True,
                            sentiment = True
                        ),
                        sourceInfo = SourceInfoFlags(
                            ranking = True
                        )
                    )
                )

data = {}
data["articles"] = []
for art in res:
    data["articles"].append(json.dumps(art))

with open("./results/er_opt.json", "w") as fp:
    json.dump(data, fp)
'''
with open("./results/er_opt.json", "r") as fp:
    df = json.load(fp)
    for i in range(len(df["articles"])):
        df["articles"][i] = json.loads(df["articles"][i])

# context and content comparison of input text and each article

# get support/reject stance for each article

# output result
print('done')