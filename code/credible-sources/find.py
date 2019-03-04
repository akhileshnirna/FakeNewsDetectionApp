#! /usr/bin/python3
'''
startSourceRankPercentile and endSourceRankPercentile: The parameters can be used to filter the returned articles to include only those that are from news sources that are of a certain ranking. Sources are ranked according to the global Alexa site ranking. By setting startSourceRankPercentile to 0 and endSourceRankPercentile to 20 would, for example, return only articles from top ranked news sources that would amount to about approximately 20% of all matching content. Note: 20 percentiles do not represent 20% of all top sources. The value is used to identify the subset of news sources that generate approximately 20% of our collected news content.
'''

from eventregistry import *

# get URI for all credible sources
source_uri = [
    'bbc.com',                          # news
    'blogs.wsj.com', 
    'npr.org',
    'pbs.org',
    'abcnews.go.com',
    'cbsnews.com',
    'nbcnews.com',
    'apnews.com',
    'edition.cnn.com',
    'nytimes.com',
    'nypost.com',
    'washingtonpost.com',
    'msnbc.com',
    'theguardian.com',
    'bloomberg.com',
    'newyorker.com',
    'politico.com',
    'foxnews.com',
    'huffingtonpost.com',
    'economist.com',
    'buzzfeednews.com',
    'vox.com',
    'reuters.com',
    'in.reuters.com',
    'forbes.com',
    'ndtv.com',
    'timesofindia.indiatimes.com',
    'economictimes.indiatimes.com',
    'ibtimes.co.in',
    'huffingtonpost.in',
    'indiatoday.in'
    'foxsports.com',                    # sports
    'espn.com',
    'nfl.com',
    'cbssports.com',
    'fifa.com',
    'techcrunch.com',                   # technology
    'wired.com',
    'lifehacker.com',
    'macworld.com',
    'pcworld.com',
    'engadget.com',
    'readwrite.com',
    'mashable.com',
    'gizmodo.com',
    'venturebeat.com',
    'recode.net',
    'cnet.com',
    'howtogeek.com',
    'entrepreneur.com',                 # business
    'hbr.org',
    'freakonomics.com',
    'ritholtz.com',
    'fortune.com',
    'business-standard.com',
    'businessinsider.com',
    'foxbusiness.com',
    'businesstimes.com.sg',
    'factly.in',                        # fact-checking
    'factcheck.org',
    'snopes.com',
    'checkyourfact.com',
    'politifact.com',
    'thequint.com'
    ]


def process_input_text(input_text):
    


output_text = process_input_text(input_text)
print(output_text)
# upload input text from file/GUI/command line
input_text = ""

# preprocess text
# annotate with concepts? EventRegistry.getConceptUri()
# processed_text_list = input_text.split(".")

# get articles from event-registry with processed text from list of credible sources URIs
# API_KEY = "eda39267-9017-481a-860d-0b565c6d8bf3"
API_KEY = "1d3ce38b-3606-4bb3-94b5-904df0583c3c"
er = EventRegistry(apiKey = API_KEY)

# print("Reminaing available requests: ", er.getRemainingAvailableRequests())
# print("Daily available requests: ", er.getDailyAvailableRequests())

it = QueryArticlesIter(
        keywords = QueryItems.OR(input_text), # pass list of strings
        dataType = ["news", "pr", "blog"],
        keywordsLoc = "body,title",
        sourceUri = QueryItems.OR(source_uri),
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

for article in res['articles']['results']:
    print(article)

# context and content comparison of input text and each article

# get support/reject stance for each article

# output result
print('done')