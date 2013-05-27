'''
Created on May 26, 2013

@author: cda
'''
import unittest
import json
from site.wikipedia import WikipediaSite, WikipediaLink
from parser.wikipedia import WikipediaLoader, WikipediaApiParser
from collections import Counter

class WikipediaVisitor(object):
    def __init__(self):
        self.max_depth = 1
        self.__current_depth = 0
        
    def _follow_links(self, site):
        print site
        print site.links
        links = site.links[:]
        if self.__current_depth < self.max_depth:
            self.__current_depth += 1
            for link in site.links:
                if link.target in self.__visited_sites:
                    print 'skipping %s' % site
                else:
                    self.__visited_sites.add(link.target)
                    links.extend(self._follow_links(link.target))
            self.__current_depth -= 1
        return links
    
    def _broad_search(self):
        self.__visited_sites = set()
        self.__visited_sites.add(self.start_site)
        all_links = self._follow_links(self.start_site)
        self.__visited_sites = set()
        return all_links

    def link_statistics(self):
        all_links = self._broad_search()
        return Counter(all_links)

class WikipediaLoaderTest(unittest.TestCase):
    def test_create_main_page(self):
        site = WikipediaSite('Main Page', None)
        self.assertEquals('Main Page', site.title) 

    def test_main_page_resolves_links(self):
        loader = WikipediaLoader()
        loader._query_api = lambda title : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Wikipedia:Hauptseite","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"<!--        BANNER ACROSS TOP OF PAGE        -->\n{| id=\"mp-topbanner\" style=\"width:100%; background:#f9f9f9; margin:1.2em 0 6px 0; border:1px solid #ddd;\"\n| style=\"width:61%; color:#000;\" |\n<!--        \"WELCOME TO WIKIPEDIA\" AND ARTICLE COUNT        -->\n{| style=\"width:280px; border:none; background:none;\"\n| style=\"width:280px; text-align:center; white-space:nowrap; color:#000;\" |\n<div style=\"font-size:162%; border:none; margin:0; padding:.1em; color:#000;\">Welcome to [[Wikipedia]],</div>\n<div style=\"top:+0.2em; font-size:95%;\">the [[free content|free]] [[encyclopedia]] that [[Wikipedia:Introduction|anyone can edit]].</div>\n<div id=\"articlecount\" style=\"font-size:85%;\">[[Special:Statistics|{{NUMBEROFARTICLES}}]] articles in [[English language|English]]</div>\n|}\n<!--        PORTAL LIST ON RIGHT-HAND SIDE        -->\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:Arts|Arts]]\n* [[Portal:Biography|Biography]]\n* [[Portal:Geography|Geography]]\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:History|History]]\n* [[Portal:Mathematics|Mathematics]]\n* [[Portal:Science|Science]]\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:Society|Society]]\n* [[Portal:Technology|Technology]]\n* '''[[Portal:Contents/Portals|All portals]]'''\n|}\n<!--        MAIN PAGE BANNER        -->\n{{#if:{{Main Page banner}}|\n<table id=\"mp-banner\" style=\"width: 100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\">\n<tr><td class=\"MainPageBG\" style=\"text-align:center; padding:0.2em; background-color:#fffaf5; border:1px solid #f2e0ce; color:#000; font-size:100%;\">{{Main Page banner}}\n</td></tr>\n</table>\n}}\n<!--        TODAY'S FEATURED CONTENT        -->\n{| id=\"mp-upper\" style=\"width: 100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\"\n<!--        TODAY'S FEATURED ARTICLE; DID YOU KNOW        -->\n| class=\"MainPageBG\" style=\"width:55%; border:1px solid #cef2e0; background:#f5fffa; vertical-align:top; color:#000;\" |\n{| id=\"mp-left\" style=\"width:100%; vertical-align:top; background:#f5fffa;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-tfa-h2\" style=\"margin:3px; background:#cef2e0; font-size:120%; font-weight:bold; border:1px solid #a3bfb1; text-align:left; color:#000; padding:0.2em 0.4em;\">{{#ifexpr:{{formatnum:{{PAGESIZE:Wikipedia:Today's featured article/{{#time:F j, Y}}}}|R}}>150|From today's featured article|Featured article <span style=\"font-size:85%; font-weight:normal;\">(Check back later for today's.)</span>}}</h2>\n|-\n| style=\"color:#000;\" | <div id=\"mp-tfa\" style=\"padding:2px 5px\">{{#ifexpr:{{formatnum:{{PAGESIZE:Wikipedia:Today's featured article/{{#time:F j, Y}}}}|R}}>150|{{Wikipedia:Today's featured article/{{#time:F j, Y}}}}|{{Wikipedia:Today's featured article/{{#time:F j, Y|-1 day}}}}}}</div>\n|-\n| style=\"padding:2px;\" | <h2 id=\"mp-dyk-h2\" style=\"margin:3px; background:#cef2e0; font-size:120%; font-weight:bold; border:1px solid #a3bfb1; text-align:left; color:#000; padding:0.2em 0.4em;\">Did you know...</h2>\n|-\n| style=\"color:#000; padding:2px 5px 5px;\" | <div id=\"mp-dyk\">{{Did you know}}</div>\n|}\n| style=\"border:1px solid transparent;\" |\n<!--        IN THE NEWS; ON THIS DAY        -->\n| class=\"MainPageBG\" style=\"width:45%; border:1px solid #cedff2; background:#f5faff; vertical-align:top;\"|\n{| id=\"mp-right\" style=\"width:100%; vertical-align:top; background:#f5faff;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-itn-h2\" style=\"margin:3px; background:#cedff2; font-size:120%; font-weight:bold; border:1px solid #a3b0bf; text-align:left; color:#000; padding:0.2em 0.4em;\">In the news</h2>\n|-\n| style=\"color:#000; padding:2px 5px;\" | <div id=\"mp-itn\">{{In the news}}</div>\n|-\n| style=\"padding:2px;\" | <h2 id=\"mp-otd-h2\" style=\"margin:3px; background:#cedff2; font-size:120%; font-weight:bold; border:1px solid #a3b0bf; text-align:left; color:#000; padding:0.2em 0.4em;\">On this day...</h2>\n|-\n| style=\"color:#000; padding:2px 5px 5px;\" | <div id=\"mp-otd\">{{Wikipedia:Selected anniversaries/{{#time:F j}}}}</div>\n|}\n|}\n<!--        TODAY'S FEATURED LIST        --><!-- CONDITIONAL: SHOW/HIDE FROM HERE -->{{#switch:{{CURRENTDAYNAME}}|Monday=\n<table id=\"mp-middle\" style=\"width:100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\">\n<tr>\n<td class=\"MainPageBG\" style=\"width:100%; border:1px solid #f2cedd; background:#fff5fa; vertical-align:top; color:#000;\">\n<table id=\"mp-center\" style=\"width:100%; vertical-align:top; background:#fff5fa; color:#000;\">\n<tr>\n<td style=\"padding:2px;\"><h2 id=\"mp-tfl-h2\" style=\"margin:3px; background:#f2cedd; font-size:120%; font-weight:bold; border:1px solid #bfa3af; text-align:left; color:#000; padding:0.2em 0.4em\">From today's featured list</h2></td>\n</tr><tr>\n<td style=\"color:#000;\"><div id=\"mp-tfl\" style=\"padding:2px 5px;\">{{#ifexist:Wikipedia:Today's featured list/{{#time:F j, Y}}|{{Wikipedia:Today's featured list/{{#time:F j, Y}}}}|{{TFLempty}}}}</div></td>\n</tr>\n</table>\n</td>\n</tr>\n</table>\n<!--        END TODAY'S FEATURED LIST        --><!-- CONDITIONAL: SHOW/HIDE TO HERE -->|}}\n<!--        TODAY'S FEATURED PICTURE        -->\n{| id=\"mp-lower\" style=\"margin:4px 0 0 0; width:100%; background:none; border-spacing: 0px;\"\n| class=\"MainPageBG\" style=\"width:100%; border:1px solid #ddcef2; background:#faf5ff; vertical-align:top; color:#000;\" |\n{| id=\"mp-bottom\" style=\"width:100%; vertical-align:top; background:#faf5ff; color:#000;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-tfp-h2\" style=\"margin:3px; background:#ddcef2; font-size:120%; font-weight:bold; border:1px solid #afa3bf; text-align:left; color:#000; padding:0.2em 0.4em\">{{#ifexist:Template:POTD protected/{{#time:Y-m-d}}|Today's featured picture | Featured picture&ensp;<span style=\"font-size:85%; font-weight:normal;\">(Check back later for today's.)</span>}}</h2>\n|-\n| style=\"color:#000; padding:2px;\" | <div id=\"mp-tfp\">{{#ifexist:Template:POTD protected/{{#time:Y-m-d}}|{{POTD protected/{{#time:Y-m-d}}}}|{{POTD protected/{{#time:Y-m-d|-1 day}}}}}}</div>\n|}\n|}\n<!--        SECTIONS AT BOTTOM OF PAGE        -->\n<div id=\"mp-other\" style=\"padding-top:4px; padding-bottom:2px;\">\n== Other areas of Wikipedia ==\n{{Other areas of Wikipedia}}\n</div><div id=\"mp-sister\">\n== Wikipedia's sister projects ==\n{{Wikipedia's sister projects}}\n</div><div id=\"mp-lang\">\n== Wikipedia languages ==\n{{Wikipedia languages}}\n</div>\n<!--        INTERWIKI STRAPLINE        -->\n<noinclude>{{Main Page interwikis}}{{noexternallanglinks}}</noinclude>__NOTOC____NOEDITSECTION__"}]}}}}""")
        parser = WikipediaApiParser(loader)
        site = WikipediaSite('Main Page', parser)
        self.assertEquals(15, len(site.links))

    def test_main_page_navigates_link_to_target_site(self):
        loader = WikipediaLoader()
        loader._query_api = lambda title : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Source Page","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"link to [[Target Page]], other link won't count [[Wikipedia]]"}]}}}}""")
        parser = WikipediaApiParser(loader)
        site = WikipediaSite('Main Page', parser)
        self.assertEquals('Wikipedia', site.link('Wikipedia').target.title)

    def test_main_page_navigates_link_name_to_target_site(self):
        loader = WikipediaLoader()
        loader._query_api = lambda title : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Source Page","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"link to [[Target Page]], other link won't count [[Wikipedia|next]]"}]}}}}""")
        parser = WikipediaApiParser(loader)
        site = WikipediaSite('Main Page', parser)
        self.assertEquals('Wikipedia', site.link('next').target.title)

class WikipediaVisitorTest(unittest.TestCase):
    def test_visit_all_links(self):
        loader = WikipediaLoader()
        loader._query_api = lambda title : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Wikipedia:Hauptseite","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"<!--        BANNER ACROSS TOP OF PAGE        -->\n{| id=\"mp-topbanner\" style=\"width:100%; background:#f9f9f9; margin:1.2em 0 6px 0; border:1px solid #ddd;\"\n| style=\"width:61%; color:#000;\" |\n<!--        \"WELCOME TO WIKIPEDIA\" AND ARTICLE COUNT        -->\n{| style=\"width:280px; border:none; background:none;\"\n| style=\"width:280px; text-align:center; white-space:nowrap; color:#000;\" |\n<div style=\"font-size:162%; border:none; margin:0; padding:.1em; color:#000;\">Welcome to [[Wikipedia]],</div>\n<div style=\"top:+0.2em; font-size:95%;\">the [[free content|free]] [[encyclopedia]] that [[Wikipedia:Introduction|anyone can edit]].</div>\n<div id=\"articlecount\" style=\"font-size:85%;\">[[Special:Statistics|{{NUMBEROFARTICLES}}]] articles in [[English language|English]]</div>\n|}\n<!--        PORTAL LIST ON RIGHT-HAND SIDE        -->\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:Arts|Arts]]\n* [[Portal:Biography|Biography]]\n* [[Portal:Geography|Geography]]\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:History|History]]\n* [[Portal:Mathematics|Mathematics]]\n* [[Portal:Science|Science]]\n| style=\"width:13%; font-size:95%;\" |\n* [[Portal:Society|Society]]\n* [[Portal:Technology|Technology]]\n* '''[[Portal:Contents/Portals|All portals]]'''\n|}\n<!--        MAIN PAGE BANNER        -->\n{{#if:{{Main Page banner}}|\n<table id=\"mp-banner\" style=\"width: 100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\">\n<tr><td class=\"MainPageBG\" style=\"text-align:center; padding:0.2em; background-color:#fffaf5; border:1px solid #f2e0ce; color:#000; font-size:100%;\">{{Main Page banner}}\n</td></tr>\n</table>\n}}\n<!--        TODAY'S FEATURED CONTENT        -->\n{| id=\"mp-upper\" style=\"width: 100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\"\n<!--        TODAY'S FEATURED ARTICLE; DID YOU KNOW        -->\n| class=\"MainPageBG\" style=\"width:55%; border:1px solid #cef2e0; background:#f5fffa; vertical-align:top; color:#000;\" |\n{| id=\"mp-left\" style=\"width:100%; vertical-align:top; background:#f5fffa;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-tfa-h2\" style=\"margin:3px; background:#cef2e0; font-size:120%; font-weight:bold; border:1px solid #a3bfb1; text-align:left; color:#000; padding:0.2em 0.4em;\">{{#ifexpr:{{formatnum:{{PAGESIZE:Wikipedia:Today's featured article/{{#time:F j, Y}}}}|R}}>150|From today's featured article|Featured article <span style=\"font-size:85%; font-weight:normal;\">(Check back later for today's.)</span>}}</h2>\n|-\n| style=\"color:#000;\" | <div id=\"mp-tfa\" style=\"padding:2px 5px\">{{#ifexpr:{{formatnum:{{PAGESIZE:Wikipedia:Today's featured article/{{#time:F j, Y}}}}|R}}>150|{{Wikipedia:Today's featured article/{{#time:F j, Y}}}}|{{Wikipedia:Today's featured article/{{#time:F j, Y|-1 day}}}}}}</div>\n|-\n| style=\"padding:2px;\" | <h2 id=\"mp-dyk-h2\" style=\"margin:3px; background:#cef2e0; font-size:120%; font-weight:bold; border:1px solid #a3bfb1; text-align:left; color:#000; padding:0.2em 0.4em;\">Did you know...</h2>\n|-\n| style=\"color:#000; padding:2px 5px 5px;\" | <div id=\"mp-dyk\">{{Did you know}}</div>\n|}\n| style=\"border:1px solid transparent;\" |\n<!--        IN THE NEWS; ON THIS DAY        -->\n| class=\"MainPageBG\" style=\"width:45%; border:1px solid #cedff2; background:#f5faff; vertical-align:top;\"|\n{| id=\"mp-right\" style=\"width:100%; vertical-align:top; background:#f5faff;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-itn-h2\" style=\"margin:3px; background:#cedff2; font-size:120%; font-weight:bold; border:1px solid #a3b0bf; text-align:left; color:#000; padding:0.2em 0.4em;\">In the news</h2>\n|-\n| style=\"color:#000; padding:2px 5px;\" | <div id=\"mp-itn\">{{In the news}}</div>\n|-\n| style=\"padding:2px;\" | <h2 id=\"mp-otd-h2\" style=\"margin:3px; background:#cedff2; font-size:120%; font-weight:bold; border:1px solid #a3b0bf; text-align:left; color:#000; padding:0.2em 0.4em;\">On this day...</h2>\n|-\n| style=\"color:#000; padding:2px 5px 5px;\" | <div id=\"mp-otd\">{{Wikipedia:Selected anniversaries/{{#time:F j}}}}</div>\n|}\n|}\n<!--        TODAY'S FEATURED LIST        --><!-- CONDITIONAL: SHOW/HIDE FROM HERE -->{{#switch:{{CURRENTDAYNAME}}|Monday=\n<table id=\"mp-middle\" style=\"width:100%; margin:4px 0 0 0; background:none; border-spacing: 0px;\">\n<tr>\n<td class=\"MainPageBG\" style=\"width:100%; border:1px solid #f2cedd; background:#fff5fa; vertical-align:top; color:#000;\">\n<table id=\"mp-center\" style=\"width:100%; vertical-align:top; background:#fff5fa; color:#000;\">\n<tr>\n<td style=\"padding:2px;\"><h2 id=\"mp-tfl-h2\" style=\"margin:3px; background:#f2cedd; font-size:120%; font-weight:bold; border:1px solid #bfa3af; text-align:left; color:#000; padding:0.2em 0.4em\">From today's featured list</h2></td>\n</tr><tr>\n<td style=\"color:#000;\"><div id=\"mp-tfl\" style=\"padding:2px 5px;\">{{#ifexist:Wikipedia:Today's featured list/{{#time:F j, Y}}|{{Wikipedia:Today's featured list/{{#time:F j, Y}}}}|{{TFLempty}}}}</div></td>\n</tr>\n</table>\n</td>\n</tr>\n</table>\n<!--        END TODAY'S FEATURED LIST        --><!-- CONDITIONAL: SHOW/HIDE TO HERE -->|}}\n<!--        TODAY'S FEATURED PICTURE        -->\n{| id=\"mp-lower\" style=\"margin:4px 0 0 0; width:100%; background:none; border-spacing: 0px;\"\n| class=\"MainPageBG\" style=\"width:100%; border:1px solid #ddcef2; background:#faf5ff; vertical-align:top; color:#000;\" |\n{| id=\"mp-bottom\" style=\"width:100%; vertical-align:top; background:#faf5ff; color:#000;\"\n| style=\"padding:2px;\" | <h2 id=\"mp-tfp-h2\" style=\"margin:3px; background:#ddcef2; font-size:120%; font-weight:bold; border:1px solid #afa3bf; text-align:left; color:#000; padding:0.2em 0.4em\">{{#ifexist:Template:POTD protected/{{#time:Y-m-d}}|Today's featured picture | Featured picture&ensp;<span style=\"font-size:85%; font-weight:normal;\">(Check back later for today's.)</span>}}</h2>\n|-\n| style=\"color:#000; padding:2px;\" | <div id=\"mp-tfp\">{{#ifexist:Template:POTD protected/{{#time:Y-m-d}}|{{POTD protected/{{#time:Y-m-d}}}}|{{POTD protected/{{#time:Y-m-d|-1 day}}}}}}</div>\n|}\n|}\n<!--        SECTIONS AT BOTTOM OF PAGE        -->\n<div id=\"mp-other\" style=\"padding-top:4px; padding-bottom:2px;\">\n== Other areas of Wikipedia ==\n{{Other areas of Wikipedia}}\n</div><div id=\"mp-sister\">\n== Wikipedia's sister projects ==\n{{Wikipedia's sister projects}}\n</div><div id=\"mp-lang\">\n== Wikipedia languages ==\n{{Wikipedia languages}}\n</div>\n<!--        INTERWIKI STRAPLINE        -->\n<noinclude>{{Main Page interwikis}}{{noexternallanglinks}}</noinclude>__NOTOC____NOEDITSECTION__"}]}}}}""")
        parser = WikipediaApiParser(loader)
        site = WikipediaSite('Main Page', parser)
        for link in site.links:
            self.assertTrue(link.target.title in ('Wikipedia',
 'free content',
 'encyclopedia',
 'Wikipedia:Introduction',
 'Special:Statistics',
 'English language',
 'Portal:Arts',
 'Portal:Biography',
 'Portal:Geography',
 'Portal:History',
 'Portal:Mathematics',
 'Portal:Science',
 'Portal:Society',
 'Portal:Technology',
 'Portal:Contents/Portals'))
            
    def test_visit_all_sites_by_depth(self):
        loader = WikipediaLoader()
        pages = {'Source Page' : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Source Page","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"link to [[Target Page]], "}]}}}}"""),
                'Target Page' : json.loads(r"""{"query":{"pages":{"15580374":{"pageid":15580374,"ns":0,"title":"Target Page","revisions":[{"contentformat":"text/x-wiki","contentmodel":"wikitext","*":"link to [[Source Page]]"}]}}}}""")
                }
        loader._query_api = lambda title : pages[title]
        parser = WikipediaApiParser(loader)
        site = WikipediaSite('Source Page', parser)
        visitor = WikipediaVisitor()
        visitor.start_site = site
        visitor.max_depth = 2
        sites = visitor.link_statistics().items()
        self.assertEquals([(WikipediaLink('Source Page', source = WikipediaSite('Target Page')), 1), 
                           (WikipediaLink('Target Page', source = WikipediaSite('Source Page')), 1)], 
                          sites)


if __name__ == "__main__":
    unittest.main()