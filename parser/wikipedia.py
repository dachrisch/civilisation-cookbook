'''
Created on May 26, 2013

@author: cda
'''
from site.wikipedia import WikipediaSite
import urllib
import json

class WikipediaApiParser(object):

    def parse_site_from_json(self, json):
        pages = json['query']['pages']
        assert len(pages.keys()) == 1, pages.keys()
        content = pages.values()[0]
        return WikipediaSite(content)

class WikipediaLoader(object):
    def __init__(self):
        self.endpoint = 'http://de.wikipedia.org/w/api.php'
        self.params = {'format' : 'json',
                       'action' : 'query',
                       'prop' : 'revisions',
                       'rvprop' : 'content'}
        self.parser = WikipediaApiParser()
        self.__site_cache = {}

    def json_fetch(self, title):
        query_params = self.params.copy()
        query_params['titles'] = title
        query_url = urllib.urlopen(self.endpoint + '?%s' % urllib.urlencode(query_params))
        return json.load(query_url)

    def load_site_by_title(self, title):
        if title not in self.__site_cache.keys():
            json_object = self.json_fetch(title)
            site = self.parser.parse_site_from_json(json_object)
            assert title == site.title, site.title
            self.__site_cache[site.title] = site
        return self.__site_cache[title]
