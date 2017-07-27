#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import datetime, time, os, json
from jsonweb.encode import to_object, dumper
from glob import glob
# '%Y-%m-%d %H:%M:%S'
import xlwt

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, '../logs/')
OUTPUT_DIR = os.path.join(BASE_DIR, '../output/')

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)

def timestr4suffix():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

def time2str(f = '%Y-%m-%d %H:%M:%S', d = None):
    if d == None: d = time.localtime(time.time())
    return time.strftime(f, d)

def time_diff(d_one = None, d_two = None, unit = 60):
    return (int)((d_one - d_two).total_seconds() / unit)

def str2time(f = '%Y-%m-%d %H:%M:%S', s = None):
    if s == None: s = time2str()
    return time.strptime(s, f) 


def removefiles(patten_str):
    try:
        os.remove(glob(patten_str))
    except:
        pass

def removefile(file_name):
    try:
        os.remove(os.path.abspath(file_name))
    except:
        pass

def save2excel(file_name = 'rs.xls', sheet_name = 'sheet1', rs = [], header_attrs = []):
    file_name = OUTPUT_DIR + file_name
    wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet(sheetname = sheet_name, cell_overwrite_ok = True)   
    for i in range(len(rs)):
        c = rs[i]
        for j in range(len(header_attrs)):
            h = header_attrs[j]
            if i == 0: sheet.write(i, j, h['v'])        
            sheet.write(i + 1, j, c[h['k']])        

    removefile(file_name)    
    wb.save(file_name)
    return wb

def append2excel(wb = None, file_name = 'rs.xls', sheet_name = 'sheet1', rs = [], header_attrs = []):
    file_name = OUTPUT_DIR + file_name
    if wb is None:
        wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet(sheetname = sheet_name, cell_overwrite_ok = True)   
    for i in range(len(rs)):
        c = rs[i]
        for j in range(len(header_attrs)):
            h = header_attrs[j]
            if i == 0: sheet.write(i, j, h['v'])        
            sheet.write(i + 1, j, c[h['k']])
    wb.save(file_name)        
    return wb
    
def save2txt(file_name = 'rs.txt', rs = []):
    file_name = OUTPUT_DIR + file_name
    with open(name=file_name, mode='w', buffering=1024) as f:
        for r in rs:
            if isinstance(r, str):
                f.write(r)
            else:
                f.write(dumper(r))
            f.write('\n')
            
def append2txt(file_name = 'rs.txt', rs = []):
    file_name = OUTPUT_DIR + file_name
    with open(name=file_name, mode='a', buffering=1024) as f:
        for r in rs:
            f.write(r)
            f.write('\n')
            
def remove1file(file_name = ""):
    if file_name is not None and len(file_name) > 0:
        try:
            file_name = OUTPUT_DIR + file_name
            removefile(file_name)
        except OSError:
            pass        

# 判断一个字符串是否是时间字符串, 比如: 2016年06月16日, 8小时前, 5分钟前 等等.
def istimestr(s):
    if s is None: return False
    idx = s.find(u'年')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'月')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True    
    idx = s.find(u'日')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True 
    idx = s.find(u'时')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'分')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'秒')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'天')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'小时')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'分钟')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True    
    return False

def list_file(file_path):
    rs = []
    path_dir =  os.listdir(file_path)
    for all_dir in path_dir:
        child = os.path.join('%s%s' % (file_path, all_dir))
        rs.append(child.decode('gbk'))
    return rs    
    
if "__main__" == __name__:
    print timestr4suffix()
    print time2str()
    save2excel(rs=[{'a': 'xxxxxx', 'b': 111}, {'a': 'yyyyy', 'b': '90888'}], header_attrs = [{'k': 'a', 'v': '我们'}, {'k': 'b', 'v': 'cccc'}])
    print istimestr(u'杭州日报')