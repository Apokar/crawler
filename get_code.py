import requests
from bs4 import BeautifulSoup

url='http://quote.stockstar.com/stock/stock_index.htm'

res = requests.get(url)

