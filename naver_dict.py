#!/usr/bin/python2.7
# encoding: utf-8

import sys
import os
import re, json, itertools
import requests
from unicodedata import normalize


reload(sys)
sys.setdefaultencoding("utf-8")

def get_naver_json_form(data, trash):
    jsonForm = re.findall(trash, ''.join(data.splitlines()))[0]
    return json.loads(jsonForm)

def callback(query):
    url = 'https://ac.dict.naver.com/enkodict/ac'

    header = {
        'referer': 'https://en.dict.naver.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }

    # query
    queryParams = {
        'st': '11001',
        'r_lt': '11001',
        'q': query,
        '_callback': 'window.__jindo2_callback._3731'
    }

    response = requests.get(url, headers=header, params=queryParams)

    jsonResult = get_naver_json_form(response.content, r'window\.__jindo2_callback\._3731\((.*?)\)')
    results = []
    for data in jsonResult['items'][0]:
        data = list(itertools.chain(*data)) # remove inner list
        results.append([data[0], data[1]])
    return results

def add_item(title, subtitle=None, arg=None):
    title = title.replace('<', '(')
    title = title.replace('>', ')')
    subtitle = subtitle.replace('<', '(')
    subtitle = subtitle.replace('>', ')')
    arg = arg.replace('<', '(')
    arg = arg.replace('>', ')')
    return u'<item arg="%s"><title>%s</title><subtitle>%s</subtitle></item>' \
           % (arg, title, subtitle)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError
    query = sys.argv[1]

    items = callback(query)

    print '<?xml version="1.0"?>'
    print '<items>'
    if items:
        for word, meaning in items:
            title = u'%s : %s' % (word, meaning)
            arg = u'%s::%s' % (word, meaning)
            subtitle = u"Open Naver Dictionary for '%s'" % word
            print add_item(title=title, subtitle=subtitle, arg=arg)
    else:
        print add_item(title=u'검색된 결과가 없습니다.')
    print '</items>'