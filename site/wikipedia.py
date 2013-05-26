'''
Created on May 26, 2013

@author: cda
'''
class WikipediaSite(object):
    
    def parse_title(self, page):
        return page['title']

    def __init__(self, page):
        self.title = self.parse_title(page)
