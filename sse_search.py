import requests
import re
import json
import os
import time
from pymongo import MongoClient
import config
import simplejson

client = MongoClient(config.db_host, config.db_port)
db = client[config.db_name]
sse_list = db[config.db_collection]
path = os.getcwd() + '/sse_list/'

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


def get_list(code, begin_time, final_time, fir_index, sec_index, thi_index, index, sid, tag_name):
    url = 'http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback98128&siteId=28&sqlId=BS_GGLL&extGGLX=&extWTFL=&stockcode=' + code + \
          '&channelId=10743%2C10744%2C10012&createTime=begin_time+00%3A00%3A00&createTimeEnd=2017-07-01+23%3A59%3A59&extGGDL=&order=createTime%7Cdesc%2Cstockcode%7Casc&isPagination=true&pageHelp.pageSize=15&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1498869654007'

    url = 'http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback18040&siteId=28&sqlId=BS_GGLL&extGGLX=&extWTFL=&stockcode=600643&channelId=10743%2C10744%2C10012&createTime=2017-06-01+00%3A00%3A00&createTimeEnd=2017-07-01+23%3A59%3A59&extGGDL=&order=createTime%7Cdesc%2Cstockcode%7Casc&isPagination=true&pageHelp.pageSize=15&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1498870427118'
    r = requests.get(url, headers=headers)
    p = re.compile('jsonpCallback18040\((.*)\)')
    content = simplejson.loads(p.findall(r.text)[0])
    c = content['pageHelp']
    for data in c['data']:
        # 格式化标题
        # an['announcementTitle'] = an['announcementTitle'].replace('<em>', '').replace('</em>', '')

        # 时间比较
        my_time = str(data['cmsOpDate'])
        timeArray = time.localtime(int(my_time))
        date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        timeArray2 = time.strptime(begin_time, "%Y-%m-%d")
        b_time = str(time.mktime(timeArray2))
        timeArray3 = time.strptime(final_time, "%Y-%m-%d")
        f_time = str(time.mktime(timeArray3))

        if b_time < my_time < f_time:
            data['down_url'] = data['docURL']
            data['index'] = index
            data['company'] = code    ##############
            data['date'] = date
            data['tag_name'] = tag_name
            data['fir_index'] = fir_index
            data['sec_index'] = sec_index
            data['thi_index'] = thi_index
            data['sid'] = sid
            sse_list.insert(data)

            #下载文件
            rr = requests.get(data['docURL'])
            with open(path + '/' + data['docTitle'] + '.pdf', 'wb') as f:
                f.write(rr.content)

        else:
            print(data['docTitle'] + '不合条件!!!')
