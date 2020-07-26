#!/usr/bin/python2.7
# encoding: utf-8

import sys
import os
import requests
import json, string, subprocess


reload(sys)
sys.setdefaultencoding("utf-8")

def request(action, **params):
    return {'action': action, 'params': params['params'], 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    try:
        response = json.loads(requests.post(url='http://localhost:8765', data=requestJson).content)
    except:
        print(u'Please run Anki first')
    try:
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
    except Exception as e:
        print(e)
    return response['result']

if __name__ == '__main__':
    query = sys.argv[1]
    word, meaning = query.split('::')
    with open('addnote.json') as f:
        jsonForm = f.read()
        template = string.Template(jsonForm)
        params = json.loads(template.substitute({'deckname': '"' + os.environ['deck_name'] + '"',
                                                 'front': '"' + word + '"',
                                                 'back': '"' + meaning + '"'}))
        result = invoke(action='addNote', params=params)
    print(result)