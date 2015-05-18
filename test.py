##encoding=utf-8

from util import *
from angora.LINEARSPIDER.simplecrawler import spider
from pprint import pprint as ppt

url = urlencoder.by_address_and_zipcode("305 Thornberry Court", "21771")
html = spider.html(url)
ppt(htmlparser.get_house_detail(html))