'''
Created on May 26, 2013

@author: cda
'''

class WikipediaLink(object):
    def __init__(self, name, source, parser):
        self.name = name
        self.source = source
        self.parser = parser
        
    @property
    def target(self):
        return WikipediaSite(self.name, self.parser)

def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop

class WikipediaSite(object):
    
    def __parse_title(self, page):
        return page['title']

    def __init__(self, title, parser):
        self.title = title
        self.parser = parser

    @lazyprop
    def links(self):
        links = self.parser.parse_links(self.title)
        return dict((link, WikipediaLink(link, self, self.parser)) for link in links)

    def link(self, name):
        return self.links[name]