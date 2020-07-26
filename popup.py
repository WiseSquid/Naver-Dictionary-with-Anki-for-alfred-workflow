#!/usr/bin/python2.7
# encoding: utf-8

import cocoa
import sys
from urllib import quote, urlencode
from unicodedata import normalize


reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    query = sys.argv[1]
    word, meaning = query.split('::')

    url = 'https://en.dict.naver.com/#/search?query=%s'

    query = normalize('NFC', unicode(word)).encode('utf-8')
    url = url % quote(query)
    print(url)
    view = cocoa.BrowserView('Naver Dictionary', url, width=720, height=700)
    view.show()
    sys.exit(0)