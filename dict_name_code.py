import re
import requests
from bs4 import BeautifulSoup
#公司名称代码 字典
url = 'http://quote.eastmoney.com/stocklist.html'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
p = re.compile('\((\d*)\)')
p2 = re.compile('(.*)\(')

div = soup.find('div', class_='quotebody')
new_code_doc = {}


for a in div.find_all('li'):
    code_name = a.text.encode('latin1').decode('gbk')
    text = p.findall(code_name)
    text2 = p2.findall(code_name)
    new_code_doc[text[0]] = text2[0]
    new_code_doc[text2[0]] = text[0]


# print(new_code_doc)

def get_code(name):


    code = new_code_doc[name]
    # print(code)

    return code
#
# if __name__=='__main':
#
#     get_code('ST智慧')