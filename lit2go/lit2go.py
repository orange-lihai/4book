#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys, os, time, datetime, json
from jsonweb.encode import to_object, dumper
from jsonweb.decode import from_object, loader
from bs4 import BeautifulSoup as BS
from bs4 import Tag as BSTag
from bs4 import NavigableString

sys.path.append('..')
from common.http_util import do_get
from common.utils import time_diff, save2txt

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, '../logs/')
OUTPUT_DIR = os.path.join(BASE_DIR, '../output/')

prefix_url = "http://etc.usf.edu/lit2go/"
__max_book_id = 222
__max_book_id_time = datetime.datetime.now()

@from_object()
@to_object()
class Book(object):
    def __init__(self, iid = None, url = None, name = None, author = None, desc = None, source = None, cover_img = None, year_published = None
                 , language = None, country_of_origin = None, readability = None, word_count = None, genre = None, keywords = None):
        self.iid = iid
        self.url = url
        self.name = name
        self.author = author
        self.desc = desc
        self.source = source
        self.cover_img = cover_img
        self.year_published = year_published
        self.language = language
        self.country_of_origin = country_of_origin
        self.readability = readability
        self.word_count = word_count
        self.genre = genre
        self.keywords = keywords
    def __delete__(self):
        pass  

@to_object()  
@from_object()
class Charpter(object):
    def __init__(self, book = None, char_name = None, char_desc = None, char_order = None, char_url = None, char_mp3 = None, char_text = None):
        self.book = book
        self.char_name = char_name
        self.char_desc = char_desc
        self.char_order = char_order
        self.char_url = char_url
        self.char_mp3 = char_mp3
        self.char_text = char_text
        pass
    def __delete__(self):
        pass     
    
@to_object()
@from_object()
class Section(object):
    def __init__(self, charpter = None, section_text = None, section_order = None):
        self.charpter = charpter
        self.section_text = section_text
        self.section_order = section_order
        pass
    def __delete__(self):
        pass      
    

### this function to get "__max_book_id" is an illusion
def max_book_id():
    _now = datetime.datetime.now()
    _day = time_diff(_now, __max_book_id_time)
    if _day > 1:
        return __max_book_id
    else:
        return __max_book_id

def get_book_by_url(book_url = None):
    _book_doc = BS(do_get(book_url), "html.parser")
    # _book_doc = BS(open(OUTPUT_DIR + 'test_222.html'), "html.parser")
    _book = Book()
    _charpters = []
    _sections = []
    
    # fill _book
    _doc_page_content = _book_doc.find(name="div", attrs={"id": "page_content"})
    _doc_hear = _doc_page_content.find(name="header", recursive=False)
    _doc_title = _doc_hear.find(name="h2", recursive=False)
    _doc_author = _doc_hear.find(name="a")
    _doc_column_primary = _book_doc.find(name="div", attrs={"id": "column_primary"})
    _doc_page_thumbnail = _book_doc.find(name="div", attrs={"id": "page_thumbnail"})
    _doc_img = _doc_page_thumbnail.find("img").attrs["src"]
    
    _book.url = book_url
    _book.iid = book_url.split("/")[-2]
    _book.name = _doc_title.string.strip('\n')
    _book.author = _doc_author.string.strip('\n')
    _book.cover_img = _doc_img
    
    _ps = _doc_column_primary.find_all(name="p", recursive=False)
    for i, _p in enumerate(_ps):
        _strong_tag = _p.find(name="strong")
        _em_tag = _p.find(name="em")
        if None != _strong_tag: _book.source = _p.text
        if None != _em_tag: _book.desc = _p.string
    if None == _book.desc: _book.desc = _ps[0].text
        
    _doc_column_secondary = _doc_page_content.find(name="div", attrs={"id": "column_secondary"})
    _doc_column2_strong = _doc_column_secondary.find_all(name="strong")
    for _s in _doc_column2_strong:
        _ss = _s.string
        _ss_next_tag = _s.next_sibling
        if _ss_next_tag == "\n": _ss_next_tag = _ss_next_tag.next_sibling
        if _ss_next_tag == "\n": _ss_next_tag = _ss_next_tag.next_sibling
        _ss_next = ""
        if isinstance(_ss_next_tag, BSTag): _ss_next = _ss_next_tag.text
        if isinstance(_ss_next_tag, NavigableString): _ss_next = _ss_next_tag.string
        
        if _ss.find("Year Published") >= 0:
            _book.year_published = _ss_next
            continue
        if _ss.find("Language") >= 0: 
            _book.language = _ss_next
            continue
        if _ss.find("Country of Origin") >= 0: 
            _book.country_of_origin = _ss_next
            continue
        if _ss.find("Readability") >= 0: 
            _book.readability = _ss_next
            continue
        if _ss.find("Word Count") >= 0: 
            _book.word_count = _ss_next
            continue
        if _ss.find("Genre") >= 0: 
            _book.genre = _ss_next
            continue
        if _ss.find("Keywords") >= 0: 
            _book.keywords = _ss_next
            continue
    
    # fill _charpters
    _dts = _doc_column_primary.find_all(name="dt")
    for i, _dt in enumerate(_dts):
        _dta = _dt.find(name="a")        
        
        _char = Charpter()
        _char.book = _book
        _char.char_order = i
        _char.char_name = _dta.string
        _char.char_url = _dta.attrs["href"]
        _dtdd = _dt.find_next_sibling()
        if _dtdd.name == "dd": _char.char_desc = _dtdd.string        
        
        _charpters.append(_char)
        
    # _sections
    # _charpters = []
    for _c in _charpters:
        _char_url = _c.char_url
        _char_doc = BS(do_get(_char_url), "html.parser")
        # _char_doc = BS(open(OUTPUT_DIR + 'test_222_charpter.html'), "html.parser")
        _mp3_ul = _char_doc.find(name="ul", attrs={"id": "downloads"})
        _mp3_a = _mp3_ul.find(name="a")
        _content = _char_doc.find(name="div", attrs={"id": "i_apologize_for_the_soup"})
        if None != _mp3_a: _c.char_mp3 = _mp3_a.attrs['href']
        
        _ps = _content.find_all(name="p", recursive=False)
        for i, _p in enumerate(_ps):
            _section = Section()
            _section.charpter = _c
            _section.section_text = _p.string
            _section.section_order = i
            
            _sections.append(_section)
        
    return _book, _charpters, _sections

