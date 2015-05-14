##encoding=utf-8

"""
This module is to parse html to get useful information from trulia

Import Command
--------------
    from util.htmlparser import htmlparser
"""

from bs4 import BeautifulSoup as BS4

class HTMLParser():
    def __init__(self):
        pass

    def _int_filter(self, text):
        """摘出文本内所有0-9数字的部分"""
        res = list()
        for char in text:
            if char.isdigit():
                res.append(char)
        return int("".join(res))

    def _float_filter(self, text):
        res = list()
        for char in text:
            if (char.isdigit() or (char == ".")):
                res.append(char)
        return float("".join(res))
    
    def _public_record_parser(self, public_record):
        """解析feature信息, 稳定输出, 不会有异常"""
        results = {
            "price": None,
            "sqft": None,
            "lot_size": None,
            "bedroom": None,
            "bathroom": None,
            "status": None,
            "heating": None,
            "exterior_walls": None,
            "build_year": None,
            }
        
        for field in public_record:
            field = field.lower()
            ## 价格
            if "price" in field:
                results["price"] = self._int_filter(field)
            
            ## 面积
            elif ("sqft" in field) and ("lot size" not in field):
                results["sqft"] = self._int_filter(field)
                
            ## 院子面积
            elif ("sqft" in field) and ("lot size" in field):
                results["lot_size"] = self._int_filter(field)
                results["lot_size_unit"] = "sqft"
            elif ("acres" in field) and ("lot size" in field):
                results["lot_size"] = self._float_filter(field)
                results["lot_size_unit"] = "acer"
                
            ## 卧室
            elif "bedroom" in field:
                results["bedroom"] = self._int_filter(field)
                
            ## 洗手间
            elif "bathroom" in field:
                results["bathroom"] = self._int_filter(field)
                
            ## 市场状态
            elif "status" in field:
                results["status"] = field.split(":")[-1].strip()
                
            ## 供暖方式
            elif "heating" in field:
                results["heating"] = field.split(":")[-1].strip()
                
            ## 外墙
            elif "exterior walls" in field:
                results["exterior_walls"] = field.split(":")[-1].strip()
                
            ## 建造年份
            elif "built in" in field:
                results["build_year"] = self._int_filter(field)
                
            ## County
            elif "county" in field:
                results["county"] = field.split(":")[-1].strip()
                
        for key in list(results.keys()):
            if not results[key]:
                del results[key]
                
        return results

    def get_house_detail(self, html):
        """get all details in html
        """
        soup = BS4(html)
        data = dict()
        # address, city, state, zipcode
        try:
            address_field = list()
            h1 = soup.find("h1", itemprop = "address")
            for span in h1.find_all("span"):
                if span.string:
                    address_field.append(span.string.strip())
            if len(address_field) == 4:
                data["address"] = address_field[0]
                data["city"] = address_field[1]
                data["state"] = address_field[2]
                data["zipcode"] = address_field[3]
        except:
            pass
        
        # price
        try:
            for span in soup.find_all("span", itemprop="price"):
                try:
                    data["price"] = self._int_filter(span.text)
                except:
                    pass
        except:
            pass
            
        # public record
        try:
            public_record_field = list()
            for ul in soup.find_all("ul", class_ = "listInline mbn pdpFeatureList"):
                for li in ul.find_all("li"):
                    if len(li.attrs) == 0:
                        public_record_field.append(li.text.strip())
                        
            results = self._public_record_parser(public_record_field)
            for k, v in results.items():
                data.setdefault(k, v)
        except:
            pass
        
        return data
        
htmlparser = HTMLParser()

if __name__ == "__main__":
    import unittest
    from pprint import pprint as ppt
    
    def read(abspath, encoding="utf-8"):
        with open(abspath, "rb") as f:
            return f.read().decode(encoding)
    
    class HTMLParserUnittest(unittest.TestCase):
        def test_all(self):
            html = read(r"testdata\property01.html")
            data = htmlparser.get_house_detail(html)
            ppt(data)

            html = read(r"testdata\property02.html")
            data = htmlparser.get_house_detail(html)
            ppt(data)
            
    unittest.main()