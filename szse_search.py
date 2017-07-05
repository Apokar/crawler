import requests
import re
import json
import os
import time
from pymongo import MongoClient
import config
from bs4 import BeautifulSoup
import dict_name_code

client = MongoClient(config.db_host, config.db_port)
db = client[config.db_name]
szse_list = db[config.db_szse_collection]
path = os.getcwd() + '/'
data = {}
db.szse_list.drop()

headers = {
    'Host': 'www.szse.cn',
    'Origin': 'http://www.szse.cn',
    'Referer': 'http://www.szse.cn/main/disclosure/jgxxgk/wxhj/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def get_keywords(company, begin_time, final_time, sid):
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
                    get_list(company, keyword, begin_time, final_time, fir_index, 0, 0, index, sid, tag_name)
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
                            get_list(company, keyword, begin_time, final_time, fir_index, second_index, 0, index, sid,
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
                                get_list(company, keyword, begin_time, final_time, fir_index, second_index,
                                          third_index,
                                          index, sid, tag_name)


def get_list(company, keyword, begin_time, final_time, fir_index, sec_index, thi_index, index, sid, tag_name):
    try:
        print('start')
        code = dict_name_code.get_code(company)

        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=main_wxhj&TABKEY=tab1&REPORT_ACTION=search&txtZqdm=' + code + '&selecthjlb=&txtStart=' \
              + begin_time + '&txtEnd=' + final_time
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        print('搜索主板')
        table = soup.find('table', id='REPORTID_tab1')

        if table == None:
            print('主板没有')
            print('搜索中小板')
            table = soup.find('table', id='REPORTID_tab2')
            if table == None:
                print('中小板没有')
                print('搜索创业板')
                table = soup.find('table', id='REPORTID_tab3')
                print('搜完')

        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')

            if len(tds) == 6:
                code = tds[0].text

                name = tds[1].text

                date = tds[2].text

                classify = tds[3].text

                a = tds[4].find_all('a')[0].get('onclick')
                p = re.compile("encodeURIComponent\(('.*')\)")
                link = p.findall(a)[0][1:-1]

                if classify == '非许可类重组问询函' or classify == '许可类重组问询函':
                    # my_time = str(date)
                    # timeArray = time.localtime(int(my_time))
                    # date = time.strftime("%Y-%m-%d", timeArray)
                    # timeArray2 = time.strptime(begin_time, "%Y-%m-%d")
                    # b_time = str(time.mktime(timeArray2))
                    # timeArray3 = time.strptime(final_time, "%Y-%m-%d")
                    # f_time = str(time.mktime(timeArray3))
                    #
                    # if b_time < date < f_time:
                    URL = 'http://www.szse.cn/UpFiles/fxklwxhj/' + link
                    tr['down_url'] = URL
                    data['index'] = index
                    data['company'] = company  ##############
                    data['date'] = date
                    data['tag_name'] = tag_name
                    data['fir_index'] = fir_index
                    data['sec_index'] = sec_index
                    data['thi_index'] = thi_index
                    data['sid'] = sid
                    szse_list.insert(data)

                    # rr = requests.get(URL)
                    # with open(path + '/get_file/szse/' + link[:-4] + '.pdf', 'wb') as f:
                    #     f.write(rr.content)
                    #     print(link[:-4]+'download is DONE')
    except:
        print('restart')
        get_list(company, keyword, begin_time, final_time, fir_index, sec_index, thi_index, index, sid, tag_name)