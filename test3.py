import requests
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.szse.cn',
    'Origin': 'http://www.szse.cn',
    'Referer': 'http://www.szse.cn/main/dyndetail/searcharticle.shtml?KEYWORD=%E5%A4%A9%E6%B4%A5%E8%86%9C%E5%A4%A9%E8%86%9C',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

url ='http://www.szse.cn/szseWeb/common/szse/search/SearchArticle.jsp?' \
     'ISAJAXLOAD=true&displayContentId=none_id&SHOWTYPE=2&CATALOGTYPE=main&' \
     'ORIGINAL_CATALOGID=3&SHOWCATALOGTREE=true&SOURCESITE=main&COUNT=-1&' \
     'ARTICLESOURCE=true&REPETITION=true&DATESTYLE=2&DATETYPE=3&SEARCHBOXSHOWSTYLE=111&' \
     'INHERIT=true&SORTTYPE=both|publistime&PAGESIZE=20&USESEARCHCATALOGID=true&TYPE=3&' \
     'STARTDATE='+'2016-01-01'+'&ENDDATE='+'2017-07-06'+'&CATALOGID=3&KEYWORD=%E5%A4%A9%E6%B4%A5%E8%86%9C%E5%A4%A9%E8%86%9C'
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
print(soup)