import requests
import language_check
import newspaper
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from newspaper import Article
import urllib.request


#TODO: 1.Prepend u to text for grammarcheck

class WebSpamDetect():

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

    def getLinks(self, url):
        data = newspaper.build(url)
        links = []
        for i in data.articles:
            links.append(i.url)
        return links

