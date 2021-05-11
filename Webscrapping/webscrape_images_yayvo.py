from bs4 import BeautifulSoup as soup
import urllib
import requests
import pandas as pd
import time
import os
from flask import Flask, render_template,  session, redirect, request
from flask_cors import CORS,cross_origin


app = Flask(__name__)

class DataCollection:
    def __init__(self):
        self.data = {
		"Name": list(),
		"Old Price (PKR)": list(),
        "Regular Price (PKR)": list(),
        "Special Price (PKR)": list(),
        "Discount %": list(),
        "Brand Name": list()}

    def get_final_data(self, commentbox=None, i=None):

        try:
            Row = commentbox.find_all("li", {"class": "item"})
            self.data["Name"].append(Row[i].a.img["alt"])
        except:
            self.data["Name"].append("No name")
        try:
            # page_soup.find_all("p",{"class":"old-price"})
            self.data["Old Price (PKR)"].append(commentbox.find_all("p", {"class": "old-price"})[i].get_text().strip())
            # self.data["Old Price (PKR)"].append("Amin")
        except:
            self.data["Old Price (PKR)"].append('0')
        try:

            self.data["Regular Price (PKR)"].append(
                commentbox.find_all("span", {"class": "price"})[i].get_text().strip())
            # self.data["Regular Price (PKR)"].append("Fatima")
        except:
            self.data["Regular Price (PKR)"].append('0')
        try:

            self.data["Special Price (PKR)"].append(
                commentbox.find_all("p", {"class": "special-price"})[i].get_text().strip())
            # self.data["Special Price (PKR)"].append("Mahira")
        except:
            self.data["Special Price (PKR)"].append('0')

        try:

            self.data["Discount %"].append(
                commentbox.find_all("span", {"class": "discount_Span"})[i].get_text().strip())
            # self.data["Discount %"].append("Anas")
        except:
            self.data["Discount %"].append('0')
        try:
            self.data["Brand Name"].append(commentbox.find_all("div", {"class": "cstm_brnd"})[i].get_text().strip())
            # self.data["Brand Name"].append("Siddiq")
        except:
            self.data["Brand Name"].append('none')

    def get_main_HTML(self, base_URL=None, search_string=None):
        # construct the search url with base URL and search string
        # http://yayvo.com/search/result/?q=samsung+mobiles
        search_url = f"{base_URL}/search/result/?q={search_string}"
        # usung urllib read the page
        with urllib.request.urlopen(search_url) as url:
            page = url.read()
        # return the html page after parsing with bs4
        return soup(page, "html.parser")

    def get_data_dict(self):
        return self.data



if __name__ == '__main__':
    base_URL = 'https://www.yayvo.com'
    #search_string = 'samsung mobiles'
    search_string = 'women shalwar kameez'
    # search_string = request.form['content']

    search_string = search_string.replace(" ", "+")
    print('processing, Please wait')
    #start = time.perf_counter()


    get_data = DataCollection()

    yayvo_HTML = get_data.get_main_HTML(base_URL, search_string)
    #print(yayvo_HTML)
    #print(len(yayvo_HTML))

    i=0
    while (i <= len(yayvo_HTML)):
        # prod_title.append(yayvo_HTML[i].a.img["alt"])
        get_data.get_final_data(yayvo_HTML, i)
        i = i + 1

    yayvo_Scrapped = pd.DataFrame(get_data.get_data_dict())
    yayvo_Scrapped = yayvo_Scrapped.head(15)
    print("---------chkinggg -------------")
    print(yayvo_Scrapped.head())
