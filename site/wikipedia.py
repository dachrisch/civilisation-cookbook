'''
Created on May 26, 2013

@author: cda
'''

def find_links_in_text(text):
    import re
    return tuple(re.findall(ur"\[\[(.+?)\]\]+?", text))

def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


class WikipediaLink(object):
    def __init__(self, name, source):
        self.name = name
        self.source = source
        
class WikipediaSite(object):
    
    def __parse_title(self, page):
        return page['title']

    def __init__(self, page):
        self.title = self.__parse_title(page)
        self.links = map(lambda link : WikipediaLink(link, self), find_links_in_text(page['revisions'][0]['*']))
