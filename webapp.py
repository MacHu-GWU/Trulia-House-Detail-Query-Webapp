##encoding=utf-8

"""
This is a web app you can use to find house detail information by address + zipcode
"""

from util import *
from angora.LINEARSPIDER.simplecrawler import spider
from angora.DATA.js import dump_js
import bottle
import datetime
import os

class Payload():
    def __init__(self):
        self.data = {
            "batch_query_result": None
            }
    
@bottle.route("/")
def index():
    payload = Payload()
    return bottle.template("index", payload.data)

@bottle.post("/result")
def get_trulia_result():
    payload = Payload()
    
    upload = bottle.request.files.get("upload")
    filename = str(datetime.datetime.now().timestamp()) # add timestamp as surfix
    uploadpath = r"user_uploaded\%s.csv" % filename
    upload.save(uploadpath)
    
    # read user uploaded data
    try:
        df = list()
        with open(uploadpath, "r") as f:
            for lines in f.readlines():
                row = [s.strip() for s in lines.split("\t")]
                if len(row) == 2:
                    df.append(row)
    except:
        pass
    
    for row in df:
        url = urlencoder.by_address_and_zipcode(row[0], row[1])
        html = spider.html(url)
        if html:
            try:
                data = htmlparser.get_house_detail(html)
                row.append(data)
            except:
                pass
    dump_js(df, r"user_uploaded\%s.json" % filename)
    
    payload.data["batch_query_result"] = "%s.json" % filename
    return bottle.template("index", payload.data)

@bottle.route("/<filename>")
def serve_static(filename):
    if filename == "example_input.txt":
        return bottle.static_file(filename, root="static")
    else:
        return bottle.static_file(filename, root="user_uploaded")

if __name__ == "__main__":
    try:
        os.mkdir("user_uploaded")
    except:
        pass
    bottle.run(host="10.255.145.57", port=8080, debug=True)