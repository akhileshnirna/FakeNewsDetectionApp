import pickle
import re
import pandas as pd
import ipaddress as ip
import tldextract
from urllib.parse import urlparse
import tld
import xgboost

class MLClassifier():
    def __init__(self):
        self.model = pickle.load(open('xgb_model.dat', 'rb'))
        self.Suspicious_TLD = ['zip', 'cricket', 'link', 'work', 'party', 'gq', 'kim', 'country', 'science', 'tk']
        self.Suspicious_Domain = ['luckytime.co.kr', 'mattfoll.eu.interia.pl', 'trafficholder.com', 'dl.baixaki.com.br',
                                  'bembed.redtube.comr', 'tags.expo9.exponential.com', 'deepspacer.com', 'funad.co.kr',
                                  'trafficconverter.biz']

    # helper functions definiton
    # Method to count number of dots
    def countdots(self, url):
        return url.count('.')

    # Is IP addr present as th hostname, let's validate

    def isip(self,uri):
        try:
            if ip.ip_address(uri):
                return 1
        except:
            return 0

    # method to check the presence of hyphens

    def isPresentHyphen(self,url):
        return url.count('-')

    # method to check the presence of @

    def isPresentAt(self, url):
        return url.count('@')

    def isPresentDSlash(self,url):
        return url.count('//')

    def countSubDir(self,url):
        return url.count('/')

    def countSubDomain(self, subdomain):
        if not subdomain:
            return 0
        else:
            return len(subdomain.split('.'))

    def getFeatures(self, url, label):
        # print("url is ",url)
        result = []
        url = str(url)

        # add the url to feature set
        result.append(url)

        # parse the URL and extract the domain information
        path = urlparse(url)
        ext = tldextract.extract(url)

        # counting number of dots in subdomain
        result.append(self.countdots(ext.subdomain))  # done

        # checking hyphen in domain
        result.append(self.isPresentHyphen(path.netloc))  # done

        # length of URL
        result.append(len(url))

        # checking @ in the url
        result.append(self.isPresentAt(path.netloc))  # done

        # checking presence of double slash
        result.append(self.isPresentDSlash(path.path))  # done

        # Count number of subdir
        result.append(self.countSubDir(path.path))  # done

        # number of sub domain
        result.append(self.countSubDomain(ext.subdomain))  # done

        # length of domain name
        result.append(len(path.netloc))

        # count number of queries
        result.append(len(path.query))

        # Adding domain information

        # if IP address is being used as a URL
        result.append(self.isip(ext.domain))  # done

        # presence of Suspicious_TLD
        result.append(1 if ext.suffix in self.Suspicious_TLD else 0)

        # presence of suspicious domain
        result.append(1 if '.'.join(ext[1:]) in self.Suspicious_Domain else 0)

        result.append(str(label))
        return result

    def classify(self, data):
        result = pd.DataFrame(columns=('url', 'no of dots', 'presence of hyphen', 'len of url', 'presence of at', 'presence of double slash', 'no of subdir', 'no of subdomain', 'len of domain',
                                       'no of queries', 'is IP', 'presence of Suspicious_TLD', 'presence of suspicious domain', 'label'))
        results = self.getFeatures(data, '1')
        #results.drop(['uses_TLS', 'no of slashes', 'has subdomain', 'has unicode'], axis=0)
        result.loc[0] = results
        result = result.drop(['url', 'label'], axis=1).values
        res = self.model.predict(result)
        if res[0] == '1':
            return True
        else:
            return False


class RuleBasedClassifier():
    # A utility function
    def getHostName(self,url):
        p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        m = re.search(p, url)
        return m.group('host')  # 'www.abc.com'

    def getHostLength(self, url):
        hname = self.getHostName(url)
        return (len(hname))

    def getNoSlashes(self,url):
        cnt = url.count('/')
        return cnt

    def getNoDots(self,url):
        hname = self.getHostName(url)
        return hname.count('.')

    def getTermsCount(self,url):
        hname = self.getHostName(url)
        if (len(hname.split('.')) > len(hname.split('-'))):
            return len(hname.split('.'))
        else:
            return len(hname.split('-'))

    def hasSpecial(self,url):
        hname = self.getHostName(url)
        spl = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', ',', ':', '~', '`']
        for i in spl:
            if i in hname:
                return 1
        return 0

    def isip(self,uri):
        hname = self.getHostName(uri)
        try:
            if ip.ip_address(hname):
                return 1
        except:
            return 0

    def hasUnicode(self,hostname):
        if len(hostname) > 255:
            return False
        hostname = hostname.rstrip(".")
        allowed = re.compile("(?!-)[A-Z\d\-\_]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    '''   
    #This function returns the opposite
    def hasUnicode(url):
        hname = getHostName(url)
        if len(hname) > 255:
            return False
        if hname[-1] == ".":
            hname = hname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hname.split("."))
    '''

    def hasTLS(self, url):
        try:
            if (url.index('https') == 0):
                return 1
        except:
            return 0

    def hasSubDomain(self,url):
        hname = self.getHostName(url)
        sd = hname.split('.')
        if ('www' in sd):
            return 0
        return 1

    def keywordCheck(self, url):
        path = urlparse(url).path

    def hasTLD(self, url):
        try:
            tld.get_tld(url)
            return 1
        except:
            return 0

    def getDotsPath(self, url):
        ur = urlparse(url)
        # return ur
        path = ur.path
        print(path)
        return path.count('.')

    def hyphenCountHname(self, url):
        hname = self.getHostName(url)
        return hname.count('-')

    def lengthURL(self, url):
        return len(url)

    def build_feature_set(self,url):
        data = {}
        data["host_length"] = self.getHostLength(url)
        data['slashes_count'] = self.getNoSlashes(url)
        data['dots_count'] = self.getNoDots(url)
        data['terms_count'] = self.getTermsCount(url)
        data['contains_special'] = self.hasSpecial(url)
        data['contains_ip'] = self.isip(url)
        data['contains_unicode'] = not self.hasUnicode(url)
        data['uses_TLS'] = self.hasTLS(url)
        data['contains_subdomain'] = self.hasSubDomain(url)
        data['contains_tld'] = self.hasTLD(url)
        data['count_dots_path'] = self.getDotsPath(url)
        data['hyphen_count_hname'] = self.hyphenCountHname(url)
        data['url_length'] = self.lengthURL(url)
        return data

    def calculate(self,features):
        return (features['slashes_count'] >= 5 and features['contains_special'] and features['uses_TLS'] and features[
            'contains_tld'] and features['url_length'] > 75) \
               or (features['slashes_count'] >= 5 and features['contains_unicode'] and features['uses_TLS'] and
                   features['url_length'] > 75) \
               or (features['slashes_count'] >= 5 and features['dots_count'] > 4 and features['contains_unicode'] and
                   features['contains_tld']) \
               or (features['slashes_count'] >= 5 and features['contains_unicode'] and features['contains_special'] and
                   features['contains_tld'] and features['url_length'] > 75) \
               or (features['slashes_count'] >= 5 and features['dots_count'] > 4 and features['contains_special'] and
                   features['contains_unicode'] and features['contains_tld']) \
               or (features['slashes_count'] >= 5 and features['dots_count'] > 4 and features['contains_special'] and
                   features['url_length'] > 75) \
               or (features['contains_special'] and features['contains_subdomain'] and features['terms_count'] >= 3) \
               or (features['slashes_count'] >= 5 and features['dots_count'] > 4 and features['uses_TLS'] and
                   features['contains_tld'] and features['url_length'] > 75) \
               or (features['contains_unicode'] and features['terms_count'] > 4 and features['url_length'] > 75)



