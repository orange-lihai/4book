#! /usr/bin/python
# -*- encoding: utf-8 -*-

import urllib, httplib2
import json
import sys
sys.path.append('.')

headers_url = {"Content-Type":"application/x-www-form-urlencoded", "Connection": "Keep-Alive"}
headers_json = {"Content-Type":"application/json;charset=UTF-8", "Connection": "Keep-Alive"}
headers_url2 = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8", "Connection": "Keep-Alive"}

def do_post(url, data, headers):
    h = httplib2.Http()
    s, r = h.request(uri=url, method="POST", body=data, headers=headers)    
    if s and hasattr(s, "status") and s["status"] == "200":
        return r
    else:
        print s
        return None
    
def do_get(url):
    h = httplib2.Http()
    s, r = h.request(uri=url, method="GET")    
    if s and hasattr(s, "status") and s["status"] == "200":
        return r
    else:
        print s
        return None

if __name__ == "__main__":
    test_url = "http://etc.usf.edu/lit2go/222/"
    print do_get(url = test_url)
    pass