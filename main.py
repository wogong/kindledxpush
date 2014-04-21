#!/usr/bin/env python
# -*- coding=UTF-8 -*-

import logging
import sqlite3
import sys
from os import path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from config import EMAIL, PASSWORD, DEVICE

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')


db = sqlite3.connect(path.join(sys.path[0], 'main.db'))
cursor = db.cursor()

s = requests.session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})

def get_hidden_form_data(page):
    hidden_form_data = dict()
    input_tags = page.findAll('input', type='hidden')
    for tag in input_tags:
        hidden_form_data[tag['name']] = tag['value']
    return hidden_form_data

def login(email, password):
    logging.info('Login...')
    login_url = 'https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dgno_signin'
    login_post_url = 'https://www.amazon.com/ap/signin'
    login_page = BeautifulSoup(s.get(login_url).text)
    data = get_hidden_form_data(login_page)
    data.update({'email': email, 'password': password})
    s.post(login_post_url, data)

def get_contents():
    url = 'https://www.amazon.com/gp/digital/fiona/manage/features/order-history/ajax/queryPdocs.html'
    r = s.post(url, {'offset': 0, 'count': 15, 
        'contentType': 'Personal Document', 'queryToken': 0, 'isAjax': 1})
    return [{'category': item['category'], 'contentName': item['asin']} 
            for item in r.json()['data']['items']]

def deliver_content(content):
    url = 'https://www.amazon.com/gp/digital/fiona/content-download/fiona-ajax.html/ref=kinw_myk_ro_send'
    content.update({'isAjax': '1', 'deviceID': DEVICE})
    r = s.post(url, content)
    assert r.json()['data'] == 1

def deliver_all(contents):
    logging.info('Delivering...')
    def contentInDB(content):
        try:
            cursor.execute('select * from content where name = "%s"' % content)
        except sqlite3.OperationalError:
            cursor.execute('create table content (name text)')
            return False
        else:
            return False if cursor.fetchone() is None else True

    contents = filter(lambda x: not contentInDB(x['contentName']), contents)
    for content in contents:
        try:
            logging.info('delivering ' + content['contentName'])
            deliver_content(content)
        except:
            logging.error('Error, ignore')
            pass
        else:
            logging.info('Done. Save to db.')
            cursor.execute('insert into content values ("%s")' % content['contentName'])

    db.commit()

if __name__ == '__main__':
    logging.basicConfig(filename=path.join(sys.path[0], 'main.log'), 
                        level='INFO', 
                        format='%(asctime)s [%(levelname)s] %(message)s')
    login(EMAIL, PASSWORD)
    deliver_all(get_contents())
