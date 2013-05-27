'''
Created on May 26, 2013

@author: cda
'''
import urllib
import json


def find_links_in_text(text):
    import re
    return tuple(re.findall(ur"\[\[(.+?)\]\]+?", text))

class WikipediaApiParser(object):
    
    def __init__(self, loader):
        self.loader = loader

    def parse_links(self, title):
        content = self._parse_content(title)
        return find_links_in_text(content)

    def _parse_content(self, title):
        json_object = self.loader.load(title)
        pages = json_object['query']['pages']
        assert len(pages.keys()) == 1, pages.keys()
        content = pages.values()[0]['revisions'][0]['*']
        return content

class WikipediaLoader(object):
    def __init__(self):
        self.endpoint = 'http://de.wikipedia.org/w/api.php'
        self.params = {'format' : 'json',
                       'action' : 'query',
                       'prop' : 'revisions',
                       'rvprop' : 'content'}

    def _query_api(self, title):
        query_params = self.params.copy()
        query_params['titles'] = title
        query_url = urllib.urlopen(self.endpoint + '?%s' % urllib.urlencode(query_params))
        json_object = json.load(query_url)
        return json_object

    def load(self, title):
        json_object = self._query_api(title)
        return json_object