def get_book_by_id(book_id = None):
    book_url = prefix_url + "/" + book_id + "/"
    return get_book_by_url(book_url)

def all2json():
    _max_book_id = max_book_id()
    for i in range(_max_book_id):
        _book_id = i + 1
        try:
            print "_book_id => " + str(_book_id)
            id2mobi(book_id=_book_id)
        except:
            print "_book_id Error" + str(_book_id)
            

def url2json(book_url = None):
    # extract data from web
    book, charpters, sections = get_book_by_url(book_url)
    # save2txt
    save2txt(file_name = "lit2go_" + str(book.iid) + ".json"  , rs = sections)
    # convert to mobi
    # convert2mobi(book=book, charpters=charpters, sections=sections)
    # return 
    return book, charpters, sections

def id2json(book_id = None):
    book_url = prefix_url + "/" + str(book_id) + "/"
    if book_id is not None and book_id > 0 and book_id <= max_book_id():
        return url2json(book_url)
    else:
        print "not found book at : " + book_url
        return None

def id2epub(book_id = None):
    json_file_name = OUTPUT_DIR + "lit2go_" + str(book_id) + ".json"

    from ebooklib import epub
    book = epub.EpubBook()
    # set metadata
    book.set_identifier("book_id_" + str(book_id))
    book.set_title("")
    book.set_language("en")
    # book.add_author('Author Authorowski')
    _book = None
    _charpter_obj = {}
    _charpter_text = {}
    with open(name = json_file_name, mode = 'r') as f:
        _pre_charpter_order = -1
        for line in f.readlines():
            _section = loader(line)
            if None == _book: _book = _section.charpter.book
            _charpter = _section.charpter
            _char_order = _charpter.char_order
            if not _charpter_obj.has_key(_char_order): 
                _charpter_obj[_char_order] = _charpter
                _charpter_text[_char_order] = ""
            if None != _section.section_text:
                _charpter_text[_char_order] += "<p>" + _section.section_text + "</p>"
            
    for k, v in _charpter_text.items():
        _char_obj = _charpter_obj[k]
        # create chapter
        _link_file = 'chap_'+ str(k) +'.xhtml'
        c1 = epub.EpubHtml(title=_char_obj.char_name, file_name=_link_file, lang='en')
        c1.content = v
        
        # add chapter
        book.add_item(c1)
        
        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())        
    
            
    # write to the file
    book.add_author(_book.author)
    epub_file_name = OUTPUT_DIR + _book.name.strip() + "(lit2go_" + str(book_id) + ")" + ".epub"
    epub.write_epub(epub_file_name, book, {})            
            
if __name__ == "__main__":
    # id2json(book_id=222)
    # all2json()
    
    id2epub(book_id=222)
    
    print __file__
    pass