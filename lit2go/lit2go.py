#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys, os, time, datetime
from bs4 import BeautifulSoup as BS
sys.path.append('..')
from common.http_util import do_get
from common.utils import time_diff

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, '../logs/')
OUTPUT_DIR = os.path.join(BASE_DIR, '../output/')

prefix_url = "http://etc.usf.edu/lit2go/"
max_book_id = 222
max_book_id_time = datetime.datetime.now()

class Book():
    def __init__(self):
        self._id = ""
        self.url = ""
        self.name = ""
        self.author = ""
        self.desc = ""
        self.source = ""
        self.cover_img = None
        self.year_published = ""
        self.language = ""
        self.country_of_origin = ""
        self.readability = ""
        self.word_count = ""
        self.genre = ""
        self.keywords = ""
        pass
    def __delete__(self):
        pass
    
class Charpter():
    def __init__(self):
        self.book = None
        self.char_name = ""
        self.char_desc = ""
        self.char_order = ""
        self.char_url = ""
        self.char_mp3 = None
        self.char_mp3_seconds = ""
        pass
    def __delete__(self):
        pass    

class Section():
    def __init__(self):
        self.charpter = None
        self.section_text = ""
        pass
    def __delete__(self):
        pass    
    
def max_book_id():
    _now = datetime.datetime.now()
    _day = time_diff(_now, max_book_id_time)
    if _day > 1:
        return max_book_id
    else:
        return max_book_id

def get_book_by_url(book_url = None):
    # _book_doc = BS(do_get(book_url))
    _book_doc = BS(open(OUTPUT_DIR + '222.html'))
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
    _book._id = book_url.split("/")[-2]
    _book.name = _doc_title.string
    _book.author = _doc_author.string
    _book.cover_img = _doc_img
    
    _ps = _doc_column_primary.find_all(name="p", recursive=False)
    for _p in _ps:
        _strong_tag = _p.find(name="strong")
        _em_tag = _p.find(name="em")
        if None != _strong_tag: _book.source = _p.string
        if None != _em_tag: _book.desc = _p.string
        
    _doc_column_secondary = _doc_page_content.find(name="header")
    _doc_column2_strong = _doc_column_secondary.find_all(name="strong")
    for _s in _doc_column2_strong:
        _ss = _s.string
        _ss_next = _s.find_next().string
        if _ss.find("Year Published") >= 0: _book.year_published = _ss_next
        if _ss.find("Language") >= 0: _book.language = _ss_next
        if _ss.find("Country of Origin") >= 0: _book.country_of_origin = _ss_next
        if _ss.find("Readability") >= 0: _book.readability = _ss_next
        if _ss.find("Word Count") >= 0: _book.word_count = _ss_next
        if _ss.find("Genre") >= 0: _book.genre = _ss_next
        if _ss.find("Keywords") >= 0: _book.keywords = _ss_next
    
    # fill _charpters
    _dts = _doc_column_primary.find_all(name="dt")
    for _dt in _dts:
        _dta = _dt.find(name="a")        
        
        _char = Charpter()
        _char.book = _book
        _char.char_name = _dta.string
        _char.char_url = _dta.attrs["href"]
        _dtdd = _dt.find_next_sibling()
        if _dtdd.name == "dd": _char.char_desc = _dtdd.string        
        
        _charpters.append(_char)
        
    # _sections
    for _c in _charpters:
        _char_url = _c.char_url
        _char_doc = BS(do_get(_char_url))
        _content = _char_doc.find(name="div", attrs={"id": "i_apologize_for_the_soup"})
        _ps = _content.find(name="p", recursive=False)
        for _p in _ps:
            _section = Section()
            _section.charpter = _c
            _section.section_text = _p.string
            
            _sections.append(_section)
        
    return _book, _charpters, _sections

def get_book_by_id(book_id = None):
    book_url = prefix_url + "/" + book_id + "/"
    return get_book_by_url(book_url)

def save2db(book = None, charpters = [], sections = []):
    pass

def convert2mobi(book = None, charpters = [], sections = []):
    pass

def all2mobi(folder_name = None):
    pass

def url2mobi(book_url = None):
    # extract data from web
    book, charpters, sections = get_book_by_url(book_url)
    # convert to mobi
    convert2mobi(book=book, charpters=charpters, sections=sections)
    # return 
    return book, charpters, sections

def id2mobi(book_id = None):
    book_url = prefix_url + "/" + str(book_id) + "/"
    if book_id is not None and book_id > 0 and book_id <= max_book_id():
        return url2mobi(book_url)
    else:
        print "not found book at : " + book_url
        return None

if __name__ == "__main__":
    id2mobi(book_id=222)
    print __file__
    pass