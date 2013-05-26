'''
Created on May 26, 2013

@author: cda
'''
import unittest


def find_links_in_text(text):
    import re
    return tuple(re.findall(ur"\[\[(.+?)\]\]+?", text))


class WikimarkupParserTest(unittest.TestCase):

    def test_will_be_recognized_as_link(self):
        texts = ['Link', 'other Link', 'otherLink', 'Streichholz']
        
        for text in texts:
            self.assertEquals((text, ), find_links_in_text('[[' + text + ']]'))

    def test_file_will_be_recognized_as_link(self):
        text = '[[Datei:File.jpg]]'
        self.assertEquals(('Datei:File.jpg', ), find_links_in_text(text))
        
    def test_will_recognize_all_links(self):
        text = 'This is a text with a [[link]]'
        self.assertEquals(('link',), find_links_in_text(text))
        
    def test_find_all_links_in_text(self):
        text = """<!-- BANNER ACROSS TOP OF PAGE --> {| id="mp-topbanner" style="width:100%; background:#f9f9f9; margin:1.2em 0 6px 0; border:1px solid #ddd;" | style="width:61%; color:#000;" | <!-- "WELCOME TO WIKIPEDIA" AND ARTICLE COUNT --> {| style="width:280px; border:none; background:none;" | style="width:280px; text-align:center; white-space:nowrap; color:#000;" | <div style="font-size:162%; border:none; margin:0; padding:.1em; color:#000;">Welcome to [[Wikipedia]],</div> <div style="top:+0.2em; font-size:95%;">the [[free content|free]] [[encyclopedia]] that [[Wikipedia:Introduction|anyone can edit]].</div> <div id="articlecount" style="font-size:85%;">[[Special:Statistics|{{NUMBEROFARTICLES}}]] articles in [[English language|English]]</div> |} <!-- PORTAL LIST ON RIGHT-HAND SIDE --> | style="width:13%; font-size:95%;" | * [[Portal:Arts|Arts]] * [[Portal:Biography|Biography]] * [[Portal:Geography|Geography]] | style="width:13%; font-size:95%;" | * [[Portal:History|History]] * [[Portal:Mathematics|Mathematics]] * [[Portal:Science|Science]] | style="width:13%; font-size:95%;" | * [[Portal:Society|Society]] * [[Portal:Technology|Technology]] * '''[[Portal:Contents/Portals|All portals]]''' |}"""
        self.assertEquals(('Wikipedia',
 'free content|free',
 'encyclopedia',
 'Wikipedia:Introduction|anyone can edit',
 'Special:Statistics|{{NUMBEROFARTICLES}}',
 'English language|English',
 'Portal:Arts|Arts',
 'Portal:Biography|Biography',
 'Portal:Geography|Geography',
 'Portal:History|History',
 'Portal:Mathematics|Mathematics',
 'Portal:Science|Science',
 'Portal:Society|Society',
 'Portal:Technology|Technology',
 'Portal:Contents/Portals|All portals'), find_links_in_text(text))

if __name__ == "__main__":
    unittest.main()