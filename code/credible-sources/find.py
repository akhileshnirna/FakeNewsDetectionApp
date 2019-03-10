#! /usr/bin/python3
'''
startSourceRankPercentile and endSourceRankPercentile: The parameters can be used to filter the returned articles to include only those that are from news sources that are of a certain ranking. Sources are ranked according to the global Alexa site ranking. By setting startSourceRankPercentile to 0 and endSourceRankPercentile to 20 would, for example, return only articles from top ranked news sources that would amount to about approximately 20% of all matching content. Note: 20 percentiles do not represent 20% of all top sources. The value is used to identify the subset of news sources that generate approximately 20% of our collected news content.
'''

from eventregistry import *
from build_database import *


def process_input_text(input_text):
    pass


# output_text = process_input_text(input_text)
# print(output_text)
# upload input text from file/GUI/command line
input_text = ["donald trump is using emergency funds to build his border wall"]

# preprocess text
# annotate with concepts? EventRegistry.getConceptUri()
# processed_text_list = input_text.split(".")

# get articles from event-registry with processed text from list of credible sources URIs
# API_KEY = "eda39267-9017-481a-860d-0b565c6d8bf3"
# API_KEY = "1d3ce38b-3606-4bb3-94b5-904df0583c3c"
# er = EventRegistry(apiKey = API_KEY)

er = EventRegistry()

# print("Reminaing available requests: ", er.getRemainingAvailableRequests())
# print("Daily available requests: ", er.getDailyAvailableRequests())

it = QueryArticlesIter(
        keywords = QueryItems.OR(input_text), # pass list of strings
        dataType = ["news", "pr", "blog"],
        keywordsLoc = "body,title",
        sourceUri = QueryItems.OR(['politifact.com']),
        lang="eng"
    )

print("Total articles retrieved: ", it.count(er))
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

res_file = open("er_opt.txt", "w")

for article in res['articles']['results']:
    res_file.write(article)

# context and content comparison of input text and each article

# get support/reject stance for each article

# output result
print('done')