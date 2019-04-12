import requests
import language_check
import newspaper
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from newspaper import Article
import tld
from nltk.corpus import stopwords
import urllib.request


#TODO: 1.Prepend u to text for grammarcheck

class WebSpamDetect():

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.tlds = ['biz','gdn','loan','work','date','bid','racing','world','ooo','ltd']  #as of April 2019, most abused tlds

    def getRawHTMLData(self, url):
        try:
            conn = requests.get(url)
        except:
            return -1
        html = conn.text
        return html

    def grammarCheck(self,url):
        text = u"".join(self.getFullTextData(url))
        tool = language_check.LanguageTool('en-US')
        matches = tool.check(text)
        return len(matches)

    def getArticle(self, url):
        p = Article(url, language="en")
        p.download()
        p.parse()
        return p.text

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def getFullTextData(self, url):
        html = self.getRawHTMLData(url)
        return self.text_from_html(html)

    #1
    def countWords(self, url):
        html = self.getRawHTMLData(url)
        clean_text = self.text_from_html(html)
        return (len(clean_text.split()))

    #2
    def TLDcheck(self,url):
        domain = tld.get_tld(url)
        return domain

    #3
    def getTitleLength(self,url):
        html = self.getRawHTMLData(url)
        soup = BeautifulSoup(html, "lxml")
        title = soup.find("title").text
        tokens = title.strip().split()
        clean_tokens = [t for t in tokens if re.match(r'[^\W\d]*$', t)]
        filtered_sent = []
        for i in clean_tokens:
            if i not in self.stop_words:
                filtered_sent.append(i)
        return len(filtered_sent)

    def getAllTextAnchors(self,url):
        html = self.getRawHTMLData(url)
        soup = BeautifulSoup(html, "lxml")
        anchor = soup.find_all("a")
        tot = len(anchor)
        for i in anchor:
            if i.text == '':
                tot = tot - 1
        return tot


    def getLinks(self, url):
        data = newspaper.build(url)
        links = []
        for i in data.articles:
            links.append(i.url)
        return links

