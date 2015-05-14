##encoding=utf-8

"""
Because when you search an address on trulia, it actually encode your input and generate an url,
and do a http request. So this module is to create the request url based on your search string.

Import Command
--------------
    from util.urlencoder import urlencoder
"""

class UrlEncoder():
    def __init__(self):
        self.homepage = "http://www.trulia.com/"
    
    def encode_address(self, address):
        """trulia only accept #unit_number, and doesn't accept Apt keyword.
        And it replace the '#' with '%23', space char ' ' with plus sign'+'
        """
        address = address.replace(",", " ")
        for s in ["  ", "   ", "    "]:
            address = address.replace(s, " ")
        address = address.replace(" ", "+")
        address = address.replace("#", "%23")
        return address
        
    def by_address_and_zipcode(self, address, zipcode):
        address = address.strip()
        zipcode = zipcode.strip()
        url = "http://www.trulia.com/submit_search/?display_select=for_sale&search={0}+{1}&locationId=&locationType=&tst=h&ac_entered_query=&ac_index=&propertyId=&propertyIndex=&display=for+sale".format(
                    self.encode_address(address), zipcode)
        return url

urlencoder = UrlEncoder()

if __name__ == "__main__":
    import unittest
    from angora.LINEARSPIDER.simplecrawler import spider
    
    class UrlEncoderUnittest(unittest.TestCase):
        def test_encode_address(self):
            address = "9701 Fields Rd #1806"
            self.assertEqual(urlencoder.encode_address(address), "9701+Fields+Rd+%231806")
        
        def test_by_address_and_zipcode(self):
            address = "9701 Fields Rd #1806"
            zipcode = "20878"
            self.assertEqual(urlencoder.by_address_and_zipcode(address, zipcode),
                "http://www.trulia.com/submit_search/?display_select=for_sale&search=9701+Fields+Rd+%231806+20878&locationId=&locationType=&tst=h&ac_entered_query=&ac_index=&propertyId=&propertyIndex=&display=for+sale")
            
    unittest.main()

#     url = urlencoder.by_address_and_zipcode("9701 Fields Rd #806", "20878")
#     html = spider.html(url)
#     with open("test.html", "w") as f:
#         f.write(html)