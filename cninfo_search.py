import requests
import time
import json
import os
from pymongo import MongoClient
import config

client = MongoClient(config.db_host, config.db_port)
db = client[config.db_name]
cninfo_list = db[config.db_cninfo_collection]
path = os.getcwd() + '/'
db.cninfo_list.drop()

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


def get_list(company, keyword, begin_time, final_time, fir_index, sec_index, thi_index, index, sid, tag_name):
    try:
        url = 'http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full?searchkey=' + company + keyword + \
              '&isfulltext=false&sortType=desc&pageNum=1'
        r = requests.get(url)
        ans = r.json()['announcements']
        for an in ans:
            # 格式化标题
            an['announcementTitle'] = an['announcementTitle'].replace('<em>', '').replace('</em>', '')

            # 时间比较
            my_time = str(an['announcementTime'])[:-3]
            timeArray = time.localtime(int(my_time))
            date = time.strftime("%Y-%m-%d", timeArray)
            timeArray2 = time.strptime(begin_time, "%Y-%m-%d")
            b_time = str(time.mktime(timeArray2))
            timeArray3 = time.strptime(final_time, "%Y-%m-%d")
            f_time = str(time.mktime(timeArray3))

            if b_time < my_time < f_time:
                down_url = 'http://www.cninfo.com.cn/' + an['adjunctUrl']
                an['down_url'] = down_url
                an['index'] = index
                an['company'] = company
                an['date'] = date
                an['tag_name'] = tag_name
                an['fir_index'] = fir_index
                an['sec_index'] = sec_index
                an['thi_index'] = thi_index
                an['sid'] = sid
                cninfo_list.insert(an)

                # 下载文件
                # rr = requests.get(down_url)
                # with open(path + '/get_file/cninfo/' + an['announcementTitle'] + '.pdf', 'wb') as f:
                #     f.write(rr.content)
                #     print(an['announcementTitle'] + ' done ~~~~')

            else:
                print(an['announcementTitle'] + '不合条件!!!')
    except:
        print('restart')
        get_list(company, keyword, begin_time, final_time, fir_index, sec_index, thi_index, index, sid, tag_name)