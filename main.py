#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from os import path
from datetime import datetime
import logging
import sqlite3
import sys

import requests
from bs4 import BeautifulSoup
from config import EMAIL, PASSWORD, DEVICE

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')


db = sqlite3.connect(sys.path[0], 'main.db')
cursor = db.cursor()

session = requests.session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})

def get_hidden_form_data(form):
    ret = dict()
    for i in form.findAll('input', type='hidden'):
        ret[i['name']] = i['value']
    return ret

def login(email, password):
    logging.info('Login...')
    LOGIN_URL = 'https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dgno_signin'
    LOGIN_POST_URL = 'https://www.amazon.com/ap/signin'
    login_page = BeautifulSoup(session.get(LOGIN_URL).text)
    form = login_page.find('form', id='ap_signin_form')
    data = get_hidden_form_data(form)
    data.update({'email': email, 'password': password})
    session.post(LOGIN_POST_URL, data)

def get_contents():
    URL = 'https://www.amazon.com/gp/digital/fiona/manage/features/order-history/ajax/queryPdocs.html'
    req = session.post(URL, {'offset': 0, 'count': 15, 
        'contentType': 'Personal Document', 'queryToken': 0, 'isAjax': 1})
    return [{'category': i['category'], 'contentName': i['asin']} 
            for i in req.json()['data']['items']]

def deliver_content(content):
    URL = 'https://www.amazon.com/gp/digital/fiona/content-download/fiona-ajax.html/ref=kinw_myk_ro_send'
    content.update({'isAjax': '1', 'deviceID': DEVICE})
    req = session.post(URL, content)
    assert req.json()['data'] == 1

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
