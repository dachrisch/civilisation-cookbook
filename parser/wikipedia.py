'''
Created on May 26, 2013

@author: cda
# -*- coding: UTF-8 -*-
'''
import urllib
import json
import unittest

def find_links_in_text(text):
    import re
    pattern = re.compile(ur"\[\[(?P<link>.+?)(\|(?P<name>.+?))?\]\]+?")
    matches = []
    for match in pattern.finditer(text):
        if match.group('link').startswith('Datei:'):
            continue
        matches.append({'name' : match.group('name') or match.group('link'), 
                        'link' : match.group('link')
                        })
    return matches

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
        str_params = {}
        for k, v in query_params.iteritems():
            str_params[k] = unicode(v).encode('utf-8')
        url = self.endpoint + '?%s' % urllib.urlencode(str_params)
        query_url = urllib.urlopen(url)
        json_object = json.load(query_url)
        return json_object

    def load(self, title):
        json_object = self._query_api(title)
        return json_object

