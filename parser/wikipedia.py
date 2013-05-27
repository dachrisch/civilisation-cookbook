'''
Created on May 26, 2013

@author: cda
'''
import urllib
import json
import unittest

def find_links_in_text(text):
    import re
    pattern = re.compile(ur"\[\[(?P<link>.+?)(\|(?P<name>.+?))?\]\]+?")
    matches = []
    for match in pattern.finditer(text):
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
        query_url = urllib.urlopen(self.endpoint + '?%s' % urllib.urlencode(query_params))
        json_object = json.load(query_url)
        return json_object

    def load(self, title):
        json_object = self._query_api(title)
        return json_object

class WikipediaApiParserTest(unittest.TestCase):
    def test_parse_link_from_markup(self):
        matche = find_links_in_text('[[a link]]')[0]
        self.assertEquals('a link', matche['name'])
        self.assertEquals('a link', matche['link'])

    def test_parse_link_and_name_from_markup(self):
        matche = find_links_in_text('[[a link|a name]]')[0]
        self.assertEquals('a name', matche['name'])
        self.assertEquals('a link', matche['link'])

    def test_parse_two_links_and_one_name_from_markup(self):
        matches = find_links_in_text('[[a link|a name]] and [[an other link]]')
        self.assertEquals('a name', matches[0]['name'])
        self.assertEquals('a link', matches[0]['link'])
        self.assertEquals('an other link', matches[1]['name'])
        self.assertEquals('an other link', matches[1]['link'])

