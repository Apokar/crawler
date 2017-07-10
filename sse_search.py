import requests
import json
import os
from pymongo import MongoClient
import config
import simplejson

client = MongoClient(config.db_host, config.db_port)
db = client[config.db_name]
sse_list = db[config.db_sse_collection]
path = os.getcwd() + '/'

db.sse_list.drop()

headers = {
    'Host': 'query.sse.com.cn',

    'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def get_keywords(company, begin_time, over_time, sid):
    f = open(path + 'config.json', encoding='utf-8')
    config = json.load(f)
    for a in config:
        fir_index = a.get('index')
        if not a.get('subs'):
            for item in a.get('tags'):
                keywords = item.get('keywords')
                index = item.get('index')
                tag_name = item.get('name')
                for keyword in keywords:
                    get_list(company, keyword, begin_time, over_time, fir_index, 0, 0, index, sid, tag_name)
        else:
            first_subs = a.get('subs')
            for sub in first_subs:
                second_index = sub.get('index')
                if not sub.get('subs'):
                    for item in sub.get('tags'):
                        keywords = item.get('keywords')
                        index = item.get('index')
                        tag_name = item.get('name')
                        for keyword in keywords:
                            get_list(company, keyword, begin_time, over_time, fir_index, second_index, 0, index, sid,
                                     tag_name)
                else:
                    second_subs = sub.get('subs')
                    for sec_sub in second_subs:
                        third_index = sec_sub.get('index')
                        for item in sec_sub.get('tags'):
                            keywords = item.get('keywords')
                            index = item.get('index')
                            tag_name = item.get('name')
                            for keyword in keywords:
                                get_list(company, keyword, begin_time, over_time, fir_index, second_index, third_index,
                                         index, sid, tag_name)


def get_list(company, keyword, begin_time, over_time, fir_index, sec_index, thi_index, index, sid, tag_name):
    try:
        url = 'http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&page=1&searchword=T_L CTITLE T_D E_KEYWORDS T_JT_E likeT_L' + \
              company + keyword + 'T_RT_R&orderby=-CRELEASETIME&perpage=10&_=1499325097160'
        r = requests.get(url, headers=headers)
        if r.text:
            content = simplejson.loads(r.text)
            c = content['data']
            for data in c:
                if begin_time < data['CRELEASETIME'] < over_time:
                    doc = {'down_url': 'http://www.sse.com.cn' + data['CURL'], 'index': index, 'company': company,
                           'date': data['CRELEASETIME'], 'tag_name': tag_name, 'fir_index': fir_index,
                           'sec_index': sec_index, 'thi_index': thi_index, 'sid': sid}
                    sse_list.insert(doc)
    except:
        get_list(company, keyword, begin_time, over_time, fir_index, sec_index, thi_index, index, sid, tag_name)


get_keywords('爱建集团', '2015-06-01', '2017-07-01', '公告')
