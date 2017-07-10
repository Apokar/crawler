import requests
import re
import simplejson

headers = {
    'Host': 'query.sse.com.cn',
    'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

url = 'http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&jsonCallBack=jQuery111206993248700197028_1499301464793&page=1&searchword=T_L+CTITLE+T_D+E_KEYWORDS+T_JT_E+T_L爱建集团*公告T_RT_R&orderby=-CRELEASETIME&perpage=10&_=1499301464816'

r = requests.get(url, headers=headers)
p = re.compile('jQuery[0-9]{21}_[0-9]{13}\((.*)\)')
content = simplejson.loads(p.findall(r.text)[0])
c = content['data']
print(c)
#
# for data in c:
#     # dict['down_url'] = 'http://www.sse.com.cn'+c['CURL']
#
#     print(data['CRELEASETIME'])
#     # dict['tag_name'] = tag_name
    # dict['fir_index'] = fir_index
    # dict['sec_index'] = sec_index
    # dict['thi_index'] = thi_index
    # dict['sid'] = sid
    # sse_list.insert(data)
