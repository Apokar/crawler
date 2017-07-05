import sse_search
import cninfo_search
import szse_search
import dict_name_code
import re
import simplejson

import requests
#
# print(cninfo_search.get_keywords('联建光电','2017-06-01','2017-07-01','意见书'))
# print(sse_search.get_keywords('*ST智慧','2017-06-01','2017-07-01','公告'))
# sse_search.get_keywords('*ST智慧','2017-06-01','2017-07-01','公告')
szse_search.get_keywords('华北高速','2017-06-01','2017-07-01','公告')
#
#
# headers = {
#     'Host': 'query.sse.com.cn',
#     'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
# }
#
# url = 'http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback46016&siteId=28&sqlId=BS_GGLL&extGGLX=&extWTFL=&stockcode=601519&channelId=10743%2C10744%2C10012&createTime=2017-05-01+00%3A00%3A00&createTimeEnd=2017-07-05+23%3A59%3A59&extGGDL=&order=createTime%7Cdesc%2Cstockcode%7Casc&isPagination=true&pageHelp.pageSize=15&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1499240365278'
#
# r = requests.get(url, headers=headers)
#
# # p = re.compile('jsonpCallback[0-9]{5}\((.*)\)')
# # content = simplejson.loads(p.findall(r.text)[0])
# # c = content['pageHelp']
# # for data in c['data']:
# #     print(data)
