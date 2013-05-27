'''
Created on May 26, 2013

@author: cda
# -*- coding: UTF-8 -*-
'''

def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


class WikipediaLink(object):
    def __init__(self, name, target_name = None, source = None, parser = None):
        self.name = name
        self.target_name = target_name or name
        self.source = source
        self.parser = parser
        
    @property
    def target(self):
        return WikipediaSite(self.target_name, self.parser)

    def __key(self):
        return (self.name, self.target)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())
    
    def __repr__(self):
        return '%(source)s--[%(name)s]-->%(target)s' % {'source' : self.source,
                                                        'target' : self.target,
                                                        'name' : self.name}

class WikipediaSite(object):
    def __init__(self, title, parser = None):
        self.title = title
        self.parser = parser
        if parser:
            links_and_names = self.parser.parse_links(self.title)
            self.links_by_name = dict((link_and_name['name'], WikipediaLink(link_and_name['name'], link_and_name['link'], self, self.parser)) for link_and_name in links_and_names)

    def __parse_title(self, page):
        return page['title']

    @property
    def links(self):
        return self.links_by_name.values()

    def link(self, name):
        return self.links_by_name[name]

    def __key(self):
        return (self.title, )

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return '(%(title)s)' % self.__dict__