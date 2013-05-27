'''
Created on May 27, 2013

@author: cda
# -*- coding: UTF-8 -*-
'''
from collections import Counter
from parser.wikipedia import WikipediaLoader, WikipediaApiParser
from site.wikipedia import WikipediaSite

class WikipediaVisitor(object):
    def __init__(self):
        self.max_depth = 1
        self.__current_depth = 0
        
    def _follow_links(self, site):
        print u'visiting %s' % (site)
        links = site.links[:]
        if self.__current_depth < self.max_depth:
            self.__current_depth += 1
            for link in site.links:
                if link.target in self.__visited_sites:
                    print 'skipping %s' % site
                else:
                    self.__visited_sites.add(link.target)
                    print 'following %s' % link
                    links.extend(self._follow_links(link.target))
            self.__current_depth -= 1
        return links
    
    def _deep_search(self):
        self.__visited_sites = set()
        self.__visited_sites.add(self.start_site)
        all_links = self._follow_links(self.start_site)
        self.__visited_sites = set()
        return all_links

    def link_statistics(self):
        all_links = self._deep_search()
        return Counter(all_links)

if __name__ == '__main__':
    loader = WikipediaLoader()
    parser = WikipediaApiParser(loader)
    visitor = WikipediaVisitor()
    visitor.start_site = WikipediaSite(ur'Streichholz', parser)
    visitor.max_depth = 2
    sites = visitor.link_statistics()
    print sites